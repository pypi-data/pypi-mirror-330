/*!
 * Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
import { NotebookPanel } from '@jupyterlab/notebook';
import { ICellModel } from '@jupyterlab/cells';
import { FileContext } from '../client/codewhispererclient'

import { FileContextMetadata } from "../utils/models";

import { Logger } from '../logging/logger';
import { pino } from 'pino';

import { MAX_LENGTH } from '../utils/constants'
import { CodeEditor } from '@jupyterlab/codeeditor';
import { getPreviousLineContents, isLineAComment } from '../utils/utils';
import { Application } from "../application";

const logger: pino.Logger = Logger.getInstance({
    "name": "codewhisperer",
    "component": "extractor"
});

/* This function serialized a notebook cell
* For markdown cell, convert it into python comment per line
* For code cell, send it as it is
* Add a \n between each cell
* Add one more \n after markdown cell, this is to let model know markdown has finished.
*/
function encodeCell(cell: ICellModel): string {
    if (cell.type === 'code') {
        return cell.toJSON()['source'] + '\n';
    } else if (cell.type === 'markdown') {
        const src = cell.toJSON()['source']
        let lines: string[] = []
        if (Array.isArray(src)) {
            lines = src
        } else {
            lines = src.split('\n')
        }
        return '# ' + lines.join('\n# ') + '\n\n';
    }
    return "";
}

export function isNotebookEmpty(panel: NotebookPanel): boolean {
    const cells = panel.content.model.cells;
    for (let i = 0; i < cells.length; i++) {
        const cell = cells.get(i);
        const src = cell.toJSON()['source'] as string
        if (src.trim() !== '') {
            return false
        }
    }
    return true
}

export async function getFileContextFromNotebook(panel: NotebookPanel):
    Promise<{ fileContext: FileContext | undefined; fileContextMetadata: FileContextMetadata; isGlueConnectionType: boolean; gluePrompt: string | undefined; }>
{
    const notebook = panel.content;
    const activeCell = notebook.activeCell;
    let cellMagicCommand = '';
    let isGlueConnectionType = false
    if (Application.getInstance().isMD())
    {
        // Pulling MagicCommand Line which contains Connection Type + Language
        const firstLine = activeCell.editor.getLine(0);
        const lineIsAMagicCommand = typeof firstLine === 'string' && firstLine.startsWith('%%');
        // Do not need to check Connection Type for default cases
        if (lineIsAMagicCommand && firstLine !== '%%local') {
            cellMagicCommand = firstLine;
            // Pull Connection Name from MagicCommand Line
            const pattern = /%%\w+(?:\s+(\S+)|(?:\s+--name\s+(\S+)))/;
            const match = cellMagicCommand.match(pattern);
            const connectionName = match ? (match[1] || match[2] || '') : '';
            // Hit GetConnection API to check if it is Glue Connection using ConnectionName that was pulled from MagicCommand Line
            const response = await fetch(`/jupyterlab/default/api/aws/datazone/connection?name=${connectionName}`);
            const connectionResponse = await response.json();
            if (connectionResponse.type === "SPARK" 
                && 'sparkGlueProperties' in connectionResponse.props
                && (cellMagicCommand.toLowerCase().includes("pyspark") || cellMagicCommand.toLowerCase().includes("spark"))) isGlueConnectionType = true
        }
    }
    const editor = notebook.activeCell?.editor;
    const cellCount = notebook.model.cells.length;
    const cellType = activeCell.model.type;
    const lineNumber = editor?.getCursorPosition().line;
    const cursorOffset = editor?.getOffsetAt(editor.getCursorPosition());
    let fileContext = undefined;
    let gluePrompt = undefined;
    if (editor && activeCell) {
        const cells = notebook.model.cells;
        let left = ``;
        let right = ``;
        for (let i = 0; i < cells.length; i++) {
            const cell = cells.get(i);
            if (i < notebook.activeCellIndex) {
                left += encodeCell(cell);
            } else if (i === notebook.activeCellIndex) {
                const pos = editor.getCursorPosition();
                const offset = editor.getOffsetAt(pos);
                gluePrompt = getGluePrompt(editor);
                const text = editor.model.sharedModel.getSource();
                left += text.substring(0, offset);
                right += text.substring(offset, text.length);
            } else {
                right += encodeCell(cell);
            }
        }
        logger.debug(`Notebook content length - left:${left.slice.length} right:${left.slice.length}`)
        fileContext = {
            leftFileContent: left.slice(-MAX_LENGTH),
            rightFileContent: right.slice(0, MAX_LENGTH),
            filename: panel.context.path.split("/").pop(),
            programmingLanguage: {
                languageName: "python",
            },
        }
    }
    return {
        fileContext: fileContext,
        fileContextMetadata: {
            activeCellIdx: notebook.activeCellIndex,
            cellCount: cellCount,
            cellType: cellType,
            lineNumber: lineNumber,
            cursorOffset: cursorOffset,
        },
        isGlueConnectionType,
        gluePrompt,
    };
}

export function getFileContextFromEditor(
    editor: CodeEditor.IEditor,
    filename: string
): {
    fileContext: FileContext | undefined;
    fileContextMetadata: FileContextMetadata;
} {
    let fileContext = undefined;
    let pos = undefined;
    let offset = undefined;
    if (editor) {
        pos = editor.getCursorPosition();
        offset = editor.getOffsetAt(pos);
        const text = editor.model.sharedModel.getSource();
        const left = text.substring(0, offset);
        const right = text.substring(offset, text.length);
        logger.debug(`File content length - left:${left.slice.length} right:${left.slice.length}`)
        fileContext = {
            leftFileContent: left.slice(-MAX_LENGTH),
            rightFileContent: right.slice(0, MAX_LENGTH),
            filename: filename,
            programmingLanguage: {
                languageName: "python",
            },
        }
    }
    return {
        fileContext: fileContext,
        fileContextMetadata: {
            lineNumber: pos.line,
            cursorOffset: offset,
        }
    };
}

/**
 * @description Returns a string if the last line before the current cursor position
 * is a comment. When passing a prompt to Glue, it will only accept a string.
 */
function getGluePrompt(editor: CodeEditor.IEditor): string | undefined {
    // get the last line of content before current cursor position
    const prevLine = getPreviousLineContents(editor);

    if(isLineAComment(prevLine)) {
        // remove # from text and set as the glue prompt
       return prevLine.replace(/#/g, "").trim()
    } 
}

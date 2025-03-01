import { CodeEditor } from '@jupyterlab/codeeditor';
import { NotebookPanel } from '@jupyterlab/notebook';
import { Inline } from '../inline/inline';
import { Logger } from '../logging/logger';
import pino from 'pino';
import { CodewhispererAutomatedTriggerType } from '../telemetry/telemetry.gen';
import { RecommendationStateHandler } from '../recommendation/recommendationStateHandler';
import { loadState } from "../utils/utils";
import { Application } from "../application";
import { AUTO_SUGGESTION } from "../utils/stateKeys";
import { ISharedText, SourceChange } from "@jupyter/ydoc";

// TODO: Too many states maintained, only enabled is needed
export class AutoTrigger {

  private static instance: AutoTrigger;

  private logger: pino.Logger;

  public static getInstance(): AutoTrigger {
    if (!AutoTrigger.instance) {
      AutoTrigger.instance = new AutoTrigger()
    }
    return AutoTrigger.instance;
  }

  constructor() {
    this.enabled = true
    this.logger = Logger.getInstance({
      "name": "codewhisperer",
      "component": "autotrigger"
    });
    Application.getInstance().loadStateSignal.connect(this.loadState, this)
  }

  public async loadState(sender: any) {
    // auto suggestion
    const autoSuggestionState = await loadState(AUTO_SUGGESTION)

    // autoSuggestionState is undefined if stateDB object is not initialized with the AUTO_SUGGESTION key
    // default to false at the very beginning when autoSuggestionState is undefined
    this.enabled = autoSuggestionState ? !!(autoSuggestionState.enabled) : false;
  }

  public get isAutoSuggestionEnabled(): boolean {
    return this.enabled
  }

  public set isAutoSuggestionEnabled(value: boolean) {
    this.enabled = value
  }

  private filename: string

  public enabled: boolean
  private specialCharacters = new Set<string>(['(', '[', ':', '{']);
  public lastKeyStrokeTime = 0

  private editor: CodeEditor.IEditor;
  private panel: NotebookPanel | undefined;

  public registerListener(editor: CodeEditor.IEditor, panel: NotebookPanel | undefined, filename?: string) {
    this.editor = editor;
    this.panel = panel;
    this.filename = filename

    editor.model.sharedModel.changed.connect(this.editorChangeHandler, this)
  }

  private async editorChangeHandler(sender: ISharedText, args: SourceChange): Promise<void> {
    const now = performance.now();
    RecommendationStateHandler.instance.timeSinceLastDocumentChange = now - this.lastKeyStrokeTime;
    if (!this.enabled) {
      this.lastKeyStrokeTime = now;
      return;
    }

    const { autoTriggerType, triggerCharacter } = this.shouldAutoTrigger(args);
    this.invokeAutoTrigger(this.editor, this.panel, autoTriggerType, triggerCharacter, this.lastKeyStrokeTime);
    this.lastKeyStrokeTime = now;
  }

  public onSwitchToNewCell(editor: CodeEditor.IEditor, panel: NotebookPanel) {
    if (!this.enabled) {
      return
    }
    const cell = panel.content.activeCell
    if (cell.model.type === 'code' && editor.getCursorPosition().line === 0
      && editor.getCursorPosition().column === 0
      && editor.model.sharedModel.source.trim().length === 0) {
      this.invokeAutoTrigger(editor, panel, "NewCell", undefined, this.lastKeyStrokeTime);
    }
  }

  private invokeAutoTrigger(
    editor: CodeEditor.IEditor,
    panel: NotebookPanel | undefined,
    autoTriggerType: CodewhispererAutomatedTriggerType,
    triggerCharacter: string,
    triggerTime: number
  ) {
    this.logger.debug(`invokeAutoTrigger - ${autoTriggerType} - ${triggerCharacter} - ${triggerTime}`)
    if (autoTriggerType) {
      if (panel) {
        // invoke in a Notebook panel
        Inline.getInstance().getCompletionsInNotebookPanel(panel, {
          triggerCharacter: triggerCharacter,
          triggerTime: triggerTime,
          automatedTriggerType: autoTriggerType,
          triggerType: "AutoTrigger",
          language: "ipynb"
        })
      } else if (editor) {
        // invoke in python file
        Inline.getInstance().getCompletionsInEditor(editor, this.filename, {
          triggerCharacter: triggerCharacter,
          triggerTime: triggerTime,
          automatedTriggerType: autoTriggerType,
          triggerType: "AutoTrigger",
          language: "python"
        })
      }
    } else {
      this.logger.debug("Not Valid auto trigger character");
    }

  }

  shouldAutoTrigger(changeArgs: SourceChange): { autoTriggerType: CodewhispererAutomatedTriggerType | undefined, triggerCharacter: string | undefined } {
    let autoTriggerType = undefined;
    let triggerCharacter = undefined;
    if (this.changeIsFromOtherSource(changeArgs)) {
      return { autoTriggerType, triggerCharacter }
    }
    autoTriggerType = this.changeIsNewLine(changeArgs)
    if (!autoTriggerType) {
      autoTriggerType = this.changeIsSpecialCharacter(changeArgs).autoTriggerType;
      triggerCharacter = this.changeIsSpecialCharacter(changeArgs).triggerCharacter;
      if (!autoTriggerType) {
        autoTriggerType = this.changeIsIdleTimeTrigger(changeArgs)
      }
    }
    return { autoTriggerType: autoTriggerType, triggerCharacter: triggerCharacter };
  }

  private changeIsFromOtherSource(changeArgs: SourceChange): boolean {
    // ignore changes which are not from typing
    // this could be from native auto completions
    return changeArgs.sourceChange?.some(change => change.insert?.replace(/ /g, '').length > 1);
  }

  private changeIsNewLine(changeArgs: SourceChange): CodewhispererAutomatedTriggerType | undefined {
    const shouldTrigger = changeArgs.sourceChange?.some(change => change.insert?.trim() === '' && change.insert?.startsWith('\n'));
    if (shouldTrigger) {
      return "Enter";
    } else {
      return undefined;
    }
  }

  private changeIsSpecialCharacter(changeArgs: SourceChange): { autoTriggerType: CodewhispererAutomatedTriggerType | undefined, triggerCharacter: string | undefined } {
    const shouldTrigger = changeArgs.sourceChange?.find(change => !!change.insert && this.specialCharacters.has(change.insert))
    if (shouldTrigger) {
      return { autoTriggerType: "SpecialCharacters", triggerCharacter: shouldTrigger.insert };
    } else {
      return { autoTriggerType: undefined, triggerCharacter: undefined };
    }
  }

  private changeIsIdleTimeTrigger(changeArgs: SourceChange): CodewhispererAutomatedTriggerType | undefined {
    const shouldTrigger = changeArgs.sourceChange?.some(change => performance.now() - this.lastKeyStrokeTime >= 2000 && !!change.insert);
    if (shouldTrigger) {
      return "IdleTime"
    } else {
      return undefined;
    }
  }
}

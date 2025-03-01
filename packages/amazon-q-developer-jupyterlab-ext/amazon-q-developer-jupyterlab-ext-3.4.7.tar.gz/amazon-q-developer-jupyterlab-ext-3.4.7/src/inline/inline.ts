import { CodeEditor } from '@jupyterlab/codeeditor';
import { CodeMirrorEditor } from '@jupyterlab/codemirror';
import { Position } from 'codemirror';
import { NotebookPanel } from "@jupyterlab/notebook";
import { Worker } from '../recommendation/worker';
import { RecommendationsList } from '../client/apiclient';
import { Icons } from '../icons';
import { INLINE_COMPLETION_SHOW_DELAY, SHOW_COMPLETION_TIMER_POLL_PERIOD, SettingIDs } from '../utils/constants';
import { AutoTrigger } from '../autotrigger/autotrigger';
import { RecommendationStateHandler } from '../recommendation/recommendationStateHandler';
import { TriggerMetadata } from '../utils/models';
import { AuthManager } from "../auth/authManager";
import { References } from '../client/codewhispererclient';
import { ReferenceTracker } from '../referencetracker/referencetracker';
import { isNotebookEmpty } from '../recommendation/extractor';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { StateEffect } from '@codemirror/state';

enum InlineSuggestionDispatchType {
  NewCompletion,
  Reload,
  CursorChange,
  Typeahead,
  RemoveCompletion
}

const COMPLETER_ACTIVE_CLASS: string = 'jp-mod-inlinecompleter-active';
const COMPLETER_ENABLED_CLASS: string = 'jp-mod-completer-enabled';

// TODO: The whole class needs to be refactored to utilize listeners/signals so we don't manually give instructions
// to manipulate inline UX everytime.
export class Inline {

    private static instance: Inline;
    public setting: ISettingRegistry.ISettings;

    public visualCueWidget?: HTMLElement;
    private invokePosition: Position;

    // the editor and panel when/where the invocations happen
    private invokeEditor: CodeMirrorEditor;
    private invokePanel: NotebookPanel;

    private completions: RecommendationsList = [];
    private currentIndex: number = 0;
    private typeahead: string = '';
    private showCompletionTimer?: NodeJS.Timer
    private cursorObserver?: MutationObserver = undefined
    private invokeFileName: string = ''

    private visualCueLeftMargin: number = 0
    private showingSuggestion = false
    // the id of the DOM node that hosts the editor
    private previousHostNodeId = ""

    public static getInstance(): Inline {
        if (!Inline.instance) {
            Inline.instance = new Inline()
        }
        return Inline.instance;
    }

    public suggestionsToShow(): boolean {
        return this.completions.length !== 0
    }

    public getTypeAheadAdjustedSuggestionText(): string {
        return this.completions[this.currentIndex].content.substring(this.typeahead.length)
    }

    // TODO: refactor this into CSS
    getVisualCueHtmlElement(): HTMLElement {
        const msg = document.createElement('span')
        const references = this.completions[this.currentIndex].references
        msg.textContent = ` Suggestion ${this.currentIndex + 1} of ${this.completions.length} from Amazon Q${this.getReferenceLogMessage(references)}`
        msg.style.opacity = '0.60';
        msg.style.fontSize = `${<number>this.invokeEditor.getOption('fontSize')-1}px`
        msg.style.whiteSpace = `pre`
        msg.style.color = 'var(--jp-content-font-color1)'
        const icon = Icons.visualCueArrowIcon.element()
        const iconSize = Math.max(this.invokeEditor.lineHeight-4, 4)
        icon.style.width = `${iconSize}px`
        icon.style.height = `${iconSize}px`
        icon.style.opacity = '0.60'
        const visualCue = document.createElement('div')
        visualCue.style.display = 'flex'
        visualCue.style.alignItems = 'center'
        visualCue.appendChild(icon)
        visualCue.appendChild(msg)
        visualCue.className = 'InlineCompletionVisualCue'
        visualCue.style.backgroundColor = 'var(--jp-layout-color1)'
        return visualCue
    }

    private isCurrentFileJupyterNotebook(): boolean {
        return this.invokeEditor !== undefined && this.invokePanel !== undefined
    }

    public addOrUpdateVisualCue() {
        if (!this.invokeEditor) return;
        const { left, top } = this.invokeEditor.cursorCoords(false, "local")
        let visualCueParent: HTMLElement = undefined
        if (this.isCurrentFileJupyterNotebook()) {
            // this is the parent element that allows visual cue to overflow and scroll
            // this parent contains the invokeEditor and a InputAreaPrompt to the left of invokeEditor
            // the left pixel needs to be adjusted due to the existence of InputAreaPrompt
            visualCueParent = this.invokeEditor.host.parentElement.parentElement.parentElement
        } else {
            // for non notebook files, the parent has to be CodeMirror-lines to allow scrollable.
            visualCueParent = this.invokeEditor.host.parentElement.parentElement.querySelector('div.jp-FileEditor') as HTMLElement
        }
        const { top: parentTop, left: parentLeft } = visualCueParent.getBoundingClientRect();
        this.setVisualCueLeftMargin()
        this.visualCueWidget?.remove()
        this.visualCueWidget = this.getVisualCueHtmlElement()
        this.visualCueWidget.style.position = 'absolute'
        this.visualCueWidget.style.left = `${left - parentLeft - 20}px`

        // since CodeMirror-lines does not allow overflow, only when invoking at the first line of non-notebook files
        // the visual Cue has to be at the bottom of ghost text
        if (!this.isCurrentFileJupyterNotebook() && this.invokeEditor.getCursorPosition().line === 0) {
            const lines = this.completions[this.currentIndex].content.split('\n').length
            this.visualCueWidget.style.top = `${top + this.invokeEditor.lineHeight * lines - parentTop}px`
        } else {
            this.visualCueWidget.style.top = `${top - this.invokeEditor.lineHeight - 6 - parentTop}px`
        }
        // make sure the visual cue widget always shows on the top
        this.visualCueWidget.style.zIndex = '10'
        visualCueParent.appendChild(this.visualCueWidget)
    }

    private setVisualCueLeftMargin(){
        if (this.visualCueLeftMargin === 0 && this.isCurrentFileJupyterNotebook()) {
            const inputAreaPromptHtmlElement = document.querySelector(`jp-InputArea-prompt`) as HTMLElement
            if (inputAreaPromptHtmlElement) {
                // 16 is a constant gap between the input area prompt and editor
                this.visualCueLeftMargin = parseFloat(inputAreaPromptHtmlElement.style.width) + 16
            } else {
                // 80px is the margin. This margin is not user configurable. It does not change when browser resizes
                this.visualCueLeftMargin = 80
            }
        }
    }

    /* Widget for the inline completion ghost text
    */
    getElement(text: string): HTMLElement {
        const span = document.createElement('span')
        span.textContent = text
        span.style.opacity = '0.70';
        span.className = 'cw-inline';
        const div = document.createElement('span')
        div.appendChild(span)
        return div
    }

    private getReferenceLogMessage(references: References) {
        if (references.length === 0) {
            return ''
        }
        const msg = `. Reference code under ${references[0].licenseName}. View details in Reference logs.`
        return msg
    }

    /* A function that detects whether a popup is active in the editor.
    */
    private isPopupActive(): boolean {
        // completion popup
        const popup = document.querySelector(`.jp-Notebook .jp-mod-completer-active`) as HTMLElement
        if (popup !== null) {
            return true
        }
        // lsp hover 
        const lspTooltip = document.querySelector(`.lsp-hover`)
        if (lspTooltip !== null) {
            return true
        }
        return false
    }

    private onReceiveListener(sender: any, value: RecommendationsList) {
        if (!this.invokeEditor) {
            this.removeCompletion()
            return
        } else {
            if (this.completions.length === 0 && this.invokePosition) {
                // only update typeAheadLength if this is the first invocation
                const pos = this.invokeEditor.getCursorPosition();
                const cmEditor = (this.invokeEditor as CodeMirrorEditor);
                const newPos = { line: pos.line, ch: pos.column };
                const typeAheadOnFirstCompletion = cmEditor.getRange(this.invokePosition, newPos);
                RecommendationStateHandler.instance.typeAheadLength = typeAheadOnFirstCompletion.length;
            }
        }

        if (value.length > 0) {
            value.forEach(i => {
                if (i.content.length > 0) {
                    this.completions.push(i)
                }
            })
        }

        if (this.isPopupActive()) {
            return
        }
        // show first recommendation
        if (!this.isInlineSessionActive()) {
            if (this.completions.length === 0) {
                return
            }
            let text = this.completions[0].content
            this.currentIndex = 0
            if (this.invokeEditor) {
                this.startShowCompletionTimer(text)
            }
        }
        this.dispatchEvent(InlineSuggestionDispatchType.NewCompletion);
    }

    private startShowCompletionTimer(text: string) {
        if (this.showCompletionTimer) {
            return
        }
        this.showCompletionTimer = setInterval(() => {
            const delay = performance.now() - AutoTrigger.getInstance().lastKeyStrokeTime
            if (delay < INLINE_COMPLETION_SHOW_DELAY) {
                return
            }
            if (!this.invokeEditor) {
                return
            }
            try {
                const showed = this.showCompletion(this.invokeEditor, text)
                if (showed) {
                    // passing `this` so bind is not needed
                    this.invokeEditor?.model.selections.changed.connect(this.onCursorChange, this)
                    
                    // make sure there is always one focus out event listener
                    this.invokeEditor?.host.removeEventListener('focusout', () => {
                        this.onFocusOut()
                    })
                    this.invokeEditor?.host.addEventListener('focusout', () => {
                        this.onFocusOut()
                    })
                }
            } finally {
                if (this.showCompletionTimer) {
                    clearInterval(this.showCompletionTimer)
                    this.showCompletionTimer = undefined
                }
            }
        }, SHOW_COMPLETION_TIMER_POLL_PERIOD)
    }

    public async getCompletionsInNotebookPanel(panel: NotebookPanel, triggerMetadata: TriggerMetadata) {
        if (this.isInlineSessionActive()) {
            return
        }
        this.invokePanel = panel
        this.invokeEditor = this.invokePanel?.content.activeCell?.editor as CodeMirrorEditor;
        this.invokeFileName = this.invokePanel.context.path.split("/").pop()
        if (this.canInvokeRecommendation()) {
            this.invokePosition = { line: this.invokeEditor.getCursorPosition().line, ch: this.invokeEditor.getCursorPosition().column }
            Worker.getInstance().getCompletionsPaginatedInNotebookPanel(panel, triggerMetadata);
            Worker.getInstance().receivedResponseSignal.connect(this.onReceiveListener, this)
        }
    }

    public async getCompletionsInEditor(editor: CodeEditor.IEditor, filename: string, triggerMetadata: TriggerMetadata) {
        if (this.isInlineSessionActive()) {
            return
        }
        this.invokeEditor = editor as CodeMirrorEditor;
        this.invokeFileName = filename
        if (this.canInvokeRecommendation()) {
            this.invokePosition = { line: editor.getCursorPosition().line, ch: editor.getCursorPosition().column }
            Worker.getInstance().getCompletionsPaginatedInEditor(editor, filename, triggerMetadata);
            Worker.getInstance().receivedResponseSignal.connect(this.onReceiveListener, this)
        }
    }


    /* Returns a boolean that is true only when the current cursor exists but is not a selection
    */
    private currentCursorIsNotASelection(): boolean {
        if (this.invokeEditor) {
            const selection = this.invokeEditor.getSelection()
            return selection.start.line === selection.end.line && selection.start.column === selection.end.column
        }
        return false
    }

    /* Can invoke only when in code cell in Jupyter Notebook and authenticated
    *  Do not invoke in non-python or non-Jupyter Notebook
    *  Only when current cursor is not a selection
    */
    private canInvokeRecommendation(): boolean {
        if (Worker.getInstance().isGetCompletionsRunning) {
            return false
        }
        if (!AuthManager.getInstance().isAuthenticated()) {
            return false
        }
        if (!(this.invokeFileName.endsWith('.py') || this.invokeFileName.endsWith('.ipynb'))) {
            return false
        }
        if (this.invokePanel) {
            const cell = this.invokePanel.content.activeCell
            if (isNotebookEmpty(this.invokePanel)) {
                return false
            }
            return this.currentCursorIsNotASelection() && cell !== undefined && cell.model.type === "code"
        } else {
            return this.currentCursorIsNotASelection()
        }

    }

    public onFocusOut() {
        this.removeCompletion()
    }

    public showNext() {
        if (this.isInlineSessionActive()) {
            this.updateCurrentIndexNext()
            this.reloadSuggestionWidget()
        }
    }

    private updateCurrentIndexNext() {
        for (let i = 0; i < this.completions.length; i++) {
            this.currentIndex = (this.currentIndex + 1) % this.completions.length

            // we will only skip the current index and update it 
            // if the corresponding recommendation doesn't match typeahead
            if (this.completions[this.currentIndex].content.startsWith(this.typeahead)) {
                return
            }
        }
    }

    private updateCurrentIndexPrev() {
        for (let i = 0; i < this.completions.length; i++) {
            this.currentIndex = (this.completions.length + this.currentIndex - 1) % this.completions.length

            // we will only skip the current index and update it 
            // if the corresponding recommendation doesn't match typeahead
            if (this.completions[this.currentIndex].content.startsWith(this.typeahead)) {
                return
            }
        }
    }

    private reloadSuggestionWidget() {
        RecommendationStateHandler.instance.setSuggestionState(this.currentIndex, "Showed");
        this.adjustCursorSizeAndPosition(this.invokeEditor)
        this.dispatchEvent(InlineSuggestionDispatchType.Reload);
    }

    /* By default, the visual cue shows on hover
    *  When there is code reference, visual cue always shows
    */
    // public setupVisualCueOnHover(left: number, top: number){
    //     if (this.decorationAdded) {
    //         if (this.completions[this.currentIndex].references !== undefined && this.completions[this.currentIndex].references.length > 0) {
    //             this.addOrUpdateVisualCue(left, top)
    //         } else {
    //             this.visualCueWidget?.remove()
    //         }
    //     }
    // }


    public showPrev() {
        if (this.isInlineSessionActive()) {
            this.updateCurrentIndexPrev()
            this.reloadSuggestionWidget()
        }
    }

    private onCursorChange() {
        if (this.invokeEditor && this.invokePosition && this.showingSuggestion) {
            const pos = this.invokeEditor.getCursorPosition();
            // Clear completion if the cursor is not at same line or it is on the left of typeahead
            if (pos.line !== this.invokePosition.line || (pos.column < this.invokePosition.ch + this.typeahead.length && pos.line === this.invokePosition.line)) {
                this.removeCompletion()
                return
            }
            const cmEditor = (this.invokeEditor as CodeMirrorEditor)
            const newPos = { line: pos.line, ch: pos.column }
            this.typeahead = cmEditor.getRange(this.invokePosition, newPos)
            const text = this.completions[this.currentIndex].content
            if (text.startsWith(this.typeahead)) {
                this.adjustCursorSizeAndPosition(this.invokeEditor);
                this.dispatchEvent(InlineSuggestionDispatchType.CursorChange);
            } else {
                this.removeCompletion()
            }
        }
    }

    /* Shows a completion string in the Editor view
    *  Returns true if shows successfully, false otherwise
    */
    public showCompletion(editor: CodeEditor.IEditor, text: string): boolean {
        const pos = editor.getCursorPosition();
        if (this.invokePosition === undefined) {
            this.removeCompletion()
            return false
        }
        if (pos.line !== this.invokePosition.line || (pos.column < this.invokePosition.ch && pos.line === this.invokePosition.line)) {
            this.removeCompletion()
            return false
        }

        const cmEditor = (editor as CodeMirrorEditor)
        if (!cmEditor.hasFocus()) {
            this.removeCompletion()
            return false
        }

        const newPos = { line: pos.line, ch: pos.column }
        this.typeahead = cmEditor.getRange(this.invokePosition, newPos)
        if (text.startsWith(this.typeahead)) {
            this.showingSuggestion = true
            this.dispatchEvent(InlineSuggestionDispatchType.Typeahead);
            if (this.invokeEditor) {
              this.invokeEditor.host.classList.add(COMPLETER_ACTIVE_CLASS);
              this.invokeEditor.host.classList.add(COMPLETER_ENABLED_CLASS);
              // We need to use id to increase the specificity of our Tab keybinding
              // so that JL doesn't override with theirs.
              this.previousHostNodeId = this.invokeEditor.host.id;
              this.invokeEditor.host.id = COMPLETER_ACTIVE_CLASS;
            }
            RecommendationStateHandler.instance.setSuggestionState(this.currentIndex, "Showed");
            this.adjustCursorSizeAndPosition(editor)
            return true
        } else {
            this.removeCompletion()
            return false
        }
    }


    /* This function resolves 2 bugs from CodeMirrorEditor
    * 1. Its cursor height can increase when there is a multi-line recommendation
    * 2. Its cursor left can move to leftmost of the line if ghost text is inserted right to non-whitespace characters.
    * 3. Its cursor top can move to the middle line of multi-line ghost text if ghost text is inserted right to non-whitespace characters in 
    *    a non-Jupyter Notebook. 
    */
    private adjustCursorSizeAndPosition(editor: CodeEditor.IEditor) {
        const cursor = document.querySelector(`div.CodeMirror-cursor`) as HTMLElement
        const cursorHeight = `${editor.lineHeight}px`
        if (cursor) {
            cursor.style.height = cursorHeight
            // when CodeMirror forces cursor to the left, use the correct logical position of JL Editor
            // to set the CSS of the cursor left pixels
            if (this.invokeEditor && parseFloat(cursor.style.left) < this.invokeEditor.charWidth) {
                const newLeft = parseFloat(cursor.style.left) + this.invokeEditor.getCursorPosition().column * this.invokeEditor.charWidth
                cursor.style.left = `${newLeft}px`
            }
            if (!this.isCurrentFileJupyterNotebook() && this.invokeEditor) {
                const cursorCssTop = parseFloat(cursor.style.top)
                const cursorLogicTop = this.invokeEditor.getCursorPosition().line * this.invokeEditor.lineHeight
                if (cursorCssTop !== cursorLogicTop) {
                    cursor.style.top = `${cursorLogicTop}px`
                }
            }
        }

        // Callback function to execute when CodeMirror cursor size overflows
        const callback = (mutationList: MutationRecord[], observer: any) => {
            for (const mutation of mutationList) {
                if (mutation.type === "childList" && mutation.addedNodes.length > 0) {
                    const node = mutation.addedNodes[0] as HTMLElement
                    if (node.className === `CodeMirror-cursor`) {
                        if (node.style.height !== cursorHeight) {
                            node.style.height = cursorHeight
                        }
                        // when CodeMirror forces cursor to the left, use the correct logical position of JL Editor
                        // to set the CSS of the cursor left pixels
                        if (this.invokeEditor && parseFloat(node.style.left) < this.invokeEditor.charWidth) {
                            const newLeft = parseFloat(node.style.left) + this.invokeEditor.getCursorPosition().column * this.invokeEditor.charWidth
                            node.style.left = `${newLeft}px`
                        }
                        if (!this.isCurrentFileJupyterNotebook() && this.invokeEditor) {
                            const cursorCssTop = parseFloat(cursor.style.top)
                            const cursorLogicTop = this.invokeEditor.getCursorPosition().line * this.invokeEditor.lineHeight
                            if (cursorCssTop !== cursorLogicTop) {
                                cursor.style.top = `${cursorLogicTop}px`
                            }
                        }
                    }
                }
            }
        };

        // Create an observer instance linked to the callback function
        this.cursorObserver = new MutationObserver(callback);
        this.cursorObserver.observe(document, { attributes: true, childList: true, subtree: true })
    }

    public removeCompletion() {
        Worker.getInstance().isInvocationCancelled = true;
        this.visualCueWidget?.remove()
        this.visualCueWidget = undefined
        this.visualCueLeftMargin = 0
        this.invokeEditor?.model.selections.changed.disconnect(this.onCursorChange, this)
        if (this.invokeEditor) {
          this.invokeEditor.host.classList.remove(COMPLETER_ACTIVE_CLASS);
          this.invokeEditor.host.classList.remove(COMPLETER_ENABLED_CLASS);
          this.invokeEditor.host.id = this.previousHostNodeId;
          this.previousHostNodeId = "";
        }
        
        if (!Worker.getInstance().isGetCompletionsRunning) {
            RecommendationStateHandler.instance.rejectRecommendationSignal.emit(-1);
        }
        this.dispatchEvent(InlineSuggestionDispatchType.RemoveCompletion)

        this.cursorObserver?.disconnect()
        this.cursorObserver = undefined
        this.completions = []
        this.currentIndex = 0
        this.typeahead = ''
        this.invokePosition = undefined
        this.showingSuggestion = false
        this.invokeEditor = undefined
        this.invokePanel = undefined
        this.invokeFileName = ''
        if (this.showCompletionTimer) {
            clearInterval(this.showCompletionTimer)
            this.showCompletionTimer = undefined
        }
        this.forceClearGhostText()
    }

    // Sometimes the this.marker.clear() method
    // cannot remove the marker if user changes the Tab
    // this is the force clear the inline completion ghost text marker.
    private async forceClearGhostText() {
        const doc = document.querySelector('span.cw-inline') as HTMLElement
        if (doc) {
            doc.remove()
        }
    }


    public isInlineSessionActive(): boolean {
        return this.invokeEditor !== undefined && this.showingSuggestion
    }

    public async acceptCompletion(editor?: CodeEditor.IEditor) {
        if (!this.isInlineSessionActive()) {
            return
        }
        if (!editor) {
            editor = this.invokeEditor
        }
        // this cursor change should not trigger the cursor change listener
        this.invokeEditor?.model.selections.changed.disconnect(this.onCursorChange, this)
        const pos = editor.getCursorPosition();

        // prevent JL native completer trigger after document code change
        const jlCompleterEnabled = this.setting.get(SettingIDs.autoCompletion).composite as boolean
        if (jlCompleterEnabled) {
            await this.setting.set(SettingIDs.autoCompletion, false)
        }
        try {
            editor.setSelection({ start: pos, end: pos })
            editor.replaceSelection(this.getTypeAheadAdjustedSuggestionText())

            Worker.getInstance().isInvocationCancelled = true;
            RecommendationStateHandler.instance.acceptRecommendationSignal.emit(this.currentIndex);

            const references = this.completions[this.currentIndex].references
            for (const reference of references) {
                const span = reference.recommendationContentSpan
                const completion = this.completions[this.currentIndex].content
                const referenceCode = completion.substring(span.start, span.end)
                // this.invokePosition is 0-indexed, hence line number is this.invokePosition + 1
                // #Lines in code snippet => completion.substring(0, span.start).split('\n').length - 1 as the array length will
                // one more than the number of lines in the snippet
                const startline = this.invokePosition.line + 1 + completion.substring(0, span.start).split('\n').length - 1
                // End line is the start line + the number of lines in the snippet - 1 (exclude the last line)
                const endline = startline + (referenceCode.split('\n').length - 1) - 1
                ReferenceTracker.getInstance().logReference(
                    referenceCode, 
                    reference.licenseName, 
                    reference.repository, 
                    reference.url,
                    this.invokeFileName,
                    startline.toString(), 
                    endline.toString()
                )
            }
            this.removeCompletion()
        } finally {
            // revert settings change
            if (jlCompleterEnabled) {
                await this.setting.set(SettingIDs.autoCompletion, true)
            }
        }
    }

    public onEditorChange(editor: CodeEditor.IEditor) {
        this.removeCompletion()
    }

    private dispatchEvent(type: InlineSuggestionDispatchType): void {
      this.invokeEditor?.editor.dispatch({
        effects: StateEffect.define<InlineSuggestionDispatchType>().of(type),
      });
    }

}

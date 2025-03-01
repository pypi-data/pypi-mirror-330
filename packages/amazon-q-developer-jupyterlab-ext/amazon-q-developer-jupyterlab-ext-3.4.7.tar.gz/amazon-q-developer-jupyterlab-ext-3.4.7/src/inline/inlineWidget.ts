import { EditorView, WidgetType } from '@codemirror/view';
import { Inline } from './inline';

// @ts-ignore
export class InlineCodeWhispererWidget extends WidgetType {

  private contentSpan: HTMLSpanElement

  private get inline(): Inline {
    return Inline.getInstance();
  }

  constructor() {
    super()
  }

  toDOM(view: EditorView): HTMLElement {
    if (!this.contentSpan) {
      this.contentSpan = document.createElement('span')
      this.contentSpan.style.opacity = '0.70';
      this.contentSpan.className = 'cw-inline';
    }
    this.contentSpan.textContent = this.inline.getTypeAheadAdjustedSuggestionText()
    const div = document.createElement('span')
    div.appendChild(this.contentSpan)
    div.addEventListener('mouseenter', this.handleMouseEnter);
    div.addEventListener('mouseleave', this.handleMouseLeave);
    setTimeout(() => {
      this.inline.addOrUpdateVisualCue();
    });
    return div
  }

  public updateContent(content: string) {
    this.contentSpan.textContent = content;
  }

  public destroy(dom: HTMLElement): void {
    dom.removeEventListener('mouseenter', this.handleMouseEnter);
    dom.removeEventListener('mouseleave', this.handleMouseLeave);
    super.destroy(dom);
  }

  private handleMouseEnter = () => {
    this.inline.addOrUpdateVisualCue();
  }

  private handleMouseLeave = () => {
    this.inline.visualCueWidget?.remove();
  }

  //TODO: can use updateDOM to update the suggestionText

  ignoreEvent(event: Event): boolean {
    return false;
  }
}

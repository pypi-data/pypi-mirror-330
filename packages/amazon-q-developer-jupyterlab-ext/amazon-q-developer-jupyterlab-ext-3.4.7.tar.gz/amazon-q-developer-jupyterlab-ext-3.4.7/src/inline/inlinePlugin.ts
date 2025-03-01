import { ViewPlugin, DecorationSet, Decoration, ViewUpdate } from '@codemirror/view';
import { Inline } from './inline';
import { InlineCodeWhispererWidget } from './inlineWidget';

export const myInlinePlugin = ViewPlugin.fromClass(class {
  decorations: DecorationSet

  constructor() {
      this.decorations = Decoration.none
  }

  inlineSuggestionDecoration(pos: number) {
      const decoration = Decoration.widget({
          widget: new InlineCodeWhispererWidget(),
          side: 1,
      });
      return Decoration.set([decoration.range(pos)]);
  }

  update(update: ViewUpdate) {
      if (Inline.getInstance().suggestionsToShow()) {
        this.decorations = this.inlineSuggestionDecoration(
          update.view.state.selection.main.head
        )
      }
      else {
        this.decorations = Decoration.none
      }
  }
}, {
  decorations: v => v.decorations
});

import { MainAreaWidget } from "@jupyterlab/apputils";
import { IHtmlLog, ILogger, ITextLog, LogConsolePanel, LoggerRegistry } from "@jupyterlab/logconsole";
import { IRenderMimeRegistry } from "@jupyterlab/rendermime";
import { listIcon } from '@jupyterlab/ui-components';

export const LOG_SOURCE = 'Q Developer Reference Logs';

export class ReferenceTracker {
  private static instance: ReferenceTracker;
  private logConsolePanel: LogConsolePanel;
  private logConsoleWidget: MainAreaWidget<LogConsolePanel>;
  private logger: ILogger;
  private loggerRegistry: LoggerRegistry;

  public static createInstance(rendermime: IRenderMimeRegistry): ReferenceTracker {
    if (!ReferenceTracker.instance) {
      ReferenceTracker.instance = new ReferenceTracker(rendermime);
    }
    return ReferenceTracker.instance;
  }

  public static getInstance(): ReferenceTracker {
    return ReferenceTracker.instance;
  }

  public createReferenceLogWidget() {
    this.logConsolePanel = new LogConsolePanel(this.loggerRegistry);
    this.logConsolePanel.source = LOG_SOURCE;

    this.logConsoleWidget = new MainAreaWidget<LogConsolePanel>({
      content: this.logConsolePanel,
    });
    this.logConsoleWidget.title.icon = listIcon;

    this.logConsoleWidget.disposed.connect(() => {
      this.logConsoleWidget = null;
      this.logConsolePanel = null;
    });

    this.logConsolePanel.activate();
    this.logger = this.loggerRegistry.getLogger(LOG_SOURCE);
    this.logConsolePanel.logger.level = 'debug';

    this.logConsoleWidget.update();
    return this.logConsoleWidget;
  }

  public disposeReferenceLogWidget() {
    if (this.logConsoleWidget) {
      this.logConsoleWidget.dispose();
    }
  }

  public isReferenceLogDisposed() {
    return this.logConsoleWidget === null;
  }

  private constructor(rendermime: IRenderMimeRegistry) {
    this.loggerRegistry = new LoggerRegistry({
      defaultRendermime: rendermime,
      maxLength: 1000,
    });
    this.createReferenceLogWidget();
    this.logger.clear();
    this.logConsoleWidget = null;
  }

  public logInfo(message: string) {
    const msg: ITextLog = {
      type: 'text',
      level: 'info',
      data: message,
    };
    this.logger.log(msg);
  }

  public logDebug(message: string) {
    const msg: ITextLog = {
      type: 'text',
      level: 'debug',
      data: message,
    };
    this.logger.log(msg);
  }

  public logError(message: string) {
    const msg: ITextLog = {
      type: 'text',
      level: 'error',
      data: message,
    };
    this.logger.log(msg);
  }

  private escapeHtml(unsafe: string): string {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
  }

  public logReference(code: string, license: string, repo: string, url: string, filepath: string, startLine: string, endLine: string) {
    const msg: IHtmlLog = {
      type: 'html',
      level: 'debug',
      data: `Accepted recommendation with code
      <br><code>${this.escapeHtml(code)}</code><br/> provided with reference under <b><i>${this.escapeHtml(license)}</i></b>
      from repository <a href=${this.escapeHtml(url)}>${this.escapeHtml(repo)}</a>. Added to ${this.escapeHtml(filepath)} (lines from ${this.escapeHtml(startLine)} to ${this.escapeHtml(endLine)}). <br>`
    };
    this.logger.log(msg);
  }
}
  


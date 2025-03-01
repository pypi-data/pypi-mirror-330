/*!
 * Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
import { JupyterFrontEnd, JupyterFrontEndPlugin, } from '@jupyterlab/application';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { IEditorTracker } from '@jupyterlab/fileeditor'
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IStateDB } from '@jupyterlab/statedb';
import { IStatusBar } from '@jupyterlab/statusbar';
import { DocumentWidget } from '@jupyterlab/docregistry';
import { ReadonlyJSONObject, UUID } from '@lumino/coreutils';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { EditorExtensionRegistry, IEditorExtensionRegistry } from '@jupyterlab/codemirror';
import { CodeEditorWrapper } from '@jupyterlab/codeeditor';
import { Worker } from './recommendation/worker'
import { Inline } from './inline/inline';
import { myInlinePlugin } from './inline/inlinePlugin';
import { AutoTrigger } from './autotrigger/autotrigger';
import { Telemetry } from './telemetry/telemetry';
import StatusBarWidget from "./statusbar/statusbarwidget";
import { AuthManager } from "./auth/authManager";
import { Logger } from './logging/logger';
import { Application } from "./application";
import { ReferenceTracker } from './referencetracker/referencetracker';
import { COMPLETER_PLUGIN_ID, CommandIDs, NEW_CELL_AUTO_TRIGGER_DELAY_IN_MS, PLUGIN_ID, SettingIDs } from './utils/constants';
import { Keybindings } from './keybindings/keybindings';
import { EditorView } from '@codemirror/view';
import { Prec } from '@codemirror/state';
import { IThemeManager, ThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [ISettingRegistry, INotebookTracker, IEditorTracker, IStateDB, IStatusBar, IRenderMimeRegistry, IEditorExtensionRegistry, IThemeManager],
  activate: async (
    app: JupyterFrontEnd,
    settings: ISettingRegistry,
    notebooks: INotebookTracker,
    editorTracker: IEditorTracker,
    state: IStateDB,
    statusBar: IStatusBar,
    rendermime: IRenderMimeRegistry,
    editorExtensionRegistry: EditorExtensionRegistry,
    themeManager: ThemeManager,
  ) => {
    const logger = Logger.getInstance({
      "name": "codewhisperer",
    });

    // This is computed per browser refresh
    const activateStartTime = performance.now()

    /* ClientId is a UUID for identifying unique customers for telemetry. It should be specific to
    *  one installation of codewhisperer extension in a host. IStateDB is used for persistence in an extension.  
    *  See https://github.com/jupyterlab/extension-examples/tree/master/state for more details. 
    */
    app.restored.then(async () => {

      // Get the state of the extension
      state.fetch(PLUGIN_ID).then(value => {
        if (value) {
          Telemetry.clientId = (value as ReadonlyJSONObject)['clientId'] as string;
          logger.debug(`Restored - clientId: ${Telemetry.clientId}`);
        } else {
          // generate uuid for clientId
          Telemetry.clientId = UUID.uuid4();
          // save clientId to state
          state.save(PLUGIN_ID, { "clientId": Telemetry.clientId });
          logger.debug(`Generated - clientId: ${Telemetry.clientId}`);
        }
      });

      const loadSetting = (setting: ISettingRegistry.ISettings) => {
        Application.getInstance().setting = setting;
        Telemetry.getInstance().enableTelemetry(setting.get(SettingIDs.keyTelemetry).composite as boolean);
        Worker.getInstance().setOptOut(!(setting.get(SettingIDs.keyOptOut).composite as boolean));
        Worker.getInstance().setSuggestionsWithCodeReferences(setting.get(SettingIDs.keyReferences).composite as boolean);
        Logger.setLogLevel(setting.get(SettingIDs.keyLogLevel).composite as string);
        Keybindings.getInstance().keyBindings = [...app.commands.keyBindings];
        logger.debug(`Loaded settings`);

        if (Application.getInstance().isJupyterOSS()) return;

        /**
         * Clear environment cache when MD environment has loaded. This allows for 
         * auth mode switching and q enabling / disabling without having to restart
         * the jupyterlab environment. 
         * 
         * How this works: 
         * 1. MD loads JupyterLab and stores auth mode and q enabled values in the local environment.
         * 2. Once values are stored, MD makes a post request to clear_environment_cache, clearing the 
         * cached environment and q_enabled values in this extension.
         * 3. After that post request is made, MD will post a message ("MD_ENVIRONMENT_LOADED") which
         * this extension will use to re-load services, updating the environment based on changes 
         * in the MD environment. 
         * 4. After services have loaded, emit an auth state changed signal to force a re-render of the 
         * widget.
         */
        window.addEventListener("message", async (message) => {
          if(message.data === "MD_ENVIRONMENT_LOADED"){
            await Application.getInstance().loadServices(state, app);
            // emit an auth state changed signal so widget state is refreshed
            AuthManager.getInstance().authStateChangedSignal.emit(null);
          }
        })

        const styleElement = document.createElement('style');

        styleElement.textContent = `
          #jp-SettingsEditor-amazon-q-developer-jupyterlab-ext\\\:completer > div:first-of-type {
            display: none !important;
          }

          #jp-SettingsEditor-amazon-q-developer-jupyterlab-ext\\\:completer > div:first-of-type > input {
            pointer-events: none;
            opacity: 0.5;
          }
        `;
        document.head.appendChild(styleElement);
      }

      Promise.all([app.restored, settings.load(PLUGIN_ID), settings.load(COMPLETER_PLUGIN_ID)])
        .then(([, setting, completerSetting]) => {
          loadSetting(setting);
          setting.changed.connect(loadSetting);
          Inline.getInstance().setting = completerSetting;
        })
      
      


      Application.getInstance().loadStateSignal.emit(null);
      await AuthManager.getInstance().refresh();

      const statusBarWidgetProps = {
        themeManager,
      }
      const statusBarWidget = new StatusBarWidget(statusBarWidgetProps);
      statusBar.registerStatusItem("aws-codewhisperer:status-bar-widget", {
        item: statusBarWidget,
        align: 'left',
        isActive: () => true,
        rank: 100,
      });
    });

    await Application.getInstance().loadServices(state, app);

    /* A listener that triggers whenever there is a new Notebook panel
    * This is to 
      1. register a listener for auto trigger in Notebook files
      2. Setup kernel completion & completion connectors using a merge connector.
    */
    notebooks.widgetAdded.connect(async (sender: INotebookTracker, panel: NotebookPanel) => {
      logger.debug(`Notebookpanel added - ${panel.id}`);
      await panel.revealed;
      let editor = panel.content.activeCell?.editor ?? null;

      const updateConnector = async () => {
        logger.debug(`Notebookpanel updated - ${panel.id}`);

        await panel.content.activeCell.ready;
        editor = panel.content.activeCell?.editor ?? null;
        if (!editor) return;
        // this connector contains native & cw suggestions  
        AutoTrigger.getInstance().registerListener(editor, panel);

        // briefly after browser refresh finishes, enable the NewCell auto trigger
        // browser refresh will send false signal of NewCell auto trigger
        const currentWidget = app.shell.currentWidget
        if (currentWidget && currentWidget instanceof NotebookPanel && performance.now() - activateStartTime > NEW_CELL_AUTO_TRIGGER_DELAY_IN_MS) {
          AutoTrigger.getInstance().onSwitchToNewCell(editor, panel)
        }
      };
      // Update the handler whenever the prompt or session changes
      panel.content.activeCellChanged.connect(() => updateConnector(), this);
      panel.sessionContext.sessionChanged.connect(() => updateConnector(), this);

      // clear suggestion when panel lost focus
      const onPanelFocusOut = () => {
        logger.debug(`Notebookpanel focus out - ${panel.id}`);
        Inline.getInstance().onFocusOut()
      }
      // ensure only one listener is active at a time
      panel.node.removeEventListener('focusout', onPanelFocusOut)
      panel.node.addEventListener('focusout', onPanelFocusOut)
    }, this);

    /* A listener that triggers whenever there is a new editor other than Notebook panel
    * This is to register a listener for auto trigger in python files
    */
    editorTracker.widgetAdded.connect((sender: any, e) => {
      logger.debug(`Editor added - ${e.id}`);
      e.content.editor.host.addEventListener('focusin', () => {
        const filename = e.context.path.split('/').pop()
        AutoTrigger.getInstance().registerListener(e.content.editor, undefined, filename);
      })
    })

    if (!app.commands.hasCommand(CommandIDs.login)) {
      logger.debug("Executing command : login")
      app.commands.addCommand(CommandIDs.login, {
        execute: async () => {
          await AuthManager.getInstance().login()
        },
      });
    }

    editorExtensionRegistry.addExtension(
      {
        name: 'cw-inline-extension',
        factory: () => EditorExtensionRegistry.createConfigurableExtension(() =>
          myInlinePlugin
        )
      }
    ) 

    if (!app.commands.hasCommand(CommandIDs.invokeInline)) {
      app.commands.addCommand(CommandIDs.invokeInline, {
        execute: async () => {
          logger.debug("Executing command : invokeInline")
          const currentWidget = app.shell.currentWidget
          if (currentWidget && currentWidget instanceof NotebookPanel) {
            logger.debug("Invoking Inline in NotebookPanel")
            await Inline.getInstance().getCompletionsInNotebookPanel(currentWidget as NotebookPanel, {
              triggerType: "OnDemand",
              triggerCharacter: undefined,
              automatedTriggerType: undefined,
              language: "ipynb",
              triggerTime: performance.now(),
            })
          } else if (currentWidget && currentWidget instanceof DocumentWidget) {
            logger.debug("Invoking Inline in Document")
            const doc = currentWidget as DocumentWidget<CodeEditorWrapper>
            const filename = doc.context.path.split('/').pop()
            await Inline.getInstance().getCompletionsInEditor(doc.content.editor, filename, {
              triggerType: "OnDemand",
              triggerCharacter: undefined,
              automatedTriggerType: undefined,
              language: "python",
              triggerTime: performance.now(),
            })
          } else {
            logger.error("Notebook or Editor not found")
          }
        },
      });
    }

    if (!app.commands.hasCommand(CommandIDs.rejectInline)) {
      logger.debug("Executing command : rejectInline")
      app.commands.addCommand(CommandIDs.rejectInline, {
        execute: async () => {
          Inline.getInstance().removeCompletion()
        },
      });
    }

    if (!app.commands.hasCommand(CommandIDs.acceptInline)) {
      logger.debug("Executing command : acceptInline")
      app.commands.addCommand(CommandIDs.acceptInline, {
        execute: async () => {
          await Inline.getInstance().acceptCompletion()
        },
      });
    }

    // Override the default CodeMirror down and up buttons
    // Only when cw inline completion active
    const onKeyDown = EditorView.domEventHandlers({
      keydown: (event: KeyboardEvent, view: EditorView) => {
        if (view.dom.querySelector('.cw-inline') && (event.code === "ArrowDown"  || event.code === "ArrowUp")) {
          if (event.code === "ArrowDown") {
            Inline.getInstance().showNext();
          }
          if (event.code === "ArrowUp") {
            Inline.getInstance().showPrev();
          }
          return true
        }
        return false
      }
    });
    editorExtensionRegistry.addExtension({
      name: 'amazonq-keybinding-override',
      factory: () =>
        EditorExtensionRegistry.createConfigurableExtension(value => Prec.highest(onKeyDown))
    })

    ReferenceTracker.createInstance(rendermime);

    Telemetry.init();

    logger.info('JupyterLab Q Developer extension is activated!');
  },
};

export default extension;

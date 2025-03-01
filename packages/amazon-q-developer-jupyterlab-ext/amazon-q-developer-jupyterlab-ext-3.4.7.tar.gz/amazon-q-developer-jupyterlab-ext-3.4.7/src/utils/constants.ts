/**
 * The metric name that will be used to send telemetry event data.
 */
export const TELEMETRY_SERVICE_INVOCATION_METRIC_NAME = "codewhisperer_serviceInvocation";
export const TELEMETRY_USER_DECISION_METRIC_NAME = "codewhisperer_userDecision";
export const TELEMETRY_USER_TRIGGER_DECISION_METRIC_NAME = "codewhisperer_userTriggerDecision";

export const LEARN_MORE_NOTIFICATION_URL = "https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html";
// TODO : Update this to CodeWhisperer URL after finalizing name
export const UPDATE_NOTIFICATION_URL = "https://pypi.org/project/amazon-q-developer-jupyterlab-ext/";

export const CWSPR_DOCUMENTATION = "https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html"

export const MAX_LENGTH = 10240;

export const MAX_RECOMMENDATIONS = 5;

export const MAX_PAGINATION_CALLS = 10;

export const AWS_BUILDER_ID_START_URL = "https://view.awsapps.com/start";

//  delay in ms when showing suggestion before user last keystroke input
export const INLINE_COMPLETION_SHOW_DELAY = 250;

// the poll period of show completion timer in ms
export const SHOW_COMPLETION_TIMER_POLL_PERIOD = 25;

export const NEW_CELL_AUTO_TRIGGER_DELAY_IN_MS = 10000;
export const NOTIFICATION_TEXT_LIMIT = 140;

export const EXPIRATION_BUFFER_IN_SECONDS = 60;

export const CONTENTS_ENDPOINT = 'api/contents'
export const AWS_DIRECTORY = '.aws';
export const AMAZON_Q_DIRECTORY = AWS_DIRECTORY + '/amazon_q';

/**
 * The command IDs used by the console plugin.
 */
export namespace CommandIDs {
    export const login = 'codewhisperer:login';
    export const invokeInline = 'codewhisperer:invoke-inline';
    export const rejectInline = 'codewhisperer:reject-inline';
    export const acceptInline = 'codewhisperer:accept-inline';
    export const startCodeWhisperer = 'codewhisperer:start';
    export const cancelLogin = 'codewhisperer:cancel-login';
    export const openDocumentation = 'codewhisperer:documentation';
    export const pauseAutoSuggestion = 'codewhisperer:pause-auto-suggestion';
    export const resumeAutoSuggestion = 'codewhisperer:resume-auto-suggestion';
    export const openReferenceLog = 'codewhisperer:open-reference-log';
    export const signOut = 'codewhisperer:sign-out';
    export const keyShortcutTitle = 'codewhisperer:key-shortcut-title';
    export const keyShortcutAccept = 'codewhisperer:key-shortcut-accept';
    export const keyShortcutManualTrigger = 'codewhisperer:key-shortcut-manual-trigger';
    export const keyShortcutNavigate = 'codewhisperer:key-shortcut-navigate';
    export const keyShortcutReject = 'codewhisperer:key-shortcut-reject';
    export const toggleTelemetry = 'codewhisperer:toggle-telemetry';
    export const toggleCodeReferences = 'codewhisperer:toggle-code-references';
    export const openCustomizationSettings = 'codewhisperer:open-customization-settings';
  }
  
  export const PLUGIN_ID = 'amazon-q-developer-jupyterlab-ext:completer';
  export const COMPLETER_PLUGIN_ID = '@jupyterlab/completer-extension:manager';

export const MESSAGE_TO_CMD_ID_MAP = {
    "codewhisperer_key_shortcut_accept": CommandIDs.acceptInline,
    "codewhisperer_key_shortcut_manual_trigger": CommandIDs.invokeInline,
    "codewhisperer_key_shortcut_reject": CommandIDs.rejectInline,
}

export enum HttpStatusCode {
    OK = 200,
    NOT_FOUND = 404,
}

export namespace SettingIDs {
    export const keyOptOut = 'shareCodeWhispererContentWithAWS'
    export const keyTelemetry = 'codeWhispererTelemetry'
    export const keyReferences = 'suggestionsWithCodeReferences'
    export const keyLogLevel = 'codeWhispererLogLevel'
    export const autoCompletion = 'autoCompletion'
}

export enum AuthMode {
	SSO = 'SSO',
	IAM = 'IAM',
}

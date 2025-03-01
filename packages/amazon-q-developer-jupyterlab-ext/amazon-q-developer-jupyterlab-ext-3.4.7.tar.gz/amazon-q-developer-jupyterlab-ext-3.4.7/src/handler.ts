import { URLExt } from '@jupyterlab/coreutils';

import { ServerConnection } from '@jupyterlab/services';
import { NotificationManager } from "./notifications/notifications";
import { message } from "./messages";
import { HttpStatusCode } from "./utils/constants";
import { LEARN_MORE_NOTIFICATION_URL } from "./utils/constants";

/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
export async function requestAPI<T>(
  endPoint = '',
  init: RequestInit = {}
): Promise<Response> {
  // Make request to Jupyter API
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(
    settings.baseUrl,
    'amazon_q_developer_jupyterlab_ext',
    endPoint
  );

  const response = await ServerConnection.makeRequest(requestUrl, init, settings);
  if (response.status === HttpStatusCode.NOT_FOUND) {
    NotificationManager.getInstance().postNotificationForApiExceptions(
        message('codewhisperer_server_extension_not_enabled_message'),
        message("codewhisperer_learn_more"),
        LEARN_MORE_NOTIFICATION_URL
    ).then();
  }
  return response;
}

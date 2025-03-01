import { Dialog, Notification, showDialog } from "@jupyterlab/apputils";
import { Logger } from '../logging/logger';
import { pino } from 'pino';
import { loadState, saveState } from "../utils/utils";
import { UPDATE_NOTIFICATION_DO_NOT_SHOW_AGAIN } from "../utils/stateKeys";
import { message } from "../messages";
import { NOTIFICATION_TEXT_LIMIT } from "../utils/constants";

export class NotificationManager {

    private static instance: NotificationManager;
    private _notifiedErrors: string[] = [];
    private logger: pino.Logger;


    private constructor() {
        this.logger = Logger.getInstance({
            "name": "codewhisperer",
            "component": "notifications"
        });
    }

    public static getInstance(): NotificationManager {
        if (!NotificationManager.instance) {
            NotificationManager.instance = new NotificationManager();
        }
        return NotificationManager.instance;
    }

    public async postNotificationForApiExceptions(notificationMessage: string, actionName: string, actionUrl: string): Promise<void> {

        if (!this._notifiedErrors.includes(notificationMessage)) {
            const notificationMessageWithTitle = "Q Developer:\n" + notificationMessage
            const givenAction = {
                label: actionName,
                callback: (event: MouseEvent) => {
                    window.open(actionUrl, '_blank');

                    // Prevent auto-dismissing the notification
                    event.preventDefault();
                },
            }
            const showFullMessageAction = {
                label: message("codewhisperer_notification_show_full_message_button_title"),
                callback: (event: MouseEvent) => {
                    showDialog({
                        body: notificationMessageWithTitle,
                        buttons: [
                            Dialog.okButton()
                        ]
                    })

                    // Prevent auto-dismissing the notification
                    event.preventDefault();
                }
            }
            const actions = notificationMessageWithTitle.length > NOTIFICATION_TEXT_LIMIT ? [givenAction, showFullMessageAction] : [givenAction];
            Notification.error(notificationMessageWithTitle, {
                autoClose: 10000,
                actions: actions
            })
            this._notifiedErrors.push(notificationMessage);
        } else {
            this.logger.error(`Skipping previous error notification`, notificationMessage);
        }
    }

    public async postNotificationForUpdateInformation(notificationMessage: string,
        latestVersion: string,
        actionName: string,
        actionUrl: string): Promise<void> {
        const isDoNotShowAgainVersions : string[] = await loadState(UPDATE_NOTIFICATION_DO_NOT_SHOW_AGAIN);

        if(isDoNotShowAgainVersions !== undefined){
            if(isDoNotShowAgainVersions.includes(latestVersion)){
                return;
            }
        }
        const id = Notification.info(notificationMessage, {
            autoClose: 5000,
            actions: [
                {
                    label: actionName,
                    callback: () => {
                        window.open(actionUrl, '_blank');
                    },
                },
                {
                    label: message("codewhisperer_update_notification_skip_this_version"),
                    callback: () => {
                        Notification.dismiss(id);
                        saveState(UPDATE_NOTIFICATION_DO_NOT_SHOW_AGAIN, [...isDoNotShowAgainVersions , latestVersion]);
                        this.logger.debug(`Setting update notification do not show again`);
                    }
                }
            ]
        })
    }
}

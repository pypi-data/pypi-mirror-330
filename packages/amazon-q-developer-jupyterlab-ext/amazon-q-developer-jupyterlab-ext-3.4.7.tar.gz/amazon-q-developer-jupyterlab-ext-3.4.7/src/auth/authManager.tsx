/*!
 * Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
import { requestAPI } from "../handler";
import {
    getErrorResponseUserMessage,
    getResponseData,
    loadState,
    isResponseSuccess,
    removeState,
    saveState
} from "../utils/utils";
import {Signal} from "@lumino/signaling";
import { Notification } from "@jupyterlab/apputils";
import { message } from "../messages";
import { showDialog, Dialog } from '@jupyterlab/apputils';
import React from "react";
import { CLIENT_REGISTRATION, SSO_TOKEN } from "../utils/stateKeys";
import { NotificationManager } from "../notifications/notifications";
import { Application } from "../application";
import { EXPIRATION_BUFFER_IN_SECONDS, HttpStatusCode } from "../utils/constants";
import { LEARN_MORE_NOTIFICATION_URL } from "../utils/constants";

export class AuthManager {
    private static instance: AuthManager;
    private _authState: AuthState = AuthState.UNAUTHENTICATED;
    public authStateChangedSignal: Signal<any, AuthState>;
    private _refreshIntervalInMs = 50 * 60 * 1000;
    private readonly _refreshToken: () => Promise<void>

    public static getInstance(): AuthManager {
        if (!AuthManager.instance) {
            AuthManager.instance = new AuthManager();
        }
        return AuthManager.instance;
    }

    private constructor() {
        this.authStateChangedSignal = new Signal(this);
        this.authStateChangedSignal.connect(this._onAuthStateChanged, this)
        this._refreshToken = async () => {
            if (!this.isAuthenticated()) return
            await this.refresh();
        };
    }

    private _onAuthStateChanged(sender: any, authState: AuthState) {
        this.authState = authState
        if (authState === AuthState.UNAUTHENTICATED || authState === AuthState.AUTHENTICATION_IN_PROGRESS) return;

        // Schedule the next refresh task whenever the current login/refresh succeeds
        setTimeout(this._refreshToken, this._refreshIntervalInMs);
    }

    public isAuthenticated(): boolean {
        return Application.getInstance().isQEnabled && (this.authState === AuthState.AUTHENTICATED || !Application.getInstance().isJupyterOSS());
    }

    public isAuthenticationInProgress(): boolean {
        return this.authState === AuthState.AUTHENTICATION_IN_PROGRESS
    }

    private get authState(): AuthState {
        return this._authState
    }

    private set authState(value: AuthState) {
        this._authState = value
    }

    public async login() {
        let registerClientResponseJsonData = await loadState(CLIENT_REGISTRATION)
        const isValidRegistration = registerClientResponseJsonData
            ? registerClientResponseJsonData.clientSecretExpiresAt >
                (Date.now() / 1000 + EXPIRATION_BUFFER_IN_SECONDS)
            : false;

        if (!isValidRegistration) {
            const registerClientResponse = await requestAPI<Response>('register_client')
            const registerClientResponseJson = await registerClientResponse.json()
            if (!isResponseSuccess(registerClientResponseJson)) {
                await NotificationManager.getInstance().postNotificationForApiExceptions(
                    getErrorResponseUserMessage(registerClientResponseJson),
                    message("codewhisperer_learn_more"), 
                    LEARN_MORE_NOTIFICATION_URL
                );
                return;
            }
            registerClientResponseJsonData = getResponseData(registerClientResponseJson)
            saveState(CLIENT_REGISTRATION, registerClientResponseJsonData).then()
        }

        const deviceAuthorizationResponse = await requestAPI<Response>('device_authorization', {
            body: JSON.stringify(registerClientResponseJsonData),
            method: 'POST',
        })
        const deviceAuthorizationResponseJson = await deviceAuthorizationResponse.json()
        if (!isResponseSuccess(deviceAuthorizationResponseJson)) {
            await NotificationManager.getInstance().postNotificationForApiExceptions(
                getErrorResponseUserMessage(deviceAuthorizationResponseJson),
                message("codewhisperer_learn_more"), 
                LEARN_MORE_NOTIFICATION_URL
            );
            return;
        }
        const deviceAuthorizationResponseJsonData = getResponseData(deviceAuthorizationResponseJson)

        // TODO: add link for Learn more
        const dialogResult = await showDialog({
            title: message("codewhisperer_copy_code_and_proceed_dialog_title"),
            body:
    <p>
        <br/>
        <li>
            {message("codewhisperer_copy_code_and_proceed_dialog_message_first_li")}
            <a href={"https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html"} className="cwspr-learn-more-link">
                {message("codewhisperer_copy_code_and_proceed_dialog_message_first_li_learn_more")}
            </a>
        </li>
        <br/>
        <li>
            {message("codewhisperer_copy_code_and_proceed_dialog_message_second_li")}
        </li>
        <br/>
        <li>
            {message("codewhisperer_copy_code_and_proceed_dialog_message_third_li")}
            {deviceAuthorizationResponseJsonData['userCode']}
        </li>
        <br/>
    </p>
,
            buttons: [
                Dialog.cancelButton(),
                Dialog.okButton({
                    label: message("codewhisperer_copy_code_and_proceed_dialog_button_yes")
                })
            ]
        });
        if (!dialogResult.button.accept) {
            return;
        }
        window.open(deviceAuthorizationResponseJsonData['verificationUriComplete'], '_blank')
        this.authStateChangedSignal.emit(AuthState.AUTHENTICATION_IN_PROGRESS)
        const createTokenRequest = {
            clientRegistration: registerClientResponseJsonData,
            deviceAuthorizationResponse: deviceAuthorizationResponseJsonData,
        }
        const createTokenResponsePromise = requestAPI<Response>('create_token', {
            body: JSON.stringify(createTokenRequest),
            method: 'POST',
        })

        createTokenResponsePromise.then(async (createTokenResponse) => {
            const createTokenResponseJson = await createTokenResponse.json()

            // CreateToken call will return null if user cancels login before they finish the browser login flow,
            // which should do nothing from below.
            if (!createTokenResponseJson) return;

            if (!isResponseSuccess(createTokenResponseJson)) {
                await NotificationManager.getInstance().postNotificationForApiExceptions(
                    getErrorResponseUserMessage(createTokenResponseJson),
                    message("codewhisperer_learn_more"), 
                    LEARN_MORE_NOTIFICATION_URL
                );
                this.authStateChangedSignal.emit(AuthState.UNAUTHENTICATED)
                return;
            }
            const createTokenResponseJsonData = getResponseData(createTokenResponseJson)
            await saveState(SSO_TOKEN, createTokenResponseJsonData)
            this.authStateChangedSignal.emit(AuthState.AUTHENTICATED)
        });
    }

    public cancelLogin() {
        requestAPI<Response>('cancel_login').then();
        this.authStateChangedSignal.emit(AuthState.UNAUTHENTICATED)
    }

    public async refresh() {
        const token = await loadState(SSO_TOKEN)
        if (token === undefined) return
        const clientRegistration = await loadState(CLIENT_REGISTRATION)
        if (clientRegistration === undefined) return
        const input = {
            clientRegistration: clientRegistration,
            token: token,
        }

        const refreshTokenResponse = await requestAPI<Response>('refresh',  {
            body: JSON.stringify(input),
            method: 'POST',
        });
        if (refreshTokenResponse.status === HttpStatusCode.NOT_FOUND) return;
        const refreshTokenResponseJson = await refreshTokenResponse.json()


        if (!isResponseSuccess(refreshTokenResponseJson)) {
            // Failed to refresh the token, the user will no longer have a valid token to use now thus need to re-login.
            // Show a re-auth notification for them
            const notificationId = Notification.emit(
                message("codewhisperer_expiry_notification_message"),
                'default',
                {
                    autoClose: 10000,
                    actions: [
                        {
                            label: message("codewhisperer_expiry_notification_button_authenticate"),
                            callback: async () => {
                                await this.login()
                            },
                            displayType: 'accent'
                        },
                        {
                            label: message("codewhisperer_expiry_notification_button_cancel"),
                            callback: async () => {
                                // Do nothing, just dismiss the notification.
                                Notification.dismiss(notificationId);
                            }
                        }
                    ]
                }
            );
            return;
        }
        const refreshTokenResponseJsonData = getResponseData(refreshTokenResponseJson)
        await saveState(SSO_TOKEN, refreshTokenResponseJsonData)
        this.authStateChangedSignal.emit(AuthState.AUTHENTICATED)
    }

    public async logout() {
        await removeState(SSO_TOKEN)
        await removeState(CLIENT_REGISTRATION)
        this.authStateChangedSignal.emit(AuthState.UNAUTHENTICATED)
    }
}

export enum AuthState {
    AUTHENTICATED,
    UNAUTHENTICATED,
    AUTHENTICATION_IN_PROGRESS,
}

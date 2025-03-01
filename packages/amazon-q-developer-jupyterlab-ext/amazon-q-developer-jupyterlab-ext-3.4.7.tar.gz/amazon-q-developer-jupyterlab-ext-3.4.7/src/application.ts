/*!
 * Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
import { Signal } from "@lumino/signaling";
import { Worker } from "./recommendation/worker";
import { AuthManager } from "./auth/authManager";
import { requestAPI } from "./handler";
import { getResponseData } from "./utils/utils";
import { HttpStatusCode } from "./utils/constants";
import { NotificationManager } from "./notifications/notifications";
import {  UPDATE_NOTIFICATION_URL } from "./utils/constants";
import { message } from "./messages";
import { IStateDB } from "@jupyterlab/statedb";
import { JupyterFrontEnd } from "@jupyterlab/application";
import { ISettingRegistry } from "@jupyterlab/settingregistry";
import { AutoTrigger } from './autotrigger/autotrigger';

export class Application {
    private static instance: Application;
    public loadStateSignal: Signal<any, any>;
    private _environment: Environment = undefined;
    private _qEnabled: boolean = undefined;
    public stateDB: IStateDB;
    public jupyterApp: JupyterFrontEnd;
    public setting: ISettingRegistry.ISettings;
    public toggleSettingSignal: Signal<any, string>

    public static getInstance(): Application {
        if (!Application.instance) {
            Application.instance = new Application()
        }
        return Application.instance;
    }

    private constructor() {
        this.loadStateSignal = new Signal(this);
        this.toggleSettingSignal = new Signal(this);
    }

    private async _fetchEnvironment() {
        const getEnvironmentResponse = await requestAPI<Response>('get_environment')
        if (getEnvironmentResponse.status !== HttpStatusCode.OK) return;
        const getEnvironmentResponseJson = await getEnvironmentResponse.json();
        this._environment = getResponseData(getEnvironmentResponseJson)['environment'];
        this._qEnabled = getResponseData(getEnvironmentResponseJson)['q_enabled'];
        const versionNotification = getResponseData(getEnvironmentResponseJson)['version_notification'];
        const latestVersion = getResponseData(getEnvironmentResponseJson)['latest_version'];
        if(versionNotification) {
            NotificationManager.getInstance().postNotificationForUpdateInformation(
                versionNotification,
                latestVersion,
                message("codewhisperer_update_now"),
                UPDATE_NOTIFICATION_URL
            ).then();
        }
    }

    public isJupyterOSS(): boolean {
        return this._environment === Environment.JUPYTER_OSS;
    }

    public isSageMakerStudio(): boolean {
        return this._environment === Environment.SM_STUDIO;
    }

    public isGlueStudioNoteBook(): boolean {
        return this._environment === Environment.GLUE_STUDIO_NOTEBOOK;
    }

    public isMD(): boolean {
        return [Environment.MD_IAM, Environment.MD_IDC, Environment.MD_SAML].includes(this._environment)
    }

    public isIdcMode(): boolean {
        return [Environment.MD_IDC, Environment.SM_STUDIO_SSO].includes(this._environment);
    }

    public get isQEnabled(): boolean {
        return this._qEnabled;
    }

    // Initialize all the application singletons here
    public async loadServices(stateDB: IStateDB, jupyterApp: JupyterFrontEnd) {
        this.stateDB = stateDB;
        this.jupyterApp = jupyterApp;

        await this._fetchEnvironment()

        Worker.getInstance();
        AutoTrigger.getInstance();
        AuthManager.getInstance();
    }
}

enum Environment {
    JUPYTER_OSS = 'Jupyter OSS',
    SM_STUDIO = 'SageMaker Studio',
    SM_STUDIO_SSO = 'SageMaker Studio SSO',
    GLUE_STUDIO_NOTEBOOK = 'Glue Studio Notebook',
    MD_IAM = "MD_IAM",
    MD_IDC = "MD_IDC",
    MD_SAML = "MD_SAML"
}

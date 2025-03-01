/*!
 * Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */


import * as CodeWhispererClient from "./codewhispererclient";
import * as CodeWhispererUserClient from './codewhispereruserclient';
import { requestAPI } from '../handler';
import { loadState } from "../utils/utils";
import { SSO_TOKEN } from "../utils/stateKeys";

export type GenerateRecommendationsRequest = Readonly<CodeWhispererClient.GenerateRecommendationsRequest>;
export type GenerateRecommendationsResponse = CodeWhispererClient.GenerateRecommendationsResponse;
export type FileContext = Readonly<CodeWhispererClient.FileContext>;
export type RecommendationsList = CodeWhispererClient.RecommendationsList | CodeWhispererUserClient.Completions;

export type GenerateCompletionsRequest = CodeWhispererUserClient.GenerateCompletionsRequest;
export type GenerateCompletionsResponse = CodeWhispererUserClient.GenerateCompletionsResponse;

export type Reference = CodeWhispererClient.Reference | CodeWhispererUserClient.Reference;
export type References = CodeWhispererClient.References | CodeWhispererUserClient.References;

type ListAvailableCustomizationsRequest = {}

/**
 * A minimal Sig V4 API client
 */

export class ApiClient {

    public async generateRecommendations(request: GenerateRecommendationsRequest, optOut: Boolean): Promise<Response> {
        const token = await loadState(SSO_TOKEN);
        const accessToken = token === undefined ? "" : token['accessToken'];
        const response = await requestAPI<Response>('generate_recommendations', {
            headers: {
                'Token': accessToken,
                'OptOut' : optOut.toString()
            },
            body: JSON.stringify(request),
            method: 'POST',
        });
        return response;
    }

    /**
     * 
     * @param request a string representing the prompt to generate recommendations
     * @param optOut a boolean which is true if a user has opted out of Q telemetry
     * @returns completions from the CW API. 
     */
    public async generateGlueRecommendations(request: string, optOut: Boolean): Promise<Response> {
        const response = await requestAPI<Response>('query', {
            headers: {
                'OptOut' : optOut.toString()
            },
            body: JSON.stringify({ Prompt: request }),
            method: 'POST',
        });
        return response;
    }

    public async listAvailableCustomizations(request: ListAvailableCustomizationsRequest): Promise<any> {
        const response = await requestAPI<Response>('list_available_customizations', {
            headers: {},
            body: JSON.stringify(request),
            method: 'POST',
        });

        return response.json();
    }
}

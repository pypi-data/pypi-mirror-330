/*!
 * Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */


import * as ClientTelemetry from './clienttelemetry';
import { requestAPI } from '../handler';
import { Logger } from '../logging/logger';
import { pino } from 'pino';

export type PostMetricsRequest = ClientTelemetry.PostMetricsRequest;


export class TelemetryApiClient {

  private logger: pino.Logger;


  constructor() {
    this.logger = Logger.getInstance({
      "name": "codewhisperer",
      "component" : "telemetryApiClient"
  });
  }

  public async postMetrics(
    request: PostMetricsRequest
  ): Promise<any> {
    try {
      await requestAPI<any>('post_metrics', {
        body: JSON.stringify(request),
        method: 'POST',
      });
    } catch (reason) {
      this.logger.error(`Error on postMetrics.\n${reason}`);
    }
    return undefined
  }

}

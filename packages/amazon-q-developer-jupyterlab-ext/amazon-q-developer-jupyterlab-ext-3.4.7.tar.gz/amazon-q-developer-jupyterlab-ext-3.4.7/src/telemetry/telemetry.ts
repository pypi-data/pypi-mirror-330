/*!
 * Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

import { PostMetricsRequest, TelemetryApiClient } from './telemetryClient';
import { Worker } from '../recommendation/worker';

// This file makes it so you can import 'telemetry' and not 'telemetry.gen'
import { MetricDatum } from './clienttelemetry';
import { CodewhispererServiceInvocation, MetricBase } from './telemetry.gen';
import { TELEMETRY_SERVICE_INVOCATION_METRIC_NAME } from '../utils/constants';
const { version } = require('../../package.json');

import { Logger } from '../logging/logger';
import { pino } from 'pino';

export class Telemetry {
    private static readonly defaultFlushPeriodMillis = 1000 * 60 * 0.25 // 15 seconds, TODO: change to 5 minutes
    private static readonly defaultMaxBatchSize = 20
    private static instance: Telemetry;
    public static clientId: string;
    private logger: pino.Logger;


    private telemetryClient: TelemetryApiClient;
    private readonly _eventQueue: MetricDatum[]
    private _telemetryEnabled: boolean = true //TODO: make this configurable
    private _timer?: NodeJS.Timer
    public startTime: Date

    public static getInstance(): Telemetry {
        if (!Telemetry.instance) {
            Telemetry.instance = new Telemetry()
        }
        return Telemetry.instance
    }

    public static init() {
        Telemetry.getInstance();
    }

    private constructor() {
        this.startTimer();
        this._eventQueue = [];
        this.telemetryClient = new TelemetryApiClient();
        this.logger = Logger.getInstance({
            "name": "codewhisperer",
            "component" : "telemetry"
        });
        Worker.getInstance().serviceInvocationSignal.connect(this.onServiceInvocationListener, this);
    }

    private onServiceInvocationListener(sender: any, value: CodewhispererServiceInvocation) {
        Telemetry.getInstance().recordTelemetry(TELEMETRY_SERVICE_INVOCATION_METRIC_NAME, value)
    }

    recordTelemetry(metricName: string, event: MetricBase) {
        if (this._telemetryEnabled) {
            const metadata = Object.entries(event)
                .filter(([_, v]) => v !== '' && v !== undefined)
                .map(([k, v]) => ({ Key: k, Value: String(v) }))

            this._eventQueue.push({
                MetricName: metricName,
                EpochTimestamp: Date.now(),
                Unit: "None",
                Value: 1,
                Metadata: metadata
            })

            this.logger.debug(`Recording telemetry: ${metricName}}`)
        }
    }

    private async startTimer() {
        this._timer = setInterval(async () => {
            try {
                await this.flush()
            } catch (e) {
                this.logger.error(e)
            }
        }, Telemetry.defaultFlushPeriodMillis)
    }

    public enableTelemetry(telemetryEnabled: boolean): void {
        this._telemetryEnabled = telemetryEnabled;
    }

    public isTelemetryEnabled(): boolean {
        return this._telemetryEnabled;
    }

    public closeTimer() {
        if (this._timer !== undefined) {
            clearTimeout(this._timer)
            this._timer = undefined
        }
    }

    private async flush(): Promise<void> {
        if (this._telemetryEnabled) {
            if (this.telemetryClient === undefined) {
                this.telemetryClient = new TelemetryApiClient()
            }
            if (this.telemetryClient !== undefined) {
                while (this._eventQueue.length !== 0) {
                    const batch = this._eventQueue.splice(0, Telemetry.defaultMaxBatchSize)

                    if (this.telemetryClient === undefined) {
                        return
                    }

                    this.telemetryClient.postMetrics(this.buildPostMetricsRequest(batch))
                    this.logger.debug("Telemetry flushed")
                }
                this.clearRecords()
            }
        }
    }

    private clearRecords(): void {
        this._eventQueue.length = 0
    }

    private buildPostMetricsRequest(records: MetricDatum[]): PostMetricsRequest {
        return {
            AWSProduct: "CodeWhisperer For JupyterLab",
            AWSProductVersion: version,
            ClientID: Telemetry.clientId,
            MetricData: records,
        }
    }
}
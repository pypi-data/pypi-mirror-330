import { Recommendation } from "../client/codewhispererclient";
import { Telemetry } from "../telemetry/telemetry";
import {
    CodewhispererJupyterLabCellType,
    CodewhispererPreviousSuggestionState,
    CodewhispererSuggestionState,
    CodewhispererUserDecision,
    CodewhispererUserTriggerDecision
} from '../telemetry/telemetry.gen';
import { TELEMETRY_USER_DECISION_METRIC_NAME, TELEMETRY_USER_TRIGGER_DECISION_METRIC_NAME } from "../utils/constants";
import { LicenseUtil } from "../utils/licenseUtils";
import { ServiceInvocationMetadata, RecommendationState } from "../utils/models";
import { Signal } from "@lumino/signaling";
import { Logger } from '../logging/logger';
import { pino } from 'pino';

export class RecommendationStateHandler {
    static #instance: RecommendationStateHandler;
    private logger: pino.Logger;

    /**
     * These are updated per trigger
     */
    private invocationMetadata: ServiceInvocationMetadata;
    private firstRequestId: string;
    private timeToFirstRecommendation: number;
    public typeAheadLength: number; // length of typeahead when receiving the first recommendation
    private previousSuggestionState: CodewhispererPreviousSuggestionState;
    private timeSinceLastUserDecision: number;
    public timeSinceLastDocumentChange: number;

    /**
     * These are updated per CodeWhisperer Invocation
     */
    private requestId: string;
    private recommendations: Recommendation[];
    private recommendationSuggestionState: Map<number, RecommendationState>;
    private acceptedIndex: number = -1;

    // These are consistent per Handler object
    public acceptRecommendationSignal: Signal<this, number>;
    public rejectRecommendationSignal: Signal<this, number>;

    private constructor() {
        this.timeSinceLastUserDecision = undefined;
        this.timeSinceLastDocumentChange = undefined;
        this.recommendations = [];
        this.recommendationSuggestionState = new Map<number, RecommendationState>();
        this.acceptRecommendationSignal = new Signal(this);
        this.acceptRecommendationSignal.connect(this.userDecisionSignalListener, this);
        this.rejectRecommendationSignal = new Signal(this);
        this.rejectRecommendationSignal.connect(this.userDecisionSignalListener, this);
        this.logger = Logger.getInstance({
            "name": "codewhisperer",
            "component" : "recommendationStateHandler"
        });
    }

    reset() {
        this.timeToFirstRecommendation = undefined;
        this.requestId = undefined;
        this.firstRequestId = undefined;
        this.invocationMetadata = undefined;
        this.acceptedIndex = -1;
        this.recommendations = [];
        this.recommendationSuggestionState = new Map<number, RecommendationState>();
        return;
    }

    public static get instance() {
        return (this.#instance ??= new this());
    }

    updateInvocationMetadata(invocationMetadata: ServiceInvocationMetadata, requestId: string, isFirstInvocation: boolean) {
        if (isFirstInvocation) {
            // first invocation
            this.invocationMetadata = invocationMetadata;
            this.firstRequestId = requestId;
            this.requestId = requestId;
            this.timeToFirstRecommendation = performance.now() - invocationMetadata.triggerMetadata.triggerTime;
        } else {
            // subsequent invocation
            this.requestId = requestId;
        }
    }

    setSuggestionState(index: number, value: RecommendationState) {
        this.logger.debug("setSuggestionState: index: " + index + " value: " + value);
        this.recommendationSuggestionState.set(index, value);
    }

    addRecommendations(recommendations: Recommendation[]) {
        this.updateRecommendationState(recommendations);
    }

    addRecommendation(recommendation: Recommendation) {
        this.recommendations.push(recommendation);
    }

    private updateRecommendationState(recommendations: Recommendation[]) {
        const previousRecommendationsLength = this.recommendations.length;
        if (recommendations.length > 0) {
            recommendations.forEach((recommendation, index) => {
                // value: RecommendationsList is appended to this.completions, so the index of the current completion is the length of this.completions - 1
                RecommendationStateHandler.instance.setSuggestionState(previousRecommendationsLength + index, "Discard");
                RecommendationStateHandler.instance.addRecommendation(recommendation);
            })
        } else {
            RecommendationStateHandler.instance.addRecommendation({content: "", references: []});
            RecommendationStateHandler.instance.setSuggestionState(previousRecommendationsLength, "Empty");
        };
    }

    userDecisionSignalListener(sender: any, value: number) {
        this.acceptedIndex = value;
        this.recordUserDecisionTelemetry();
    }

    private recordUserDecisionTelemetry() {
        if (!this.invocationMetadata) {
            //TODO: this is not the optimal solution. 
            // We should record suggestions as Discard for the ones returned after user moves
            // on from (accept/reject) the previous suggestions
            this.reset();
            return;
        }

        const userDecisionEvents: CodewhispererUserDecision[] = [];

        this.recommendations.forEach((recommendation, index) => {
            let uniqueSuggestionReferences: string | undefined = undefined;
            const uniqueLicenseSet = LicenseUtil.getUniqueLicenseNames(recommendation.references);
            if (uniqueLicenseSet.size > 0) {
                uniqueSuggestionReferences = JSON.stringify(Array.from(uniqueLicenseSet));
            }
            if (recommendation.content.length === 0) {
                this.recommendationSuggestionState?.set(index, "Empty");
            }

            const event: CodewhispererUserDecision = {
                codewhispererSuggestionIndex: index,
                codewhispererSuggestionState: this.getSuggestionState(index, this.acceptedIndex),
                codewhispererCompletionType: this.invocationMetadata.completionType,
                codewhispererLanguage: this.invocationMetadata.triggerMetadata.language,
                codewhispererSessionId: this.invocationMetadata.sessionId,
                codewhispererRequestId: this.requestId,
                codewhispererPaginationProgress: this.invocationMetadata.paginationProgress,
                codewhispererSuggestionReferences: uniqueSuggestionReferences,
                codewhispererSuggestionReferenceCount: recommendation.references
                    ? recommendation.references.length
                    : 0,
                credentialStartUrl: this.invocationMetadata.credentialStartUrl,
                codewhispererTriggerType: this.invocationMetadata.triggerMetadata.triggerType,
            };
            userDecisionEvents.push(event);
            Telemetry.getInstance().recordTelemetry(TELEMETRY_USER_DECISION_METRIC_NAME, event);
        });

        this.recordUserTriggerDecisionTelemetry(userDecisionEvents);

        this.reset();
    }

    private recordUserTriggerDecisionTelemetry(events: CodewhispererUserDecision[]) {
        if (!this.invocationMetadata) {
            return;
        }
        const userDecisionByTrigger = this.getAggregatedUserDecisionBySession(events);

        const event: CodewhispererUserTriggerDecision = {
            codewhispererSessionId: this.invocationMetadata.sessionId,
            codewhispererFirstRequestId: this.firstRequestId,
            codewhispererSuggestionState: userDecisionByTrigger,
            codewhispererCompletionType: this.invocationMetadata.completionType,
            codewhispererTriggerType:  this.invocationMetadata.triggerMetadata.triggerType,
            codewhispererLanguage: this.invocationMetadata.triggerMetadata.language,
            codewhispererAutomatedTriggerType: this.invocationMetadata.triggerMetadata.automatedTriggerType,
            codewhispererLineNumber: this.invocationMetadata.fileContextMetadata.lineNumber,
            codewhispererCursorOffset: this.invocationMetadata.fileContextMetadata.cursorOffset,
            codewhispererJupyterLabCellCount: this.invocationMetadata.fileContextMetadata.cellCount,
            codewhispererJupyterLabCellIndex: this.invocationMetadata.fileContextMetadata.activeCellIdx,
            codewhispererJupyterLabCellType: <CodewhispererJupyterLabCellType>this.invocationMetadata.fileContextMetadata.cellType,
            codewhispererSuggestionCount: this.recommendations.length,
            codewhispererTriggerCharacter: this.invocationMetadata.triggerMetadata.triggerType === 'AutoTrigger' ? this.invocationMetadata.triggerMetadata.triggerCharacter : undefined,
            codewhispererPreviousSuggestionState: this.previousSuggestionState,
            codewhispererTimeToFirstRecommendation: this.timeToFirstRecommendation,
            codewhispererTimeSinceLastUserDecision: this.timeSinceLastUserDecision ? performance.now() - this.timeSinceLastUserDecision : undefined,
            codewhispererTimeSinceLastDocumentChange: this.timeSinceLastDocumentChange,
            codewhispererTypeaheadLength: this.typeAheadLength,
            codewhispererSuggestionImportCount: undefined, // This is dummy value, we don't have this available in JupyterLab at the moment

        };
        Telemetry.getInstance().recordTelemetry(TELEMETRY_USER_TRIGGER_DECISION_METRIC_NAME, event);
        this.previousSuggestionState = (userDecisionByTrigger as CodewhispererPreviousSuggestionState);
    }

    getSuggestionState(i: number, acceptIndex: number): CodewhispererSuggestionState {
        const state = this.recommendationSuggestionState?.get(i);
        if (state && acceptIndex === -1 && ["Empty", "Filter", "Discard"].includes(state)) {
            return state as CodewhispererSuggestionState;
        } else if (
            this.recommendationSuggestionState !== undefined &&
            this.recommendationSuggestionState.get(i) !== "Showed"
        ) {
            return "Unseen";
        }
        if (acceptIndex === -1) {
            return "Reject";
        }
        return i === acceptIndex ? "Accept" : "Ignore";
    }

    /**
     * 1. if there is any Accept within the session, mark the session as Accept.
     * 2. if there is any Reject within the session, mark the session as Reject.
     * 3. if all recommendations within the session are empty, mark the session as Empty.
     * 
     * @returns the aggregated user decision by session.
     */
    private getAggregatedUserDecisionBySession(events: CodewhispererUserDecision[]): CodewhispererSuggestionState {
        let isEmpty = true
        for (const event of events) {
            if (event.codewhispererSuggestionState === 'Accept') {
                return 'Accept'
            } else if (event.codewhispererSuggestionState === 'Reject') {
                return 'Reject'
            } else if (event.codewhispererSuggestionState !== 'Empty') {
                isEmpty = false
            }
        }
        return isEmpty ? 'Empty' : 'Discard'
    }
}

import { CellType } from "@jupyterlab/nbformat";
import {
    CodewhispererAutomatedTriggerType,
    CodewhispererCompletionType,
    CodewhispererLanguage,
    CodewhispererTriggerType,
} from "../telemetry/telemetry.gen";

export interface FileContextMetadata {
    readonly activeCellIdx?: number;
    readonly cellCount?: number;
    readonly cellType?: CellType;
    readonly lineNumber: number;
    readonly cursorOffset: number;
}

export interface TriggerMetadata {
    readonly triggerType: CodewhispererTriggerType;
    readonly automatedTriggerType: CodewhispererAutomatedTriggerType;
    readonly triggerCharacter: string;
    readonly language: CodewhispererLanguage;
    readonly triggerTime: number;
}

export interface ServiceInvocationMetadata {
    readonly completionType: CodewhispererCompletionType;
    readonly credentialStartUrl: string;
    readonly sessionId: string;
    readonly paginationProgress: number;
    readonly fileContextMetadata: FileContextMetadata;
    readonly triggerMetadata: TriggerMetadata;
}

export type RecommendationState =
    | "Discard"
    | "Showed"
    | "Filter"
    | "Empty";

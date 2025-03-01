import { requestAPI } from '../handler';
	
export enum CompletionStatus {
    "SUCCEEDED" = "SUCCEEDED",
    "SUBMITTED" = "SUBMITTED",
    "RUNNING" = "RUNNING",
    "FAILED" = "FAILED",
    "DELETED" = "DELETED",
    "EXPIRED" = "EXPIRED",
}

export interface GlueCompletionResponse { 
    completions?: GlueCompletion[];
    nextToken?: string;
    status: CompletionStatus;
    "x-amzn-requestid": string;
    "x-amzn-sessionid": string;
}

interface GlueCompletion {
    content: string;
    mostRelevantMissingImports?: Import[],
    references?: Reference[]
}

type Import = {
    statement: string
}

type Reference = {
    licenseName?: string;
    repository?: string;
    url?: string;
    recommendationContentSpan?: Span;
}

type Span = {
    start: number;
    end: number;
}

export class GlueClient {
    constructor() {
    }
    public async generateResponse(query: string): Promise<Response> { 
        const response = await requestAPI<Response>('query', {
            body: JSON.stringify({Prompt: query}),
            method: 'POST',
        });
        return response;
    }
}
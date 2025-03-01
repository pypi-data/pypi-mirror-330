import { CodewhispererCompletionType } from "../telemetry/telemetry.gen";
import { RecommendationsList } from "../client/apiclient";
import { ReadonlyPartialJSONObject } from "@lumino/coreutils";
import { Application } from "../application";
import { CodeEditor } from "@jupyterlab/codeeditor";
import { ServerConnection } from '@jupyterlab/services';
import { CONTENTS_ENDPOINT } from "./constants";
import { URLExt } from '@jupyterlab/coreutils';

/**
 * @param f callback
 * @param wait milliseconds
 * @param abortValue if has abortValue, promise will reject it if
 * @returns Promise
 */
export function debouncePromise<T extends (...args: any[]) => any>(
    fn: T,
    wait: number,
    abortValue: any = undefined
) {
    let cancel = () => {
        // do nothing
    };
    type Awaited<T> = T extends PromiseLike<infer U> ? U : T
    type ReturnT = Awaited<ReturnType<T>>;
    const wrapFunc = (...args: Parameters<T>): Promise<ReturnT> => {
        cancel();
        return new Promise((resolve, reject) => {
            const timer = setTimeout(() => resolve(fn(...args)), wait);
            cancel = () => {
                clearTimeout(timer);
                if (abortValue !== undefined) {
                    reject(abortValue);
                }
            };
        });
    };
    return wrapFunc;
}



export function sleep(duration: number = 0): Promise<void> {
    const schedule = setTimeout
    return new Promise(r => schedule(r, Math.max(duration, 0)))
}

export function detectCompletionType(recommendations: RecommendationsList): CodewhispererCompletionType {
    if (
        recommendations &&
        recommendations.length > 0) {
        if (recommendations[0].content.search("\n") !== -1) {
            return "Block";
        } else {
            return "Line";
        }
    } else {
        return undefined;
    }
}

// TODO: make loadState, saveState, removeState into Application as a centralized place to manage state
// Use `await loadState(id)` to get the actual value
export async function loadState(id: string): Promise<any | undefined> {
    try {
        const value = await Application.getInstance().stateDB.fetch(id);
        return await value;
    } catch (error) {
        return undefined;
    }
}

export async function saveState(id: string, value: any) {
    try {
        await Application.getInstance().stateDB.save(id, value);
    } catch (error) {
    }
}

export async function removeState(id: string) {
    try {
        await Application.getInstance().stateDB.remove(id);
    } catch (error) {
    }
}

export function isResponseSuccess(json: ReadonlyPartialJSONObject): boolean {
    return ['SUCCESS','SUCCEEDED'].includes(json.status as string)
}

export function getResponseData(json: ReadonlyPartialJSONObject): any {
    return json['data']
}

export function getErrorResponseUserMessage(json: ReadonlyPartialJSONObject): any {
    if (json["error_info"]) {
        const errorInfo = json["error_info"] as ReadonlyPartialJSONObject;
        return errorInfo["user_message"]
    } else if (json["message"]) {
        return (json["message"] as ReadonlyPartialJSONObject)
    } else {
        return "unknown error user message";
    }   
}

export function getPreviousLineContents(editor: CodeEditor.IEditor): string {
    const lineNumber = Math.max(editor.getCursorPosition().line - 1, 0); // get previous line of where cursor is, defaults to 0 if at line 0. 
    return editor.getLine(lineNumber)
}

export function isLineAComment(line: string): boolean {
    return line.trim().startsWith("#")
}

interface CustomizationArn {
    customization_arn: string;
}

enum OPTIONS_TYPE {
    POST = 'POST',
    GET = 'GET',
    PUT = 'PUT',
}

async function callContentsApi(
    endPoint = '',
    init: RequestInit = {}
  ): Promise<Response> {
    // this function is different from requestAPI in handler as it does not need
    // amazon_q_developer_jupyterlab_ext and NotificationManager 
    const settings = ServerConnection.makeSettings();
    const requestUrl = URLExt.join(settings.baseUrl, endPoint);

    return await ServerConnection.makeRequest(requestUrl, init, settings);
  }

async function getDirectory(path: string, returnContent?: boolean): Promise<Response | undefined> {
    try {
        return await callContentsApi(`${CONTENTS_ENDPOINT}/${path}?content=${returnContent ? 1 : 0}`, { method : OPTIONS_TYPE.GET });
    } catch {
        return undefined;
    }
}

async function putDirectory(path: string, name: string): Promise<Response | undefined> {
    return await callContentsApi(`${CONTENTS_ENDPOINT}/${path}`,
        { 
            method : OPTIONS_TYPE.PUT,
            body:JSON.stringify({ type: 'directory', format: 'text', name }),
        });
}

export async function createDirectoryIfDoesNotExist(path: string, name: string) {
    const exists = await getDirectory(path, false);
    if (!exists) {
        await putDirectory(path, name);
    }
}

export async function saveFile(
    path: string,
    name: string,
    ext: string,
    content: CustomizationArn,
): Promise<Response> {
    // PUT method will create the path and file if it does not exist
    return await callContentsApi(
        `${CONTENTS_ENDPOINT}/${path ? `${path}/${name}.${ext}` : `/${name}.${ext}`}`,
        {
            method: OPTIONS_TYPE.PUT,
            body: JSON.stringify({
                content: JSON.stringify(content),
                format: 'text',
                name: `${name}.${ext}`,
                type: 'file',
        }),
    });
}

export async function readFile(
    path: string,
    name: string,
    ext: string,
): Promise<Response> {
    return await callContentsApi(
        `${CONTENTS_ENDPOINT}/${path ? `${path}/${name}.${ext}` : `/${name}.${ext}`}`,
        {
            method: OPTIONS_TYPE.GET,
        }
    );
}

export function getCookie(name: string): string | undefined {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift();
    return undefined;
}

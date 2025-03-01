import { RecommendationStateHandler } from "../../recommendation/recommendationStateHandler";
import { Telemetry } from "../../telemetry/telemetry";
import { TELEMETRY_USER_TRIGGER_DECISION_METRIC_NAME } from "../../utils/constants";

describe("RecommendationStateHandler", () => {
  beforeEach(() => {
    jest.resetModules();
    jest.resetAllMocks();

    RecommendationStateHandler.instance.reset();
    RecommendationStateHandler.instance.updateInvocationMetadata(
      {
        completionType: "Block",
        credentialStartUrl: "url",
        sessionId: "123",
        paginationProgress: 0,
        fileContextMetadata: {
          activeCellIdx: 0,
          cellCount: 1,
          cellType: "code",
          lineNumber: 1,
          cursorOffset: 0,
        },
        triggerMetadata: {
          triggerType: "AutoTrigger",
          automatedTriggerType: "Enter",
          triggerCharacter: "Enter",
          language: "python",
          triggerTime: 0,
        },
      },
      "123",
      true
    );

    RecommendationStateHandler.instance.addRecommendation({
      content: "test",
    });
    RecommendationStateHandler.instance.addRecommendation({
      content: "test2",
    });
  });

  test("should return Accept when there is an Accept in the session", () => {
    RecommendationStateHandler.instance.setSuggestionState(0, "Showed");

    const mockedFn = jest.spyOn(Telemetry.prototype, "recordTelemetry");

    RecommendationStateHandler.instance.userDecisionSignalListener(undefined, 0);

    expect(mockedFn).toHaveBeenCalledWith(TELEMETRY_USER_TRIGGER_DECISION_METRIC_NAME, {
      codewhispererAutomatedTriggerType: "Enter",
      codewhispererCompletionType: "Block",
      codewhispererCursorOffset: 0,
      codewhispererFirstRequestId: "123",
      codewhispererJupyterLabCellCount: 1,
      codewhispererJupyterLabCellIndex: 0,
      codewhispererJupyterLabCellType: "code",
      codewhispererLanguage: "python",
      codewhispererLineNumber: 1,
      codewhispererPreviousSuggestionState: undefined,
      codewhispererSessionId: "123",
      codewhispererSuggestionCount: 2,
      codewhispererSuggestionImportCount: undefined,
      codewhispererSuggestionState: "Accept",
      codewhispererTimeSinceLastDocumentChange: undefined,
      codewhispererTimeSinceLastUserDecision: undefined,
      codewhispererTimeToFirstRecommendation: expect.any(Number),
      codewhispererTriggerCharacter: "Enter",
      codewhispererTriggerType: "AutoTrigger",
      codewhispererTypeaheadLength: undefined,
    });

    expect(mockedFn).toBeCalledTimes(3);
  });

  test("should return Reject when there is no accept in the session", () => {
    RecommendationStateHandler.instance.setSuggestionState(0, "Showed");

    const mockedFn = jest.spyOn(Telemetry.prototype, "recordTelemetry");

    RecommendationStateHandler.instance.userDecisionSignalListener(undefined, -1);

    expect(mockedFn).toHaveBeenCalledWith(TELEMETRY_USER_TRIGGER_DECISION_METRIC_NAME, {
      codewhispererAutomatedTriggerType: "Enter",
      codewhispererCompletionType: "Block",
      codewhispererCursorOffset: 0,
      codewhispererFirstRequestId: "123",
      codewhispererJupyterLabCellCount: 1,
      codewhispererJupyterLabCellIndex: 0,
      codewhispererJupyterLabCellType: "code",
      codewhispererLanguage: "python",
      codewhispererLineNumber: 1,
      codewhispererPreviousSuggestionState: "Accept",
      codewhispererSessionId: "123",
      codewhispererSuggestionCount: 2,
      codewhispererSuggestionImportCount: undefined,
      codewhispererSuggestionState: "Reject",
      codewhispererTimeSinceLastDocumentChange: undefined,
      codewhispererTimeSinceLastUserDecision: undefined,
      codewhispererTimeToFirstRecommendation: expect.any(Number),
      codewhispererTriggerCharacter: "Enter",
      codewhispererTriggerType: "AutoTrigger",
      codewhispererTypeaheadLength: undefined,
    });

    expect(mockedFn).toBeCalledTimes(3);
  });

  test("should return Discard when suggestion state is Discard and accept index == -1", () => {
    RecommendationStateHandler.instance.setSuggestionState(0, "Discard");
    const returnVal = RecommendationStateHandler.instance.getSuggestionState(0, -1);
    expect(returnVal).toBe("Discard");
  });

  test("should return Discard when suggestion state is Discard and acceptIndex != -1 and index != acceptIndex", () => {
    RecommendationStateHandler.instance.setSuggestionState(0, "Discard");
    const returnVal = RecommendationStateHandler.instance.getSuggestionState(0, 1);
    expect(returnVal).toBe("Unseen");
  });

  test("should return Accept when suggestion state is Showed and acceptIndex != -1 and index == acceptIndex", () => {
    RecommendationStateHandler.instance.setSuggestionState(0, "Showed");
    const returnVal = RecommendationStateHandler.instance.getSuggestionState(0, 0);
    expect(returnVal).toBe("Accept");
  });

  test("should return Accept when suggestion state is Showed and acceptIndex != -1 and index != acceptIndex", () => {
    RecommendationStateHandler.instance.setSuggestionState(0, "Showed");
    const returnVal = RecommendationStateHandler.instance.getSuggestionState(0, 1);
    expect(returnVal).toBe("Ignore");
  });
});

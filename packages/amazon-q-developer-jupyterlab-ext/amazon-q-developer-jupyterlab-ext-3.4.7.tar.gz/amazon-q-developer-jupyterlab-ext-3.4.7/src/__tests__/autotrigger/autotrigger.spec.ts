import { AutoTrigger } from "../../autotrigger/autotrigger";
import { SourceChange } from '@jupyter/ydoc';

jest.mock("@jupyterlab/apputils");
jest.mock("@jupyterlab/ui-components");
jest.mock("@jest/transform");
jest.mock("../../logging/logger");
jest.mock("../../inline/inline");

let autoTrigger = new AutoTrigger();
let changeArgs: SourceChange;

describe("AutoTrigger tests", () => {
  beforeEach(() => {
    autoTrigger = new AutoTrigger();
    changeArgs = {
      sourceChange: [{
        insert: 'a'
      }]
    };
  });

  test("should trigger on idle time", async () => {
    changeArgs.sourceChange![0].insert = "a";
    autoTrigger.lastKeyStrokeTime = performance.now() - 3000;

    const returnedValue = autoTrigger.shouldAutoTrigger(changeArgs);
    expect(returnedValue.autoTriggerType).toBe("IdleTime");
    expect(returnedValue.triggerCharacter).toBeUndefined();
  });

  test("should not trigger on idle time", async () => {
    changeArgs.sourceChange![0].insert = "a";
    autoTrigger.lastKeyStrokeTime = performance.now();

    const returnedValue = autoTrigger.shouldAutoTrigger(changeArgs);
    expect(returnedValue.autoTriggerType).toBe(undefined);
    expect(returnedValue.triggerCharacter).toBeUndefined();
  });

  test("should trigger on new line", async () => {
    changeArgs.sourceChange![0].insert = "\n";


    const returnedValue = autoTrigger.shouldAutoTrigger(changeArgs);
    expect(returnedValue.autoTriggerType).toBe("Enter");
    expect(returnedValue.triggerCharacter).toBeUndefined();
  });

  test("should trigger on special character", async () => {
    changeArgs.sourceChange![0].insert = "(";

    const returnedValue = autoTrigger.shouldAutoTrigger(changeArgs);
    expect(returnedValue.autoTriggerType).toBe("SpecialCharacters");
    expect(returnedValue.triggerCharacter).toBe("(");
  });
});

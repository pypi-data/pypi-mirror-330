import { CommandRegistry } from '@lumino/commands';

export class Keybindings {
  private static instance: Keybindings;
  public keyBindings: CommandRegistry.IKeyBinding[];

  private constructor() { }

  public static getInstance(): Keybindings {
    if (!Keybindings.instance) {
      Keybindings.instance = new Keybindings();
    }
    return Keybindings.instance;
  }

  public getKeybinding(cmd: string): string[] {

    var keyMap = [].concat(...this.keyBindings
      .filter(shortcut => shortcut.command === cmd)
      .map(obj => obj.keys));

    keyMap = keyMap.map(key => key.replace('Enter', '↩'));
    keyMap = keyMap.map(key => key.replace('Shift', '⇧'));

    if (navigator.userAgent.includes('Mac')) {
      keyMap = keyMap.map(key => key.replace('Alt', '⌥'));
      keyMap = keyMap.map(key => key.replace('Cmd', '⌘'));
      keyMap = keyMap.map(key => key.replace('Ctrl', '⌃'));
    }
    return keyMap;

  }
}
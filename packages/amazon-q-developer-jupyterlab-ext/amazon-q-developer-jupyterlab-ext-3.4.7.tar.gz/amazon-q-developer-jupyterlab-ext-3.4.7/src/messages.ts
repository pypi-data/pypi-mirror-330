const localization = require('../locale/messages.json');

export function message(id: string) {
    return localization[id];
}

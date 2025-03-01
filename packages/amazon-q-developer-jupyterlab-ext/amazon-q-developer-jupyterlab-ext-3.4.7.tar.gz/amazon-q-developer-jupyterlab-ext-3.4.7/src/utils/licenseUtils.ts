import { References } from "../client/apiclient"

export class LicenseUtil {
    public static getUniqueLicenseNames(references: References | undefined): Set<string> {
        const n = new Set<string>()
        references?.forEach(r => {
            if (r.licenseName) {
                n.add(r.licenseName)
            }
        })
        return n
    }
}

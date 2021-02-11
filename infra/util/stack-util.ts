import config from 'config'

export class StackUtil {
    static getStackName(stackPart: string) {
        const systemNameUpperCase = config.get<string>('systemName').toUpperCase();
        return `${systemNameUpperCase}-${stackPart}`;
    }

    static getName(resourcePart: string) {
        const systemNameUpperCase = config.get<string>('systemName');
        return `${systemNameUpperCase}-${resourcePart}`;
    }

    static getUpperCaseName(resourcePart: string) {
        const systemNameUpperCase = config.get<string>('systemName').toUpperCase();
        return `${systemNameUpperCase}-${resourcePart}`;
    }

}

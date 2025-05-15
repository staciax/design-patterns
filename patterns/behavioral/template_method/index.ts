import fs from 'node:fs';

function stringFormat(fmt: string, values: { [key: string]: any }): string {
    return fmt.replace(
        /\{(\w+)\}/g,
        (_, key) => values[key]?.toString() ?? `{${key}}`,
    );
}

abstract class Logging {
    private readonly _name: string;

    constructor(name: string) {
        this._name = name;
    }

    public log(level: 'INFO' | 'WARN' | 'ERROR', message: string): void {
        this.preLog();
        const formattedMessage = this.buildFormattedLog(level, message);
        this.writeLog(formattedMessage);
    }

    protected buildFormattedLog(
        level: 'INFO' | 'WARN' | 'ERROR',
        message: string,
    ): string {
        const formattedMessage = this.formatMessage();
        const formatted = stringFormat(formattedMessage, {
            dt: new Date().toLocaleString(),
            level: level.padEnd(7),
            name: this._name,
            message: message,
        });
        return formatted;
    }

    protected preLog(): void {}
    protected abstract formatMessage(): string;
    protected abstract writeLog(message: string): void;
}

class StreamLogger extends Logging {
    protected override formatMessage(): string {
        return '{level} {name}: {message}';
    }

    protected override writeLog(message: string): void {
        console.log(message);
    }
}

class FileLogger extends Logging {
    private filename: string;

    constructor(name: string) {
        super(name);
        this.filename = `${name}.log`;
    }

    protected override formatMessage(): string {
        return '[{dt}] [{level}] {name}: {message}';
    }

    protected override preLog(): void {
        const fileIsExist = fs.existsSync(this.filename);
        if (!fileIsExist) {
            const time = new Date();
            try {
                fs.utimesSync(this.filename, time, time);
            } catch (_err) {
                fs.closeSync(fs.openSync(this.filename, 'w'));
            }
        }
    }

    protected override writeLog(message: string): void {
        const fileContent = fs.readFileSync(this.filename, 'utf8');
        fs.writeFileSync(this.filename, `${fileContent}\n${message}`);
    }
}

function clientCode(logger: Logging): void {
    logger.log('INFO', 'get user info');
    logger.log('ERROR', 'database lost connection');
}

function main(): void {
    const logs: Logging[] = [new StreamLogger('app'), new FileLogger('app')];

    for (const log of logs) {
        clientCode(log);
    }
}

main();

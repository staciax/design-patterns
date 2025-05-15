// command
interface ICommand {
    execute(): Promise<any>;
}

abstract class BaseCommand implements ICommand {
    abstract execute(): Promise<any>;
}

//

class AddReminderCommand implements BaseCommand {
    app: ReminderApp;
    reminder: Reminder;

    constructor(app: ReminderApp, reminder: Reminder) {
        this.app = app;
        this.reminder = reminder;
    }

    async execute() {
        return this.app.addReminder(this.reminder);
    }
}

class DeleteReminderCommand implements BaseCommand {
    app: ReminderApp;
    reminder: Reminder;

    constructor(app: ReminderApp, reminder: Reminder) {
        this.app = app;
        this.reminder = reminder;
    }

    async execute() {
        return this.app.removeReminder(this.reminder);
    }
}

// decorator

export abstract class CommandDecorator implements ICommand {
    protected command: ICommand;
    constructor(command: ICommand) {
        this.command = command;
    }

    async execute(): Promise<any> {
        return await this.command.execute();
    }

    getCommand() {
        return this.command;
    }
}

export class LoggerCommandDecorator extends CommandDecorator {
    override async execute() {
        const command = this.command;
        const date = new Date();
        console.log(
            `[${date.toISOString()}] Command executed: ${command.constructor.name}`,
        );
        return await super.execute();
    }
}

class TimerCommandDecorator extends CommandDecorator {
    override async execute() {
        const command = this.command;
        const start = performance.now();
        const result = await super.execute();
        const end = performance.now();

        const unwrapCommand = (command: ICommand): ICommand => {
            if (command instanceof CommandDecorator) {
                return unwrapCommand(command.getCommand());
            }
            return command;
        };
        const unwrappedCommand = unwrapCommand(command);

        console.log(
            `[TIMER] ${unwrappedCommand.constructor.name} took ${end - start}ms`,
        );
        return result;
    }
}

// Invoker

export class Invoker {
    private command: ICommand | null = null;

    setCommand(command: ICommand) {
        this.command = command;
    }

    async executeCommand() {
        if (!this.command) {
            console.log('Command not set');
            return;
        }
        return await this.command.execute();
    }
}

//

class Reminder {
    public title: string;
    public dueDate: Date | null;
    public readonly createdAt = new Date();

    constructor(title: string, dueDate: Date | null = null) {
        this.title = title;
        this.dueDate = dueDate;
    }

    getTitle() {
        return this.title;
    }

    setTitle(title: string) {
        this.title = title;
    }

    getdueDate() {
        return this.dueDate;
    }
}

// Receiver

export class ReminderApp {
    private reminders: Reminder[] = [];

    addReminder(reminder: Reminder) {
        this.reminders.push(reminder);
        return reminder;
    }

    removeReminder(reminder: Reminder) {
        const index = this.reminders.indexOf(reminder);
        if (index !== -1) {
            this.reminders.splice(index, 1);
            return true;
        }
        return false;
    }

    getReminders(): Reminder[] {
        return this.reminders;
    }
}

async function main() {
    const app = new ReminderApp();
    const invoker = new Invoker();

    const r1 = new Reminder('do design pattern', new Date('2025-04-09'));
    console.log('r1: ', r1.toString());

    const addReminderR1 = new AddReminderCommand(app, r1);
    const addReminderR1WithLog = new LoggerCommandDecorator(addReminderR1);
    invoker.setCommand(addReminderR1WithLog);
    await invoker.executeCommand();

    console.log('-'.repeat(30));

    const r2 = new Reminder('do homework', new Date('2025-03-01'));
    console.log('r2: ', r2.toString());
    const addReminderR2 = new AddReminderCommand(app, r2);
    const addReminderR2WithTimer = new TimerCommandDecorator(addReminderR2);
    invoker.setCommand(addReminderR2WithTimer);
    await invoker.executeCommand();

    console.log('-'.repeat(30));

    console.log('app reminders: ');
    app.getReminders().map((r) => {
        console.log('-', r.toString());
    });

    console.log('-'.repeat(30));

    console.log('delete r2: ');
    const deleteReminderCmd = new DeleteReminderCommand(app, r2);
    const deleteReminderCmdWithLog = new LoggerCommandDecorator(
        deleteReminderCmd,
    );
    const deleteReminderCmdWithTimer = new TimerCommandDecorator(
        deleteReminderCmdWithLog,
    );
    invoker.setCommand(deleteReminderCmdWithTimer);
    await invoker.executeCommand();

    console.log('-'.repeat(30));

    console.log('reminders: ');
    app.getReminders().map((r) => {
        console.log('-', r.toString());
    });
}

main();

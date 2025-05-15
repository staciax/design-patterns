import { getUsers } from './db';
// import { sendEmail } from './utils';

interface Publisher {
    subscribe(observer: Observer): void;
    unsubscribe(observer: Observer): void;
    notify(): void | Promise<void>;
}

interface Observer {
    update(publisher: Publisher): void | Promise<void>;
}

//

class EmailSubscriber {
    readonly email: string;

    constructor(email: string) {
        this.email = email;
    }

    async update(publisher: Publisher) {
        if (
            publisher instanceof AdPublisher &&
            publisher.subject.length &&
            publisher.content.length
        ) {
            // await sendEmail({
            //     email_to: this.email,
            //     subject: publisher.subject,
            //     htmlContent: publisher.content,
            // });
            console.log(`Sent email to ${this.email}`);
        }
    }
}

class AdPublisher implements Publisher {
    private observers: Observer[] = [];
    private _subject = '';
    private _content = '';

    get subject() {
        return this._subject;
    }
    set subject(value: string) {
        this._subject = value;
    }

    get content() {
        return this._content;
    }
    set content(value: string) {
        this._content = value;
    }

    subscribe(observer: Observer) {
        this.observers.push(observer);
    }

    unsubscribe(observer: Observer) {
        const observerIndex = this.observers.indexOf(observer);
        if (observerIndex === -1) {
            return;
        }
        this.observers.splice(observerIndex, 1);
    }

    async notify() {
        for (const observe of this.observers) {
            await observe.update(this);
        }
    }
}

const client = async () => {
    const adPublisher = new AdPublisher();

    const users = getUsers();
    console.log('users: ', users);

    const subscribers = [];

    for (const user of users) {
        const sub = new EmailSubscriber(user.email);
        adPublisher.subscribe(sub);

        subscribers.push(sub);
    }

    adPublisher.subject = '3.3 Month sale';
    adPublisher.content = '<h1>code: 123456<h1>';
    await adPublisher.notify();

    for (const sub of subscribers) {
        adPublisher.unsubscribe(sub);
    }
};

const main = async () => {
    await client();
};

await main();

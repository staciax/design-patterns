import crypto from 'node:crypto';

const settings = {
    ENCRYPTION_KEY: 'LOrG82NjxiRqZMyoBc1DynoBsU6y/MUy',
    TEXT_LENGTH: 1000,
    IMAGE_FILE_SIZE: 1024 * 1024 * 10, // 10MB
    VIDEO_FILE_SIZE: 1024 * 1024 * 25, // 25MB
};

export interface Message {
    accept<T>(visitor: MessageVisitor<T>): T;
}

export interface MessageVisitor<T = unknown> {
    visitTextMessage(message: TextMessage): T;
    visitImageMessage(message: ImageMessage): T;
    visitVideoMessage(message: VideoMessage): T;
}

export class TextMessage implements Message {
    public text: string;
    constructor(text: string) {
        this.text = text;
    }

    accept<T>(visitor: MessageVisitor<T>): T {
        return visitor.visitTextMessage(this);
    }
}

export class ImageMessage implements Message {
    public text: string;
    public file: Bun.BunFile;

    constructor(file: Bun.BunFile, caption = '') {
        this.text = caption;
        this.file = file;
    }

    accept<T>(visitor: MessageVisitor<T>): T {
        return visitor.visitImageMessage(this);
    }
}

export class VideoMessage implements Message {
    public text: string;
    public file: Bun.BunFile;

    constructor(file: Bun.BunFile, caption = '') {
        this.text = caption;
        this.file = file;
    }

    accept<T>(visitor: MessageVisitor<T>): T {
        return visitor.visitVideoMessage(this);
    }
}

type ValidationResult = {
    isValid: boolean;
    errors: string[];
};

class MessageValidator implements MessageVisitor<ValidationResult> {
    visitTextMessage(message: TextMessage): ValidationResult {
        const errors: string[] = [];

        if (!message.text) {
            errors.push('message text cannot be empty');
        }

        if (message.text && message.text.length > settings.TEXT_LENGTH) {
            errors.push('maximum length of 1000 characters');
        }

        return {
            isValid: errors.length === 0,
            errors: errors,
        };
    }

    visitImageMessage(message: ImageMessage): ValidationResult {
        const errors: string[] = [];

        if (!message.file) {
            errors.push('image file is required');
        } else {
            const validMimeTypes = [
                'image/jpeg',
                'image/jpg',
                'image/png',
                'image/gif',
            ];

            // @ts-ignore
            if (!validMimeTypes.includes(message.file.type)) {
                errors.push('invalid image file type');
            }

            // @ts-ignore
            if (message.file.size > settings.IMAGE_FILE_SIZE) {
                errors.push('image file size exceeds maximum of 10MB');
            }
        }

        if (message.text && message.text.length > 200) {
            errors.push(
                'image caption exceeds maximum length of 200 characters',
            );
        }

        return {
            isValid: errors.length === 0,
            errors,
        };
    }

    visitVideoMessage(message: VideoMessage): ValidationResult {
        const errors: string[] = [];

        if (!message.file) {
            errors.push('Video file is required');
        } else {
            const validMimeTypes = ['video/mp4', 'video/quicktime'];

            // @ts-ignore
            if (!validMimeTypes.includes(message.file.type)) {
                errors.push('invalid video file type');
            }

            // @ts-ignore
            if (message.file.size > settings.VIDEO_FILE_SIZE) {
                errors.push('video file size exceeds maximum of 25MB');
            }
        }

        if (message.text && message.text.length > 100) {
            errors.push(
                'Video caption exceeds maximum length of 100 characters',
            );
        }

        return {
            isValid: errors.length === 0,
            errors: errors,
        };
    }
}

export class MessageEncryptionVisitor implements MessageVisitor<Message> {
    private encryptionKey: Buffer;
    private algorithm = 'aes-256-cbc';

    constructor(encryptionKey: Buffer) {
        this.encryptionKey = encryptionKey;
    }

    visitTextMessage(message: TextMessage): TextMessage {
        const encryptedText = this.encryptText(message.text);
        return new TextMessage(encryptedText);
    }

    visitImageMessage(message: ImageMessage): ImageMessage {
        const encryptedCaption = this.encryptText(message.text);
        const encryptedFile = this.encryptFile(message.file);
        return new ImageMessage(encryptedFile, encryptedCaption);
    }

    visitVideoMessage(message: VideoMessage): VideoMessage {
        const encryptedCaption = this.encryptText(message.text);
        const encryptedFile = this.encryptFile(message.file);
        return new VideoMessage(encryptedFile, encryptedCaption);
    }

    private encryptText(text: string): string {
        const iv = crypto.randomBytes(16);
        const cipher = crypto.createCipheriv(
            this.algorithm,
            this.encryptionKey,
            iv,
        );
        let encrypted = cipher.update(text, 'utf8', 'hex');
        encrypted += cipher.final('hex');
        return `${iv.toString('hex')}:${encrypted}`;
    }

    private encryptFile(file: Bun.BunFile): Bun.BunFile {
        return file;
    }
}

class App {
    private validator: MessageValidator;
    private encryption: MessageEncryptionVisitor;

    constructor(encryptionKey: string) {
        this.validator = new MessageValidator();
        this.encryption = new MessageEncryptionVisitor(
            Buffer.from(encryptionKey),
        );
    }

    validateBeforeSend(message: Message): boolean {
        const result = message.accept(this.validator);
        if (!result.isValid) {
            console.log('validation errors:', result.errors);
        }
        return result.isValid;
    }

    encryptMessage(message: Message): Message {
        return message.accept(this.encryption);
    }

    sendMessage(message: Message): void {
        if (this.validateBeforeSend(message)) {
            const encryptedMessage = this.encryptMessage(message);
            console.log('sent message: ', encryptedMessage);
        }
    }
}

export function main() {
    const app = new App(settings.ENCRYPTION_KEY);

    const messages: Message[] = [
        new TextMessage('hi luna'),
        new ImageMessage(Bun.file('./assets/avatar.png')),
        // new VideoMessage(Bun.file('./assets/test.mov')),
    ];

    for (const message of messages) {
        app.sendMessage(message);
        console.log('-'.repeat(50));
    }
}

main();

abstract class ScreenRecordingState {
    // @ts-ignore
    protected app: App;

    public setContext(app: App) {
        this.app = app;
    }

    public abstract startRecording(): void;
    public abstract pauseRecording(): void;
    public abstract stopRecording(): void;
}

class IdleState extends ScreenRecordingState {
    public startRecording() {
        console.log('starting screen recording...');
        this.app.setState(new RecordingState());
    }

    public pauseRecording() {
        console.log('cannot pause, recording has not started');
    }

    public stopRecording() {
        console.log('cannot stop, recording has not started');
    }
}

class RecordingState extends ScreenRecordingState {
    public startRecording() {
        console.log('already recording');
    }

    public pauseRecording() {
        console.log('pausing screen recording...');
        this.app.setState(new PausedState());
    }

    public stopRecording() {
        console.log('stopping screen recording...');
        this.app.setState(new IdleState());
    }
}

class PausedState extends ScreenRecordingState {
    public startRecording() {
        console.log('resuming screen recording...');
        this.app.setState(new RecordingState());
    }

    public pauseRecording() {
        console.log('already paused');
    }

    public stopRecording() {
        console.log('stopping screen recording...');
        this.app.setState(new IdleState());
    }
}

class App {
    // @ts-ignore
    private state: ScreenRecordingState;

    constructor() {
        this.setState(new IdleState());
    }

    public setState(state: ScreenRecordingState) {
        console.log(`app: transition to ${state.constructor.name}.`);
        this.state = state;
        this.state.setContext(this);
    }

    public startRecording() {
        this.state.startRecording();
    }

    public pauseRecording() {
        this.state.pauseRecording();
    }

    public stopRecording() {
        this.state.stopRecording();
    }
}

function main() {
    const app = new App();

    app.startRecording();
    app.pauseRecording();
    app.startRecording();
    app.stopRecording();

    console.log('-'.repeat(10));

    app.startRecording();
    app.stopRecording();
}

main();

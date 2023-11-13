from .core.executor import execute_command
from .core.interpretation import CommandInterpreter
from .core.recognition import Model
from .core.voice_activity_detection import VADetector
from .dataclasses import Command, Interaction


class Assistant:
    def __init__(
        self, wake_word: str, commands: list[Command], model_path: str, verbose=False
    ) -> None:
        self.commands = commands
        self.verbose = verbose

        self.vad = VADetector()
        self.model = Model(model_path)
        self.interpreter = CommandInterpreter(self.commands, wake_word)

        self._awake = False

    @property
    def is_awake(self):
        return self._awake

    def run(self):
        for segment in self.vad.listen():
            self.on_voice_activity_detection(segment)
            transcription = self.model.transcribe(segment)
            self.on_transcription(transcription)
            if self._awake:
                if command := self.interpreter.associate(transcription):
                    self.on_command(command)
                    execute_command(command, on_interaction=self.on_interaction)
                    self._awake = False
                else:
                    self.on_no_associated_command()
            else:
                if self.interpreter.is_wake_word(transcription):
                    self.on_awake()
                    self._awake = True

    def on_voice_activity_detection(self, segment: bytes):
        if self.verbose:
            print("Detected Voice.")

    def on_transcription(self, transcription: str):
        if self.verbose:
            print(f"Transcribed: {transcription}.")

    def on_command(self, command: Command):
        if self.verbose:
            print(f"Executing Command: {command.identifier}.")

    def on_no_associated_command(self):
        if self.verbose:
            print(f"Couldn't associate transcription with command.")

    def on_interaction(self, interaction: Interaction):
        if self.verbose:
            print(f"Started interaction with text: {interaction.text}.")

    def on_awake(self):
        if self.verbose:
            print("Assistant just woke up.")
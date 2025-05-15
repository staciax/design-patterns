from __future__ import annotations

import io
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, override

from matplotlib import pyplot as plt
from PIL import Image, ImageFilter


class Memento(ABC):
    @abstractmethod
    def get_image(self) -> Image.Image: ...

    @property
    @abstractmethod
    def saved_at(self) -> datetime: ...


class ImageMemento(Memento):
    def __init__(self, image: Image.Image) -> None:
        self.image_data = io.BytesIO()
        image.save(self.image_data, format='PNG')
        self.image_data.seek(0)
        self._saved_at = datetime.now()

    @override
    def get_image(self) -> Image.Image:
        return Image.open(io.BytesIO(self.image_data.getvalue()))

    @property
    @override
    def saved_at(self) -> datetime:
        return self._saved_at


class Caretaker:
    def __init__(self, originator: Originator) -> None:
        self._mementos: list[Memento] = []
        self._originator = originator

    def backup(self) -> None:
        print("\nCaretaker: saving originator's state...")
        memento = self._originator.save()
        self._mementos.append(memento)

    def undo(self) -> None:
        if not len(self._mementos):
            return

        memento = self._mementos.pop()
        print(
            f'Caretaker: restoring state to: {memento.get_image()} saved_at: {memento.saved_at.strftime("%Y-%m-%d %H:%M:%S")}'
        )
        try:
            self._originator.restore(memento)
        except Exception:
            self.undo()

    def show_history(self) -> None:
        print("Caretaker: Here's the list of mementos:")
        for memento in self._mementos:
            print(memento, f'saved_at: {memento.saved_at.strftime("%Y-%m-%d %H:%M:%S")}')


class Originator(ABC):
    @abstractmethod
    def save(self) -> Any: ...

    @abstractmethod
    def restore(self, memento: Memento) -> None: ...


class ImageEditor(Originator):
    def __init__(self, image_path: str) -> None:
        self.image_path = image_path
        self.image = Image.open(image_path)

    @override
    def save(self) -> ImageMemento:
        return ImageMemento(self.image)

    @override
    def restore(self, memento: Memento) -> None:
        self.image = memento.get_image()  # type: ignore[assignment]

    def add_filter(self, pil_filter: ImageFilter) -> None:  # type: ignore[valid-type]
        self.image = self.image.filter(pil_filter)  # type: ignore[assignment]

    def to_gray_scale(self) -> None:
        self.image = self.image.convert('L')  # type: ignore[assignment]

    def show(self) -> None:
        plt.axis('off')
        plt.imshow(self.image, cmap='gray')
        plt.show()

    def to_file(self, filename: str) -> None:
        self.image.save(filename)

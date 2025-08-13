from __future__ import annotations

import io
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, override

from matplotlib import pyplot as plt
from PIL import Image, ImageFilter


class Memento(ABC):
    @abstractmethod
    def restore(self) -> Any: ...


class ImageMemento(Memento):
    def __init__(self, originator: ImageEditor, image: Image.Image) -> None:
        self.originator = originator
        self.image_data = io.BytesIO()
        image.save(self.image_data, format='PNG')
        self.image_data.seek(0)
        self._saved_at = datetime.now()

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} saved_at={self._saved_at.strftime("%Y-%m-%d %H:%M:%S")!r}>'

    @override
    def restore(self) -> None:
        img = Image.open(io.BytesIO(self.image_data.getvalue()))
        self.originator.set_image(img)


class Originator(ABC):
    @abstractmethod
    def save(self) -> Any: ...


class Caretaker:
    def __init__(self) -> None:
        self._mementos: list[Memento] = []

    def save(self, memento: Memento) -> None:
        self._mementos.append(memento)

    def undo(self) -> None:
        if not len(self._mementos):
            return
        self._mementos.pop().restore()

    def show_history(self) -> None:
        print("Caretaker: Here's the list of mementos:")
        for memento in self._mementos:
            print(memento)


class ImageEditor(Originator):
    def __init__(self, image_path: str) -> None:
        self.image_path = image_path
        self.image = Image.open(image_path)

    @override
    def save(self) -> ImageMemento:
        return ImageMemento(self, self.image)

    def set_image(self, image: Image.Image) -> None:
        self.image = image  # type: ignore[assignment]

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

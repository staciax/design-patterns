from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override


class EquipmentFactory(ABC):
    @abstractmethod
    def create_sword(self) -> Sword: ...

    @abstractmethod
    def create_armor(self) -> Armor: ...

    @abstractmethod
    def create_shield(self) -> Shield: ...


# -


class FireFactory(EquipmentFactory):
    @override
    def create_sword(self) -> Sword:
        return FireSword()

    @override
    def create_armor(self) -> Armor:
        return FireArmor()

    @override
    def create_shield(self) -> Shield:
        return FireShield()


class WaterFactory(EquipmentFactory):
    @override
    def create_sword(self) -> Sword:
        return WaterSword()

    @override
    def create_armor(self) -> Armor:
        return WaterArmor()

    @override
    def create_shield(self) -> Shield:
        return WaterShield()


class WindFactory(EquipmentFactory):
    @override
    def create_sword(self) -> Sword:
        return WindSword()

    @override
    def create_armor(self) -> Armor:
        return WindArmor()

    @override
    def create_shield(self) -> Shield:
        return WindShield()


# -


class Sword(ABC):
    @abstractmethod
    def wear(self) -> str: ...

    @abstractmethod
    def remove(self) -> str: ...

    @abstractmethod
    def attack(self) -> str: ...


class Armor(ABC):
    @abstractmethod
    def wear(self) -> str: ...

    @abstractmethod
    def remove(self) -> str: ...


class Shield(ABC):
    @abstractmethod
    def wear(self) -> str: ...

    @abstractmethod
    def remove(self) -> str: ...


# sword


class FireSword(Sword):
    @override
    def wear(self) -> str:
        return 'FireSword is worn'

    @override
    def remove(self) -> str:
        return 'FireSword is removed'

    @override
    def attack(self) -> str:
        return 'FireSword is attacking'


class WaterSword(Sword):
    @override
    def wear(self) -> str:
        return 'WaterSword is worn'

    @override
    def remove(self) -> str:
        return 'WaterSword is removed'

    @override
    def attack(self) -> str:
        return 'WaterSword is attacking'


class WindSword(Sword):
    @override
    def wear(self) -> str:
        return 'WindSword is worn'

    @override
    def remove(self) -> str:
        return 'WindSword is removed'

    @override
    def attack(self) -> str:
        return 'WindSword is attacking'


# armor


class FireArmor(Armor):
    @override
    def wear(self) -> str:
        return 'FireArmor is worn'

    @override
    def remove(self) -> str:
        return 'FireArmor is removed'


class WaterArmor(Armor):
    @override
    def wear(self) -> str:
        return 'WaterArmor is worn'

    @override
    def remove(self) -> str:
        return 'WaterArmor is removed'


class WindArmor(Armor):
    @override
    def wear(self) -> str:
        return 'WindArmor is worn'

    @override
    def remove(self) -> str:
        return 'WindArmor is removed'


# shield


class FireShield(Shield):
    @override
    def wear(self) -> str:
        return 'FireShield is worn'

    @override
    def remove(self) -> str:
        return 'FireShield is removed'


class WaterShield(Shield):
    @override
    def wear(self) -> str:
        return 'WaterShield is worn'

    @override
    def remove(self) -> str:
        return 'WaterShield is removed'


class WindShield(Shield):
    @override
    def wear(self) -> str:
        return 'WindShield is worn'

    @override
    def remove(self) -> str:
        return 'WindShield is removed'


# -


def client(factory: EquipmentFactory) -> None:
    sword = factory.create_sword()
    armor = factory.create_armor()
    shield = factory.create_shield()

    print(sword.wear())
    print(sword.attack())
    print(sword.remove())

    print(armor.wear())
    print(armor.remove())

    print(shield.wear())
    print(shield.remove())


def main() -> None:
    fire_factory = FireFactory()
    client(fire_factory)

    print('-' * 20)

    water_factory = WaterFactory()
    client(water_factory)

    print('-' * 20)

    wind_factory = WindFactory()
    client(wind_factory)


if __name__ == '__main__':
    main()

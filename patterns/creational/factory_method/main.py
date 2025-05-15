from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override


class JobSelector(ABC):
    @abstractmethod
    def get_job(self) -> Job: ...

    def select_job(self) -> list[str]:
        job = self.get_job()

        return job.get_quests()


class ArcherQuest(JobSelector):
    @override
    def get_job(self) -> Archer:
        return Archer()


class SwordsmanQuest(JobSelector):
    @override
    def get_job(self) -> Swordsman:
        return Swordsman()


class MageQuest(JobSelector):
    @override
    def get_job(self) -> Mage:
        return Mage()


class Job(ABC):
    @abstractmethod
    def get_quests(self) -> list[str]: ...


class Archer(Job):
    @override
    def get_quests(self) -> list[str]:
        return ['Archer quest 1', 'Archer quest 2', 'Archer quest 3']


class Swordsman(Job):
    @override
    def get_quests(self) -> list[str]:
        return ['Swordsman quest 1', 'Swordsman quest 2', 'Swordsman quest 3']


class Mage(Job):
    @override
    def get_quests(self) -> list[str]:
        return ['Mage quest 1', 'Mage quest 2', 'Mage quest 3']


# def client(job_selector: JobSelector) -> None:
#     job_quests = job_selector.select_job()


def main() -> None:
    archer_quest = ArcherQuest()
    archer_job_quests = archer_quest.select_job()
    print('archer quest:', archer_job_quests)

    swordsman_quest = SwordsmanQuest()
    swordsman_job_quests = swordsman_quest.select_job()
    print('swordsman quest:', swordsman_job_quests)

    mage_quest = MageQuest()
    mage_job_quests = mage_quest.select_job()
    print('mage quest:', mage_job_quests)


if __name__ == '__main__':
    main()

from abc import ABC, abstractmethod
from typing import Set


class IdGenerator(ABC):

    @abstractmethod
    def get_id(self, i: int):
        pass


class IdKeeper(IdGenerator):

    def __init__(self, ids: Set[int]):
        self._id_map: dict[int, int] = dict()
        self._missing = [i for i in range(1, len(ids)) if i not in ids]
        self._max = max(ids) + 1

    def _gen_new_id(self):
        if self._missing:
            return self._missing.pop(0)

        i = self._max
        self._max += 1
        return i

    def get_id(self, i: int):
        if i > 0:
            return i

        if i in self._id_map:
            return self._id_map[i]

        new_id = self._gen_new_id()
        self._id_map[i] = new_id
        return new_id


class IdCounter(IdGenerator):

    def __init__(self):
        self._id_map: dict[int, int] = dict()
        self._id_count = 1

    def get_id(self, i: int):
        if i in self._id_map:
            return self._id_map[i]
        else:
            new_id = self._id_count
            self._id_map[i] = new_id
            self._id_count += 1
            return new_id

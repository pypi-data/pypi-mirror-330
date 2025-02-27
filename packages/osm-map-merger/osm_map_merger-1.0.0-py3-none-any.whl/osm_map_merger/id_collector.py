from typing import Set

import osmium
from osmium import osm

from .id_generator import IdKeeper, IdGenerator
from .util import get_action_delete_ids


class IdCollector(osmium.SimpleHandler):

    def __init__(self):
        super().__init__()
        self._ids: set[int] = set()
        self._action_delete: Set[int] = set()

    def collect(self, filename: str) -> IdGenerator:
        self._action_delete = get_action_delete_ids(filename)
        self.apply_file(filename)
        return IdKeeper(self._ids)

    def _add_id(self, i: int):
        self._ids.add(i)

    def node(self, n: osm.Node):
        if n.id in self._action_delete:
            return

        self._add_id(n.id)

    def way(self, w: osm.Way):
        if w.id in self._action_delete:
            return

        for node in w.nodes:
            if node.ref not in self._action_delete:
                self._add_id(node.ref)

        self._add_id(w.id)

    def relation(self, r: osm.Relation):
        if r.id in self._action_delete:
            return

        for tup in r.members:
            if tup.ref not in self._action_delete:
                self._add_id(tup.ref)

        self._add_id(r.id)

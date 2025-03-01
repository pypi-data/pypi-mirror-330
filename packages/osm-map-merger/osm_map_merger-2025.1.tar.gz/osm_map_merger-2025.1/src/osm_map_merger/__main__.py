import os
from typing import Dict, Set

import click
import osmium
from osmium import osm

from .id_collector import IdCollector
from .id_generator import IdCounter, IdGenerator
from .util import get_action_delete_ids, get_version, get_visible


class MapHandler(osmium.SimpleHandler):

    @staticmethod
    def apply_fill(file: str, writer: osmium.SimpleWriter):
        id_keeper = IdCollector()
        id_gen = id_keeper.collect(file)
        MapHandler(writer, id_gen).apply_file(file)

    @staticmethod
    def apply_redistribute(files: [str], writer: osmium.SimpleWriter):
        id_gen = IdCounter()
        for f in files:
            MapHandler(writer, id_gen).apply_file(f)

    def __init__(self, writer: osmium.SimpleWriter, id_gen: IdGenerator):
        super().__init__()
        self._writer = writer
        self._id_map: Dict[int, int] = dict()
        self._action_delete: Set[int] = set()
        self._id_gen = id_gen

    def apply_file(self, filename, locations=False, idx='flex_mem'):
        self._action_delete = get_action_delete_ids(filename)
        super().apply_file(filename, locations, idx)

    def _get_id(self, i: int):
        return self._id_gen.get_id(i)

    def node(self, n: osm.Node):
        if n.id in self._action_delete:
            return

        n = n.replace(id=self._get_id(n.id),
                      version=get_version(n.version),
                      visible=get_visible(n.visible))
        self._writer.add_node(n)

    def way(self, w: osm.Way):
        if w.id in self._action_delete:
            return

        nodes = [] if not w.nodes else [self._get_id(int(n.ref)) for n in w.nodes if
                                        n.ref not in self._action_delete]
        w = w.replace(id=self._get_id(w.id),
                      nodes=nodes,
                      version=get_version(w.version),
                      visible=get_visible(w.visible))
        self._writer.add_way(w)

    def relation(self, r: osm.Relation):
        if r.id in self._action_delete:
            return

        members = [] if not r.members else [(t.type, self._get_id(t.ref), t.role) for t in r.members if
                                            t.ref not in self._action_delete]
        r = r.replace(id=self._get_id(r.id),
                      members=members,
                      version=get_version(r.version),
                      visible=get_visible(r.visible))
        self._writer.add_relation(r)


@click.command()
@click.option("--input", "-i", "input_", multiple=True, required=True, help="One or more input files.")
@click.option("--output", "-o", "output", multiple=False, required=True, help="The output file.")
@click.option("--force", "-f", is_flag=True, help="Override the output file.")
@click.option("--redistribute", "-r", "redist", is_flag=True, help="Input files will be merged and id's will be "
                                                                   "redistributed starting from one. [default]")
@click.option("--keep", "-k", "keep", is_flag=True, help="Convert negative id's but keep original positive id's. "
                                                         "Allows only one input file.")
def cmd(input_, output, force, redist, keep):
    usage = "Usage: map_merger.py [OPTIONS]\nTry 'map_merger.py --help' for help.\n\n"

    if redist and keep:
        print(usage + "Error: Options --redistribute "
                      "and --keep are mutual exclusive.")
        return

    if keep and len(input_) > 1:
        print(usage + "Error: Option --keep only "
                      "allows one input file.")
        return

    if os.path.isfile(output):
        if force:
            os.remove(output)
        else:
            print(usage + "Error: File already "
                          "exists. Use --force to override the output file.")
            return

    writer = osmium.SimpleWriter(output)

    if keep:
        MapHandler.apply_fill(input_[0], writer)
    else:
        MapHandler.apply_redistribute(input_, writer)
    writer.close()


if __name__ == "__main__":
    cmd()

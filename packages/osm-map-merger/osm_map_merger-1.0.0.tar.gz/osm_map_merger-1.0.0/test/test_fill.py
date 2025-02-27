import os
import tempfile

import osmium
import pytest
import subprocess
import logging

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def temp_folder() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory()


def execute_cmd(cmd: str):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, cwd=os.getcwd())
    output, error = process.communicate()
    return output, error


class _TestNodeFill(osmium.SimpleHandler):

    def node(self, n: osmium.Node):
        assert n.version == n.id


@pytest.mark.parametrize("keep", ["--keep", "-k"])
def test_keep(keep: str, temp_folder):
    temp_file = temp_folder.name + "/out.osm"
    LOGGER.info(temp_file)
    cmd = f"osm-map-merger -i data/test_fill.osm -o {temp_file} {keep} -f"
    o, e = execute_cmd(cmd)

    assert o == b'', o
    assert e is None

    tnf = _TestNodeFill()
    tnf.apply_file(temp_file)

# Todo: Add positive tests for ways, relations, override, redistribute
# Todo: Add Stresstest
# Todo: Add negative tests
# Todo: Make tests more atomic

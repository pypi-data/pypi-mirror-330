from typing import Set

from bs4 import BeautifulSoup


def get_version(version) -> int:
    if type(version) is not int or version < 1:
        return 1
    return version


def get_visible(visible) -> bool:
    if type(visible) is not bool:
        return True
    return visible


def get_action_delete_ids(file: str) -> Set[int]:
    with open(file, "r") as f:
        return {int(child.attrs["id"]) for child in BeautifulSoup(f.read(), "xml").findChildren() if
                "action" in child.attrs and child.attrs["action"] == "delete"}

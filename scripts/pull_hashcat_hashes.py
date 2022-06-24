#!/usr/bin/env python3

from argparse import ArgumentParser
from datetime import datetime
from json import JSONEncoder
from os import stat
from pathlib import Path
from typing import Any, NamedTuple, Set
from urllib.request import urlopen
from collections import namedtuple
from json import dumps as j_dumps
from bs4 import BeautifulSoup


class HashJSONParser(JSONEncoder):
    def default(self, o: Any) -> Any:
        # if isinstance(o, tuple):
        #     try:
        #         o.hash
        #     except AttributeError:
        #         pass
        #     else:
        #         return {
        #             "hash_name": o.name,
        #             "hashcat_mode": o.mode,
        #             "hash_example": o.hash,
        #         }
        # elif isinstance(o, set):
        if isinstance(o, set):
            return list(o)
        return super().default(o)


class HashTyping(NamedTuple):
    name: str
    mode: str
    hash: str


def parse_args() -> ArgumentParser:
    """
    handle all the arguement parsing for the script
    """
    parser = ArgumentParser(
        description="""
            grab all the example hashes and 
        """,
    )


def _get_hashcat_example_hashes() -> Set[HashTyping]:
    url = "https://hashcat.net/wiki/doku.php?id=example_hashes"
    soup = BeautifulSoup(urlopen(url).read(), features="html.parser")

    filters = {"hashcat", "tbd", "n/a"}
    hash_collection = set()
    hash_type = namedtuple("HashType", ["name", "mode", "hash"])

    for raw_hash in soup.find_all("td", class_="col2"):
        hash_str = raw_hash.get_text().strip()
        if (hash_str.lower() not in filters) and not hash_str.startswith("https://"):
            hash_name = raw_hash.previous_sibling.get_text().strip()
            hashcat_mode = raw_hash.previous_sibling.previous_sibling.get_text().strip()
            hash_collection.add(hash_type(hash_name, hashcat_mode, hash_str))

    return hash_collection


# pylint: disable=missing-function-docstring
def main():

    print(j_dumps(_get_hashcat_example_hashes(), cls=HashJSONParser, indent=2))
    # tmpz = Path("data/hashcat_hashes.txt")
    # print(datetime.fromtimestamp(stat(tmpz).st_mtime))


if __name__ == "__main__":
    main()

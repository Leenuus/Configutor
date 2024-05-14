#!/usr/bin/env python

from tree_sitter import Language, Parser, Node, Query
from icecream import ic
from glob import glob
from pathlib import Path

from os import environ
import sys

HOME = environ["HOME"]

DEBUG = environ.get("DEBUG", False)

# path_or_ptr -> Lang
LANGS = {}
parsers = glob("./parsers/*.so")
for p in parsers:
    p = Path(p)
    name = p.stem
    lang = Language(p, p.stem)
    LANGS[name] = lang
# ic(LANGS)


"""
filename -> src
filename -> langauge name

parser -> Lang -> src -> tree

query_src -> Lang -> query
tree -> query -> profile
"""


QUERY_SRC = """
(program
(comment) @comments
)
"""


def guess_lang(file: Path | str) -> str:
    if isinstance(file, str):
        file = Path(file)
    if file.suffix:
        return file.suffix[1:]
    else:
        raise ValueError("Can't get src code langauge")


def new_tree_root(src: bytes | str, lang: str | Language):
    if isinstance(src, str):
        src = src.encode()
    parser = Parser()
    if isinstance(lang, str):
        lang = LANGS[lang]
    parser.set_language(lang)
    return parser.parse(src).root_node


# query_src -> Lang -> query
def new_query(lang: str | Language, query_src: str = QUERY_SRC):
    if isinstance(lang, str):
        lang = LANGS[lang]
    return lang.query(query_src)


# tree -> query -> profiles
def export_profiles(tree_root: Node, query: Query):
    comments = query.captures(tree_root)
    profiles = {}
    profiles["default"] = []
    for c in comments:
        node = c[0]
        if b"EXPORT" not in node.text:
            continue
        # modline = node.text
        # parse_modline(modline, node)
        content = node.next_named_sibling
        if content is not None:
            if DEBUG:
                ic(content.text)
            profiles["default"].append(content.text)
    return profiles


# tree -> query -> profile
def _parse_modline(tree_root: Node, node: Node):
    """
    TODO:
    # EXPORT: default, kali, debian
    """
    pass


def main():
    files = glob(f"{HOME}/.config/fish/conf.d/*.fish")

    artifact = {}
    for file in files:
        # file = "./fish/alias.fish"
        with open(file, "rb") as f:
            src = f.read()
        if DEBUG:
            print(f"------------{file}-----------", file=sys.stderr)
        lang = guess_lang(file)
        tree_root = new_tree_root(src, lang)
        q = new_query(lang)
        profiles = export_profiles(tree_root, q)
        if DEBUG:
            ic(profiles)
        for p_name, p_content in profiles.items():
            artifact.setdefault(p_name, list()).extend(p_content)
        if DEBUG:
            print("------------\n\n", file=sys.stderr)

    build = Path("./build")
    if not build.exists():
        build.mkdir()
    for p_name, p_content in artifact.items():
        if DEBUG:
            print(f"------------{p_name}-----------", file=sys.stderr)
            ic(p_content)
            print("------------\n\n", file=sys.stderr)
        with open(build / (p_name + ".fish"), "wb") as f:
            f.write(b"\n\n".join(p_content))


if __name__ == "__main__":
    main()

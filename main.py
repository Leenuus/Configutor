#!/usr/bin/env python

"""
filename -> src
filename -> langauge name
parser -> Lang -> src -> tree
query_src -> Lang -> query
tree -> query -> profile
"""

from tree_sitter import Language, Parser, Node, Query
from icecream import ic
from glob import glob
from pathlib import Path
from typing import Callable

from os import environ
import sys

HOME = environ["HOME"]

DEBUG = environ.get("DEBUG", False)

LANGS = {}
parsers = glob("./parsers/*.so")
for p in parsers:
    p = Path(p)
    name = p.stem
    lang = Language(p, p.stem)
    LANGS[name] = lang

LANGS["sh"] = LANGS["bash"]


FISH_QUERY_SRC = """
(program
(comment) @comments
)
"""

LUA_QUERY_SRC = """
(chunk
(comment) @comments
)
"""

BASH_QUERY_SRC = """
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
def new_query(lang: str | Language, query_src: str = FISH_QUERY_SRC):
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
        content = node.next_named_sibling
        if content is not None:
            if DEBUG:
                ic(content.text)
            profiles["default"].append(content.text)
    return profiles


def build_file(file: str | Path, artifact: dict = None, query_src: str = None):
    if artifact is None:
        artifact = {}
    with open(file, "rb") as f:
        src = f.read()
    if DEBUG:
        print(f"------------{file}-----------", file=sys.stderr)
    lang = guess_lang(file)
    tree_root = new_tree_root(src, lang)
    if query_src is None:
        if lang == "fish":
            query_src = FISH_QUERY_SRC
        elif lang == "lua":
            query_src = LUA_QUERY_SRC
        else:
            raise ValueError("Can't figure out which query string to use")
    q = new_query(lang, query_src)

    profiles = export_profiles(tree_root, q)
    if DEBUG:
        ic(profiles)
    for p_name, p_content in profiles.items():
        artifact.setdefault(p_name, list()).extend(p_content)
    if DEBUG:
        print("------------\n\n", file=sys.stderr)
    return artifact


def build_fish_profiles(
    files: str | list = "/home/leenuus/Dotfiles/.config/fish/conf.d/*.fish",
    query_src: str = FISH_QUERY_SRC,
    transform: Callable | None = None,
):
    if isinstance(files, str):
        files = glob(files)
    else:
        files = [glob(file) for file in files]
    artifact = {}
    for file in files:
        build_file(file, artifact, query_src)

    OUTPUT = Path("./build/fish")
    if not OUTPUT.exists():
        OUTPUT.mkdir(parents=True)

    for p_name, p_content in artifact.items():
        if DEBUG:
            print(f"------------{p_name}-----------", file=sys.stderr)
            ic(p_content)
            print("------------\n\n", file=sys.stderr)
        with open(OUTPUT / (p_name + ".fish"), "wb") as f:
            f.write(b"\n\n".join(p_content))


def build_lua_profiles(
    files: str | list = "/home/leenuus/Dotfiles/.config/nvim/**/*.lua",
    query_src: str = LUA_QUERY_SRC,
    transform: Callable | None = None,
):
    if isinstance(files, str):
        files = glob(files)
    else:
        files = [glob(file) for file in files]
    files.append(files[0])
    files[0] = "/home/leenuus/Dotfiles/.config/nvim/init.lua"
    artifact = {}
    for file in files:
        build_file(file, artifact, query_src)

    OUTPUT = Path("./build/lua")
    if not OUTPUT.exists():
        OUTPUT.mkdir(parents=True)

    for p_name, p_content in artifact.items():
        if DEBUG:
            print(f"------------{p_name}-----------", file=sys.stderr)
            ic(p_content)
            print("------------\n\n", file=sys.stderr)

        profile = b"\n\n".join(p_content)
        if transform is not None:
            ic(profile)
            profile = transform(profile)

        with open("./single-file-version.lua", "rb") as f:
            nvim_tmux_navigator = f.read()

        profile = profile + nvim_tmux_navigator

        with open(OUTPUT / (p_name + ".lua"), "wb") as f:
            f.write(profile)


def build_bash_profiles(
    files: list | str = "/home/leenuus/.config/bashrc.d/*.sh",
    query_src: str = BASH_QUERY_SRC,
    transform: Callable | None = None,
):
    if isinstance(files, str):
        files = glob(files)
    else:
        files = [glob(file) for file in files]

    artifact = {}
    for file in files:
        build_file(file, artifact, query_src)

    OUTPUT = Path("./build/bash")
    if not OUTPUT.exists():
        OUTPUT.mkdir(parents=True)

    for p_name, p_content in artifact.items():
        if DEBUG:
            print(f"------------{p_name}-----------", file=sys.stderr)
            ic(p_content)
            print("------------\n\n", file=sys.stderr)
        with open(OUTPUT / (p_name + ".sh"), "wb") as f:
            f.write(b"\n\n".join(p_content))


def main():
    build_lua_profiles()
    build_fish_profiles()
    build_bash_profiles()


if __name__ == "__main__":
    main()

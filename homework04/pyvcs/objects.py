import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find

def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0"
    sum = header.encode() + data
    sha = hashlib.sha1(sum).hexdigest()
    if write == True:
        gitdir = repo_find()
        if (not os.path.exists(gitdir / "objects" / sha[:2])):
            pathlib.Path(gitdir / "objects" / sha[:2]).mkdir()
        if (not os.path.exists(gitdir / "objects" / sha[:2] / sha[2:])):
            pathlib.Path(gitdir / "objects" / sha[:2] / sha[2:]).touch()
        with (pathlib.Path(gitdir / "objects" / sha[:2]) / sha[2:]).open("wb") as f:
            f.write(zlib.compress(sum))
            f.close()
    return (sha)

def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if len(obj_name) not in range(4, 41) or not os.path.isdir(gitdir / "objects" / obj_name[0:2]):
        raise AssertionError(f"Not a valid object name {obj_name}")
    current_dir = gitdir / "objects" / obj_name[0:2]
    end = obj_name[2:]
    result = []
    for files in os.listdir(current_dir):
        if os.path.isfile(current_dir / files) and files == end or files[0:len(end)] == end:
            result.append(obj_name[0:2] + files)
    if len(result) == 0:
        raise AssertionError(f"Not a valid object name {obj_name}")
    return result

def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    return resolve_object(obj_name, gitdir)[0]

def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = find_object(sha, gitdir)
    file = open(gitdir / "objects" / path[0:2] / path[2:], "rb")
    data = zlib.decompress(file.read())
    start = data.find(b" ")
    end = data.find(b"\x00")
    lenght = int(data[start:end].decode("ascii"))
    content = data[end + 1:]
    fmt = data[:start].decode()
    file.close()
    return fmt, content

def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    tree = []
    while len(data) > 0:
        mode = data[:6].decode()
        st_sha = data.find(b"\00")
        if mode == "100644":
            name = data[7:st_sha]
            sha = data[st_sha + 1:st_sha + 21].hex()
            tree.append((100644, name.decode(), sha))
            data = data[st_sha + 21:]
        else:
            name = data[6:st_sha]
            sha = data[st_sha + 1:st_sha + 21].hex()
            tree.append((40000, name.decode(), sha))
            data = data[st_sha + 21:]
    return tree

def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find()
    fmt, data = read_object(obj_name, gitdir)
    if fmt == "blob" or fmt == "commit":
        print(data.decode())
    else:
        result = ""
        for tree in read_tree(data):
            result += str(tree[0]).zfill(6) + " "
            if tree[0] == 100644:
                result += "blob "
            else:
                result += "tree "
            result += tree[2] + "\t"
            result += tree[1] + "\n"
        print(result)

def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    fmt, content = read_object(tree_sha, gitdir)
    objects = read_tree(content)
    result = []
    for tree in objects:
        if tree[0] == 100644:
            result.append((tree[1], tree[2]))
        else:
            sub_objects = find_tree_files(tree[2], gitdir)
            for ob in sub_objects:
                result.append((tree[1] + "/" + ob[0], ob[1]))
    return result

def commit_parse(raw: bytes, start: int = 0, dct=None):
    ...
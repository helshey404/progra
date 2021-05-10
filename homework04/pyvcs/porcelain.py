import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object, read_tree
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree

def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)

def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    commit_sha = commit_tree(gitdir, write_tree(gitdir, read_index(gitdir)), message, author=author)
    if is_detached(gitdir):
        ref = gitdir / "HEAD"
    else:
        ref = pathlib.Path(get_ref(gitdir))
    f = open(gitdir / ref, "w")
    f.write(commit_sha)
    f.close()
    return commit_sha

def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    getref = get_ref(gitdir)
    if os.path.isfile(gitdir / getref):
        branch_head = open(gitdir / getref, "r")
        getref = branch_head.read()
        branch_head.close()
    fmt, content1 = read_object(getref, gitdir)
    content1_1 = content1.decode()
    objects = find_tree_files(content1_1[5:25], gitdir)
    dir = gitdir.absolute().parent
    for obj in objects:
        os.remove(dir / obj[0])
        parent_path = pathlib.Path(obj[0]).parent
        while len(parent_path.parents) > 0:
            os.rmdir(parent_path)
            parent_path = pathlib.Path(parent_path).parent
    f_getref = open(gitdir / "HEAD", "w")
    f_getref.write(obj_name)
    f_getref.close()
    fmt, content2 = read_object(obj_name, gitdir)
    content2_2 = content2.decode()
    objects = find_tree_files(content2_2[5:25], gitdir)
    for obj in objects:
        parent_count = len(pathlib.Path(obj[0]).parents)
        parent_path = dir
        for par in range(parent_count - 2, -1, -1):
            parent_path /= pathlib.Path(obj[0]).parents[par]
            if not os.path.isdir(parent_path):
                os.mkdir(parent_path)
        fmt, obj_content = read_object(obj[1], gitdir)
        if fmt == "blob":
            pathlib.Path(dir / obj[0]).touch()
            blob = open(dir / obj[0], "w")
            blob.write(obj_content.decode())
            blob.close()
        else:
            os.mkdir(dir / obj[0])
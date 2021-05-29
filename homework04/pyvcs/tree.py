# coding: utf8
import os
import pathlib
import stat
import time
import datetime
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(
    gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = ""
) -> str:
    list_in_dir = [x.absolute() for x in (gitdir.parent / dirname).glob("*")]
    add_in_fut: tp.Dict[str, tp.List[GitIndexEntry]]
    add_in_fut = dict()
    toformat = []
    for entry in index:
        if pathlib.Path(entry.name).absolute() in list_in_dir:
            toformat.append(entry)
        else:
            subdir_name = entry.name.lstrip(dirname).split("/", 1)[0]
            if subdir_name not in add_in_fut:
                add_in_fut[subdir_name] = []
            add_in_fut[subdir_name].append(entry)
    for subdir_name in add_in_fut:
        st = (pathlib.Path(gitdir.parent) / dirname / subdir_name).stat()
        going_deeper = subdir_name if dirname == "" else dirname + "/" + subdir_name
        sha = write_tree(gitdir, add_in_fut[subdir_name], going_deeper)
        toformat.append(
            GitIndexEntry(
                ctime_s=int(st.st_ctime),
                ctime_n=st.st_ctime_ns % len(str(int(st.st_ctime))),
                mtime_s=int(st.st_mtime),
                mtime_n=st.st_mtime_ns % len(str(int(st.st_mtime))),
                dev=st.st_dev,
                ino=st.st_ino,
                mode=0o40000,
                uid=st.st_uid,
                gid=st.st_gid,
                size=st.st_size,
                sha1=bytes.fromhex(sha),
                flags=7,
                name=str(pathlib.Path(gitdir.parent) / dirname / subdir_name),
            )
        )
    data = b"".join(
        oct(entry.mode)[2:].encode()
        + b" "
        + pathlib.Path(entry.name).name.encode()
        + b"\00"
        + entry.sha1
        for entry in sorted(toformat, key=lambda x: x.name)
    )
    return hash_object(data, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    cur_time = int(time.mktime(time.localtime()))
    timezone = time.timezone
    if timezone > 0:
        formatted_timezone = "-"
    else:
        formatted_timezone = "+"
    formatted_timezone += f"{abs(timezone) // 3600:02}{abs(timezone) // 60 % 60:02}"
    commit_content = []
    commit_content.append(f"tree {tree}")
    if parent is not None:
        commit_content.append(f"parent {parent}")
    commit_content.append(f"author {author} {cur_time} {formatted_timezone}")
    commit_content.append(f"committer {author} {cur_time} {formatted_timezone}")
    commit_content.append(f"\n{message}\n")
    data = "\n".join(commit_content).encode()
    return hash_object(data, "commit", write=True)

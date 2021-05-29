# coding: utf8
import os
import pathlib
import typing as tp

def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    if 'GIT_DIR' not in os.environ:
        gitname = pathlib.Path('.git')
    else:
        gitname = pathlib.Path(os.environ['GIT_DIR'])
    while os.path.isdir(workdir):
        if os.path.isdir(workdir / pathlib.Path(gitname)):
            return workdir / gitname
        if workdir == '.':
            break
        workdir = pathlib.Path(os.path.dirname(workdir))
    raise AssertionError('Not a git repository')


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    if os.path.isfile(workdir):
        raise AssertionError(f'{workdir} is not a directory')
    if 'GIT_DIR' not in os.environ:
        gitdir = workdir / pathlib.Path('.git')
    else:
        gitdir = workdir / pathlib.Path(os.environ['GIT_DIR'])
    os.mkdir(gitdir)
    os.makedirs(gitdir / "refs" / "heads")
    os.mkdir(gitdir / "refs" / "tags")
    os.mkdir(gitdir / "objects")
    pathlib.Path(gitdir / "HEAD").touch()
    pathlib.Path(gitdir / "config").touch()
    pathlib.Path(gitdir / "description").touch()
    current_file = open(gitdir / "HEAD", "w")
    current_file.write("ref: refs/heads/master\n")
    current_file.close()
    current_file = open(gitdir / "config", "w")
    current_file.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
    current_file.close()
    current_file = open(gitdir / "description", "w")
    current_file.write("Unnamed pyvcs repository.\n")
    current_file.close()
    return gitdir
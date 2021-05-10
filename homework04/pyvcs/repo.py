import os
import pathlib
import typing as tp

def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    global det
    det = None
    try:
        gitdir = os.environ["GIT_DIR"]
        workdir_abs = pathlib.Path(workdir).absolute()
        if workdir == gitdir:
            return (workdir_abs)
        else:
            for dirpath, dirnames, filenames in os.walk(workdir):
                for name in dirnames:
                    name_cr = os.path.join(dirpath, name)
                    if name == gitdir:
                        det = pathlib.Path(name_cr)
        if det == None:
            parent = os.path.dirname(workdir)
            repo_find(parent)
        return det
    except:
        raise AssertionError("Not a git repository")

def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    if "GIT_DIR" not in os.environ:
        os.environ["GIT_DIR"] = ".git"
    gitdir = os.environ["GIT_DIR"]
    if pathlib.Path(workdir).is_dir():
        workdir = pathlib.Path(workdir)
        if not os.path.exists(workdir / gitdir):
            os.mkdir(workdir / gitdir)
        if not os.path.exists(workdir / gitdir / "refs"):
            os.mkdir(workdir / gitdir / "refs")
        if not os.path.exists(workdir / gitdir / "refs" / "heads"):
            os.mkdir(workdir / gitdir / "refs" / "heads")
        if not os.path.exists(workdir / gitdir / "refs" / "tags"):
            os.mkdir(workdir / gitdir / "refs" / "tags")
        if not os.path.exists(workdir / gitdir / "objects"):
            os.mkdir(workdir / gitdir / "objects")
        if not os.path.exists(workdir / gitdir / "HEAD"):
            pathlib.Path(workdir / gitdir / "HEAD").touch()
            with pathlib.Path(workdir / gitdir / "HEAD").open("w") as f:
                f.write("ref: refs/heads/master\n")
                f.close()
        if not os.path.exists(workdir / gitdir / "config"):
            pathlib.Path(workdir / gitdir / "config").touch()
            with pathlib.Path(workdir / gitdir / "config").open("w") as f:
                f.write(
                    "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
                f.close()
        if not os.path.exists(workdir / gitdir / "description"):
            pathlib.Path(workdir / gitdir / "description").touch()
            with pathlib.Path(workdir / gitdir / "description").open("w") as f:
                f.write("Unnamed pyvcs repository.\n")
                f.close()
        return pathlib.Path(gitdir)
    else:
        raise AssertionError(f"{workdir} is not a directory")
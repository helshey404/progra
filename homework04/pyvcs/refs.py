import pathlib
import typing as tp

def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    gitdir = pathlib.Path(gitdir)
    gitdir = gitdir / ref
    if not pathlib.Path(gitdir).exists():
        pathlib.Path(gitdir).touch()
    with (pathlib.Path(gitdir)).open("w") as f:
        f.write(new_value)
        f.close()

def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    gitdir = pathlib.Path(gitdir)
    with (pathlib.Path(gitdir / ".git" / name)).open("w") as f:
        f.write(f"ref: {ref}")
        f.close()

def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    gitdir = pathlib.Path(gitdir)
    if refname == "HEAD":
        with (pathlib.Path(gitdir / refname)).open("r") as f:
            f.seek(5)
            refname = f.read(17)
            f.close()
    with (pathlib.Path(gitdir / refname)).open("r") as f:
        data = f.read()
        f.close()
    return data

def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    if gitdir == "master":
        with (pathlib.Path(gitdir)).open("r") as f:
            data = f.read()
            f.close()
            return data
    else:
        path = sorted(pathlib.Path(".").glob('**/master'))
        if len(path) != 0:
            with (path[0]).open("r") as f:
                data = f.read()
                f.close()
                return data

def is_detached(gitdir: pathlib.Path) -> bool:
    if not pathlib.Path.exists(gitdir / "HEAD"):
        return False
    with (pathlib.Path(gitdir / "HEAD")).open("r") as f:
        data = f.read()
        f.close()
    if type(data) == str and len(data) == 40 and data[:5] != "ref: ":
        return True
    return False

def get_ref(gitdir: pathlib.Path) -> str:
    with pathlib.Path(gitdir, "HEAD").open("r") as f:
        getref = f.read()
        f.close()
    if getref[:5] == "ref: ":
        getref = getref[5:-1]
    return getref
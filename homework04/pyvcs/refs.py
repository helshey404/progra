import pathlib
import typing as tp
import os


def update_ref(
    gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str
) -> None:
    with open((pathlib.Path(str(gitdir) + os.path.sep + str(ref))), "w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    with open(str(gitdir) + os.path.sep + name, "w") as f:
        f.write(f"ref: {ref}")


def is_detached(gitdir: pathlib.Path) -> bool:
    with open(pathlib.Path(str(gitdir) + os.path.sep + "HEAD"), "r") as f:
        return len(f.read()) == 40


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD" and not is_detached(gitdir):
        return resolve_head(gitdir)
    if os.path.exists(pathlib.Path(str(gitdir) + os.path.sep + refname)):
        with open(pathlib.Path(str(gitdir) + os.path.sep + refname), "r") as f:
            return f.read().strip()



def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, get_ref(gitdir))


def get_ref(gitdir: pathlib.Path) -> str:
    with open(pathlib.Path(str(gitdir) + os.path.sep + "HEAD"), "r") as f:
        return f.read().split()[1].strip()

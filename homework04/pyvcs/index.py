import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        values = (self.ctime_s, self.ctime_n, self.mtime_s, self.mtime_n, self.dev, self.ino, self.mode, self.uid, self.gid, self.size, self.sha1, self.flags,
                  self.name.encode()
                  )

        return struct.pack("!10i20sh" + str(len(self.name)) + "s" + str(8 - (62 + len(self.name)) % 8) + "x", *values)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        index_unpacked_data = list(struct.unpack("!10i20sh" + str(len(data) - 62) + "s", data))
        return GitIndexEntry(*(tuple(index_unpacked_data[:-1] + [index_unpacked_data[-1].rstrip(b"\00").decode()])))


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    index = []
    if not pathlib.Path(gitdir / "index").exists():
        return index
    with (gitdir / "index").open("rb") as file:
        data = file.read()
    header = file.read(12)

    result = []

    count_files = struct.unpack(">i", header[8:])[0]
    for i in range(count_files):
        end = len(data)
        for j in range(63, end, 8):
            if data[j] == 0:
                end = j
                break
        result.append(GitIndexEntry.unpack(data[:end]))
        if len(data) > end:
            data = data[end + 1:]
    return result

def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    sign = b"DIRC"
    ver = 2
    count_entries = len(entries)
    head = struct.pack("!4s2i", sign, ver, count_entries)
    packed = ""
    packed = packed.encode()

    for i in entries:
        packed += i.pack()
    data = head + packed
    extension_data = hashlib.sha1(data).digest()
    data = data + extension_data
    with (pathlib.Path(gitdir / "index")).open("wb") as f:
        f.write(data)
        f.close()

def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    data = read_index(gitdir)
    if details:
        for file in data:
            print(oct(file.mode)[2:], file.sha1.hex(), "0\t" + file.name)
    else:
        for file in data:
            print(file.name)

def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    new_entr = []
    if (not pathlib.Path(gitdir / "index").exists()):
        pathlib.Path(gitdir / "index").touch()
    for path in paths:
        contain = os.stat(path)
        with (pathlib.Path(path)).open("rb") as f:
            data = f.read()
            f.close()
        sha = hash_object(data, "blob", True)
        up_entr = GitIndexEntry(
            int(contain.st_ctime),
            0,
            int(contain.st_mtime),
            0,
            contain.st_dev,
            contain.st_ino,
            contain.st_mode,
            contain.st_uid,
            contain.st_gid,
            contain.st_size,
            bytes.fromhex(sha),
            7,
            str(path).replace("\\", "/")
        )
        if write:
            new_entr.append(up_entr)
            new_entr.sort(key=lambda files: files[-1])
            write_index(gitdir, new_entr)
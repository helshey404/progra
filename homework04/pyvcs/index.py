# coding: utf-8
import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
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
		s = str.encode(self.name, "utf-8")
		return struct.pack(
			f">10i20sh{len(s) + 3}s",
			self.ctime_s,
			self.ctime_n,
			self.mtime_s,
			self.mtime_n,
			self.dev,
			self.ino,
			self.mode,
			self.uid,
			self.gid,
			self.size,
			self.sha1,
			self.flags,
			s,
		)

	@staticmethod
	def unpack(data: bytes) -> "GitIndexEntry":
		(ctime_s,
		ctime_n,
		mtime_s,
		mtime_n,
		dev,
		ino,
		mode,
		uid,
		gid,
		size,
		sha1,
		flags) = struct.unpack(">10i20sh", data[:62])
		data = data[62:]
		last_byte = data.find(b"\x00\x00\x00")
		name = data[:last_byte].decode()
		return GitIndexEntry(ctime_s, ctime_n, mtime_s, mtime_n, dev, ino, mode, uid, gid, size, sha1, flags, name)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
	index_f = pathlib.Path(gitdir / "index")
	result: tp.List[GitIndexEntry] = []
	if not os.path.isfile(index_f):
		return result
	content = open(index_f, "rb")
	data = content.read()
	dirc, version, cnt = struct.unpack(">4s2i", data[:12])
	data = data[12:]
	for i in range(cnt):
		result.append(GitIndexEntry.unpack(data))
		data = data[62:]
		next_byte = data.find(b"\x00\x00\x00")
		data = data[next_byte + 3 :]
	content.close()
	return result


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
	signature = b"DIRC"
	version = 2
	header = struct.pack("!4sLL", signature, version, len(entries))
	packed_entries = b""
	for entry in entries:
		packed_entries += entry.pack()
	content = header + packed_entries
	digest = hashlib.sha1(content).digest()

	with open(str(gitdir) + os.path.sep + "index", "wb") as f:
		f.write(content + digest)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
	entries = read_index(gitdir)
	if not details:
		for entry in entries:
			print(entry.name)
	else:
		for entry in entries:
			mode = entry.mode
			newMode = ""
			while mode > 0:
				newMode = str(mode % 8) + newMode
				mode //= 8
			if newMode[3:].split() != "755":
				newMode = newMode[0:3] + "644"
			print(f"{newMode} {bytes.hex(entry.sha1)} 0\t{entry.name}")


def update_index(
	gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True
) -> None:
	dict_entries = [entry for entry in read_index(gitdir)]
	for file in paths:
		if str(file) in dict_entries:
			del dict_entries[dict_entries.index(file)]
		with open(file, "r") as f:
			content = f.read()
		sha1 = bytes.fromhex(hash_object(content.encode(), fmt="blob", write=True))
		name = str(file)
		flags = len(name)
		if file not in dict_entries:
			dict_entries.append(
				GitIndexEntry(
					os.stat(file)[9],
					0,
					os.stat(file)[8],
					0,
					os.stat(file)[2],
					os.stat(file)[1],
					os.stat(file)[0],
					os.stat(file)[4],
					os.stat(file)[5],
					os.stat(file)[6],
					sha1,
					flags,
					name,
				)
			)
		else:
			dict_entries[dict_entries.index(file)] = GitIndexEntry(
				os.stat(file)[9],
				0,
				os.stat(file)[8],
				0,
				os.stat(file)[2],
				os.stat(file)[1],
				os.stat(file)[0],
				os.stat(file)[4],
				os.stat(file)[5],
				os.stat(file)[6],
				sha1,
				flags,
				name,
			)
	if write:
		name_list = []
		dict_entries = sorted(dict_entries, key=operator.attrgetter("name"))
		for x in dict_entries:
			name_list.append(x)
		write_index(gitdir, name_list)



gitdir = os.getcwd() + os.path.sep + ".git"
entries = [
	GitIndexEntry(
		ctime_s=1593379228,
		ctime_n=200331013,
		mtime_s=1593379228,
		mtime_n=200331013,
		dev=16777220,
		ino=8610507,
		mode=33188,
		uid=501,
		gid=20,
		size=4,
		sha1=b"W\x16\xcaY\x87\xcb\xf9}k\xb5I \xbe\xa6\xad\xde$-\x87\xe6",
		flags=7,
		name="bar.txt",
	),
	GitIndexEntry(
		ctime_s=1593379274,
		ctime_n=535850078,
		mtime_s=1593379274,
		mtime_n=535850078,
		dev=16777220,
		ino=8610550,
		mode=33188,
		uid=501,
		gid=20,
		size=7,
		sha1=b"\x9f5\x8aJ\xdd\xef\xca\xb2\x94\xb8>B\x82\xbf\xef\x1f\x96%\xa2I",
		flags=15,
		name="baz/numbers.txt",
	),
	GitIndexEntry(
		ctime_s=1593379233,
		ctime_n=953396667,
		mtime_s=1593379233,
		mtime_n=953396667,
		dev=16777220,
		ino=8610515,
		mode=33188,
		uid=501,
		gid=20,
		size=4,
		sha1=b"%|\xc5d,\xb1\xa0T\xf0\x8c\xc8?-\x94>V\xfd>\xbe\x99",
		flags=7,
		name="foo.txt",
	),
]
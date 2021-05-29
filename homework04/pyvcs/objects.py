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
	header = f"{fmt} {len(data)}\0".encode()
	store = header + data
	if write:
		dir_name = hashlib.sha1(store).hexdigest()[:2]
		file_name = hashlib.sha1(store).hexdigest()[2:]
		if not os.path.exists(f".git/objects/{dir_name}"):
			os.mkdir(f".git/objects/{dir_name}")
		if os.path.exists(f".git/objects/{dir_name}/{file_name}"):
			os.remove(f".git/objects/{dir_name}/{file_name}")
		file_name = hashlib.sha1(store).hexdigest()[2:]
		content = zlib.compress(store)
		f = open(f".git/objects/{dir_name}/{file_name}", "wb")
		f.write(content)
		f.close()
	return hashlib.sha1(store).hexdigest()


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
	dir_name = obj_name[:2]
	file_name = obj_name[2:]
	if len(obj_name) > 40 or len(obj_name) < 4:
		raise Exception(f"Not a valid object name {obj_name}")
	PATH = pathlib.Path(
		str(gitdir) + str(os.path.sep) + "objects" + str(os.path.sep) + dir_name
	)
	ld = []
	ls = os.listdir(PATH)
	for filename in ls:
		if file_name == filename[: len(file_name)]:
			ld.append(dir_name + filename)
	if not ld:
		raise Exception(f"Not a valid object name {obj_name}")
	return ld



def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
	dir_name = obj_name[:2]
	file_name = resolve_object(obj_name, gitdir)[0][2:]
	return str(
		pathlib.Path(
			str(gitdir)
			+ os.path.sep
			+ "objects"
			+ os.path.sep
			+ dir_name
			+ os.path.sep
			+ file_name
		)
	)


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
	if len(sha) > 40 or len(sha) < 4 or not os.path.exists(find_object(sha, gitdir)):
		raise Exception(f"Not a valid object name {sha}")
	dir_name = sha[:2]
	file_name = sha[2:]
	with open(pathlib.Path(find_object(sha, gitdir)), "rb") as f:
		answ = f.read()
		answ = zlib.decompress(answ)

	return (
		answ.split(b"\00")[0].split(b" ")[0].decode(),
		answ.split(b"\00", maxsplit=1)[1],
	)


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
	tree = []
	while data:
		flag = data.index(b"\00")
		mode, name = map(lambda x: x.decode(), data[:flag].split(b" "))
		sha = data[flag + 1 : flag + 21]
		tree.append((int(mode), name, sha.hex()))
		data = data[flag + 21 :]
	return tree


def cat_file(obj_name: str, pretty: bool = True) -> None:
	gitdir = repo_find()
	fmt, content = read_object(obj_name, gitdir)
	if fmt == "blob" or fmt == "commit":
		print(content.decode())
	else:
		for tree in read_tree(content):
			if tree[0] == 40000:  										
				print(f"{tree[0]:06}", "tree", tree[2] + "\t" + tree[1])
			else:
				print(f"{tree[0]:06}", "blob", tree[2] + "\t" + tree[1])



def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
	fmt, content = read_object(tree_sha, gitdir)
	objects = read_tree(content)
	result = []
	for obj in objects:
		if obj[0] == 100644 or obj[0] == 100755:
			result.append((obj[1], obj[2]))
		else:
			sub_objects = find_tree_files(obj[2], gitdir)
			for sub_obj in sub_objects:
				result.append((obj[1] + "/" + sub_obj[0], sub_obj[1]))
	return result


def commit_parse(raw: bytes, start: int = 0, dct=None):
	result = {"message": []}
	for elem in raw.decode().split("\n"):
		if elem.startswith(("tree", "parent", "author", "committer")):
			name, value = elem.split(" ", maxsplit=1)
			result[name] = value
		else:
			result["message"].append(elem)
	return result

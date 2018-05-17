####################################################
#
#   dist.py - Create PyGUI distribution tar file
#
####################################################

source_indent = 4
text_indent = 2

text_suffixes = {
	".py": source_indent,
	".pyx": source_indent,
	".txt": text_indent
}

ignore_suffixes = [
	"~", ".pyc", ".o", ".so", ".core", "]",
	".DS_Store"
]

ignore_names = [
	"build", "dist", "core", "Icon\r", ".DS_Store"
]

tar_name_prefix = "PyGUI"

dist_items = [
	"Demos", "Doc", "GUI", "Tests",
	"CHANGES.txt", "README.txt", "TODO.txt",
	"setup.cfg", "setup.py", "distutils_extensions.py"
]

#testing_items = [
#]

#----------------------------------------------------

import os, re, sys, tarfile
from cStringIO import StringIO
from glob import glob

tabs = re.compile(r"^\t+", re.MULTILINE)

def endswith_any(path, suffixes):
	for suffix in suffixes:
		if path.endswith(suffix):
			return 1
	return 0

def expand_indentation(indent):
	def f(match):
		n = len(match.group(0))
		return (n * indent) * " "
	return f
	
def join_path(*args):
	return os.path.normpath(os.path.join(*args))

def add_text_file(tar, arcname, path, indent):
	f = open(path, "r")
	info = tar.gettarinfo(path, arcname, f)
	data = f.read()
	f.close()
	data = tabs.sub(expand_indentation(indent), data)
	info.size = len(data)
	h = StringIO(data)
	tar.addfile(info,  h)

#def add_text_file(zip, arcname, path, indent):
#	f = open(path, "r")
#	data = f.read()
#	f.close()
#	data = tabs.sub(expand_indentation(indent), data)
#	zip.writestr(arcname,  data)

def add_file(tar, arcname, path):
	tar.add(path, arcname)

#def add_file(zip, arcname, path):
#	zip.write(path, arcname)

def add_directory(tar, arc_dir, root_dir, dir, exclude = []):
	dir_path = join_path(root_dir, dir)
	for name in os.listdir(dir_path):
		if name not in ignore_names \
			and not endswith_any(name, ignore_suffixes):
				item = join_path(dir, name)
				add_item(tar, arc_dir, root_dir, item, exclude)

def add_item(tar, arc_dir, root_dir, item, exclude = []):
	if item not in exclude:
		arc_path = join_path(arc_dir, item)
		item_path = join_path(root_dir, item)
		arrow = "<-"
		if os.path.isdir(item_path):
			add_directory(tar, arc_dir, root_dir, item, exclude)
		else:
			suffix = os.path.splitext(item_path)[1]
			if suffix in text_suffixes:
				add_text_file(tar, arc_path, item_path, indent = text_suffixes[suffix])
				arrow = "<="
			else:
				add_file(tar, arc_path, item_path)
		print arc_path, arrow, repr(item_path)

def add_items(tar, arc_dir, root_dir, items, exclude = []):
	for item in items:
		add_item(tar, arc_dir, root_dir, item, exclude)

def open_archive(tar_dir, prefix, version):
	tarpath = os.path.join(tar_dir, "%s-%s.tar.gz" % (prefix, version))
	print "=====", tarpath, "====="
	tar = tarfile.open(tarpath, "w:gz")
	return tar

#def open_archive(tar_dir, prefix, version):
#	zippath = os.path.join(tar_dir, "%s-%s.zip" % (prefix, version))
#	print "=====", zippath, "====="
#	zip = zipfile.ZipFile(zippath, "w", zipfile.ZIP_DEFLATED)
#	return zip

def create_source_archive(tar_dir, arc_dir, root_dir, version):
	tar = open_archive(tar_dir, tar_name_prefix, version)
	#add_directory(tar, arc_dir, root_dir, os.curdir, exclude = testing_items)
	add_items(tar, arc_dir, root_dir, dist_items)
	tar.close()

#def create_source_archive(zip_dir, arc_dir, root_dir, version):
#	zip = open_zipfile(zip_dir, tar_name_prefix, version)
#	#add_directory(tar, arc_dir, root_dir, os.curdir, exclude = testing_items)
#	add_items(zip, arc_dir, root_dir, dist_items)
#	zip.close()

#def create_test_tarball(tar_dir, arc_dir, root_dir, version):
#	tar = open_tarfile("%s-Tests" % tar_name_prefix, version)
#	add_items(tar, arc_dir, root_dir, testing_items)
#	tar.close()
	
def main(tar_dir, root_dir, version):
	arc_dir = "PyGUI-%s" % version
	create_source_archive(tar_dir, arc_dir, root_dir, version)
	#create_test_tarball(tar_dir, arc_dir, root_dir, version)

if __name__ == "__main__":
	main(*sys.argv[1:])

#---------------------------------------------------
#
#   PyGUI test launcher for Windows
#
#---------------------------------------------------

import os, sys
from glob import glob
from testing import say, ask

def get_test_names():
	global test_names
	test_names = glob("*-*.py")

def list_tests():
	all = test_names + [""]
	n = len(all) // 2
	for row in zip(all[:n], all[n:]):
		for name in row:
			sys.stdout.write("%-38s" % name)
		sys.stdout.write("\n")

def get_test():
	while 1:
		prefix = ask("Test? ")
		if not prefix:
			sys.exit(0)
		matches = glob("%s-*.py" % prefix)
		if not matches:
			say("Unknown test")
			continue
		if len(matches) > 1:
			say("Ambiguous")
			continue
		return matches[0]

def main():
	get_test_names()
	while 1:
		list_tests()
		name = get_test()
		print
		#cmd = r"c:\python25\python %s" % name
		cmd = "%s %s" % (sys.executable, name)
		say("Executing:", repr(cmd))
		os.system(cmd)

main()

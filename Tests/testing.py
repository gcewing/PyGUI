import sys

try:
	ask = raw_input
except NameError:
	ask = input

def say(*args):
	sys.stdout.write(" ".join(map(str, args)) + "\n")

#!/usr/bin/python3 -B

import re

"""
	TODO ranges: int[0-30]

	Examples for formats:
		"({-1,0,1},int)":
			(1,1)
			(-1,4)
			(0,18)
		"{int,(int,int)}":
			1
			(1, 2)
			(19, 20)
			100
		"[(1, bool, float)]":
			[(1, true, 2.3f)  |  (1, false, 0.0f)]
			[(1, false, 1.5f)]
			[(1, false, 1.5f)  |  (1, true, 3.f)  |  (1, false, 2.2f)]
		"([(false, bool, {-1,0,[str]})], int)":
			([false, false, -1  |  false, true, 0  |  false, true, ["wow"  |  "really"]],2)
			([],54)
			([false, false, -1  |  []],2)
"""

def die(string):
	print(string)
	1/0 # FOR THE STACK TRACE!

def matches(data, format):
	format = format.replace(" ", "").replace("\n", "").replace("\t", "")
	if not validateFormat(format):
		die("invalid format")
		return False
	if format == "":
		die("format can't be void")
		return False
	if format.startswith("("):
		if not isinstance(data, tuple):
			return False
		splat = splitFormat(format)
		if not (len(data) == len(splat)):
			return False
		for i in range(len(data)):
			if not matches(data[i], splat[i]):
				return False
	elif format.startswith("{"):
		innerFormats = splitFormat(format)
		for innerFormat in innerFormats:
			if matches(data, innerFormat):
				return True
		return False
	elif format.startswith("["):
		if not isinstance(data, list):
			return False
		innerFormat = format[1:-1]
		for elem in data:
			if not matches(elem, innerFormat):
				return False
	elif format == "float":
		if (not isinstance(data, float)) and (not isinstance(data, int)):
			print("no float", data)
			return False
	elif format == "int":
		if not isinstance(data, int):
			print("no int", data)
			return False
	elif format == "str":
		if not isinstance(data, str):
			print("no str", data)
			return False
	elif format == "bool":
		if not isinstance(data, bool):
			print("no bool", data)
			return False
	else:
		die("wot format section: " + format)
	return True

def splitFormat(format): # "(1,2,3)" -> [1, 2, 3]; "{'a','b','c'}" -> ['a', 'b', 'c']
	format = format[1:-1]
	i = 0
	sections = list()
	braces = 0
	while format != "" and i < len(format):
		if format[i] == '{' or format[i] == '(' or format[i] == '[':
			braces += 1
		elif format[i] == '}' or format[i] == ')' or format[i] == ']':
			braces -= 1
		elif (braces == 0) and (format[i] == ','):
			sections.append(format[:i])
			format = format[i+1:]
			i = -1 # because of i += 1
		i += 1
	sections.append(format)
	return sections

def validateFormat(format):
	PAREN = 0
	BRACE = 1
	LIST = 2

	bracelist = list()
	return True

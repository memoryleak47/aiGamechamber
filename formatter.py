#!/usr/bin/python3 -B

import re

def countSections(format):
	format = re.sub("\[.*\]", "", re.sub("\{.*\}", "", format))
	return format.count(",")+1

def splitSections(format):
	i = 0
	sections = list()
	braces = 0
	while format != "" and i < len(format):
		if format[i] == '{' or format[i] == '[':
			braces += 1
		elif format[i] == '}' or format[i] == ']':
			braces -= 1
		elif (braces == 0) and (format[i] == ','):
			sections.append(format[:i])
			format = format[i+1:]
			i = -1 # because of i += 1
		i += 1
	sections.append(format)
	return sections

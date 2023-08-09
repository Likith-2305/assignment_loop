#!/usr/bin/python
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')


def database(section='postgresql'):
	

	# get section, default to postgresql
	db = {}
	if parser.has_section(section):
		params = parser.items(section)
		for param in params:
			db[param[0]] = param[1]
	else:
		raise Exception('Section {0} not found in the secrets file'.format(section,))

	return db

def openAiSecrets(section='openAI'):
	if parser.has_section(section):
		params = parser.items(section)
		for param in params:
			return param[1]
	else:
		raise Exception('Section {0} not found in the secrets file'.format(section,))

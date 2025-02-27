# coding=utf8
"""Constants

Holds various strings and regexes for valid types
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-18"

# Python imports
import re as _re

# Pip imports
from jobject import jobject

# Private values
_special_syntax = r'[a-z0-9_-]+'

# Export the values
array = ['unique', 'duplicates']
nodes = [
	'any', 'base64', 'bool', 'date', 'datetime', 'decimal', 'float', 'int',
	'ip', 'json', 'md5', 'price', 'string', 'time', 'timestamp', 'uint',
	'uuid', 'uuid4'
]
special = jobject({
	'syntax': _special_syntax,
	'key': _re.compile('^__(%s)__$' % _special_syntax),
	'name': _re.compile('^%s$' % _special_syntax),
	'reserved': [
		'__array__', '__hash__', '__maximum__', '__minimum__', '__name__',
		'__options__', '__regex__', '__require__', '__type__'
	]
})
standard = _re.compile('^_?[a-zA-Z0-9][a-zA-Z0-9_-]*$')
regex = jobject({
	'base64':	_re.compile('^(?:[A-Za-z0-9+/]{4})+(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$'),
	'date':		_re.compile('^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$'),
	'datetime':	_re.compile('^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]) (?:[01]\d|2[0-3])(?::[0-5]\d){2}$'),
	'decimal':	_re.compile('^-?(?:[1-9]\d+|\d)(?:\.(\d+))?$'),
	'int':		_re.compile('^(?:0?|[+-]?[1-9]\d*|0x[0-9a-f]+|0?o[0-7]+)$'),
	'ip':		_re.compile('^(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}$'),
	'md5':		_re.compile('^[a-fA-F0-9]{32}$'),
	'price':	_re.compile('^-?(?:[1-9]\d+|\d)(?:\.\d{1,2})?$'),
	'time':		_re.compile('^(?:[01]\d|2[0-3])(?::[0-5]\d){2}$'),
	'uuid':		_re.compile('^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'),
	'uuid4':	_re.compile('^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}$')
})
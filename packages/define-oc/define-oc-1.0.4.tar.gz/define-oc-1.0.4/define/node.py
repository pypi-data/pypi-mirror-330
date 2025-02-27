# coding=utf8
"""Node

Represents a single node of data, an immutable type like an int or a string
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-19"

# Limit exports
__all__ = ['Node']

# Ouroboros imports
import jsonb
from tools import combine
import undefined

# Python imports
from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation as DecimalInvalid
import hashlib
import re
from typing import Literal as TL, Pattern

# Local imports
from define import constants
from define.base import Base

# There is no way to access the real type of compiled regular expressions or md5
#	hashes so unfortunately we have to do this ugly hack
_REGEX_TYPE	= type(constants.regex['date'])
_MD5_TYPE = type(hashlib.md5(b'hack'))

class Node(Base):
	"""Node

	Represents a single node of data, an immutable type like an int or a string

	Extends:
		Base
	"""

	_VALID_TYPES = ['any', 'base64', 'bool', 'date', 'datetime', 'decimal',
					'float', 'int', 'ip', 'json', 'md5', 'price', 'string',
					'time', 'timestamp', 'uint', 'uuid', 'uuid4']
	"""Valid Types

	Holds a list of valid values used to represent Node types"""

	def __init__(self,
		details: dict | str,
		extend: dict | TL[False] = False,
		name: str = None
	):
		"""Constructor

		Initialises the instance

		Arguments:
			details (dict | str): Definition, or type string
			extend (dict | False): Optional, a dictionary to extend the \
				definition
			name (str): The name of the field if it is one

		Raises:
			KeyError, ValueError

		Returns:
			Node
		"""

		# Init the details
		dDetails: dict = None

		# If we got a string
		if isinstance(details, str):

			# If we got no extend or it's False
			if extend is undefined or extend is False:

				# Store the type as the passed string
				dDetails = { '__type__': details }

			# Else, we have an extend value
			else:

				# If it's a dictionary
				if isinstance(extend, dict):

					# Store the details by making a new dict from the details
					#	and the extend
					dDetails = combine(
						{ '__type__': details },
						extend
					)

				# Else, we got some invalid value
				raise ValueError('extend must be a dict or False')

		# Else, if we got a dict
		elif isinstance(details, dict):

			# Generate the details
			dDetails = Base.make_details(details, extend)

		# Else, we got invalid details
		else:
			raise ValueError('"details" must be a dict or a str')

		# If the type is not found
		if '__type__' not in dDetails:
			raise KeyError('__type__ missing')

		# If the type is invalid
		if dDetails['__type__'] not in self._VALID_TYPES:
			raise KeyError('__type__ (%s) invalid' % dDetails['__type__'])

		# Call the parent constructor
		super(Node, self).__init__(dDetails, name)

		# Store the type
		self._type = dDetails['__type__']

		# Init the value types
		self._regex = None
		self._options = None
		self._minimum = None
		self._maximum = None

		# If we have options
		if '__options__' in details:
			self.options(details['__options__'])

		# Else, no options
		else:

			# If there's a regex string available
			if '__regex__' in details:
				self.regex(details['__regex__'])

			# If there's a min or max
			bMin = ('__minimum__' in details and True or False)
			bMax = ('__maximum__' in details and True or False)

			if bMin or bMax:
				self.minmax(
					(bMin and details['__minimum__'] or None),
					(bMax and details['__maximum__'] or None)
				)

	@staticmethod
	def compare_ips(first: str, second: str) -> int:
		"""Compare IPs

		Compares two IPs and returns a status based on which is greater
		If first is less than second: -1
		If first is equal to second: 0
		If first is greater than second: 1

		Arguments:
			first (str): A string representing an IP address
			second (str): A string representing an IP address

		Returns:
			int
		"""

		# If the two IPs are the same, return 0
		if first == second:
			return 0

		# Create lists from the split of each IP, store them as ints
		lFirst = [int(i) for i in first.split('.')]
		lSecond = [int(i) for i in second.split('.')]

		# Go through each part from left to right until we find the
		# 	difference
		for i in [0, 1, 2, 3]:

			# If the part of x is greater than the part of y
			if lFirst[i] > lSecond[i]:
				return 1

			# Else if the part of x is less than the part of y
			elif lFirst[i] < lSecond[i]:
				return -1

	def clean(self, value: any, level: list[str] = undefined):
		"""Clean

		Cleans and returns the new value

		Arguments:
			value {mixed} -- The value to clean

		Returns:
			mixed
		"""

		# If the level is not set
		if level is undefined:
			level = []

		# If the value is None and it's optional, return as is
		if value is None and self._optional:
			return None

		# If it's an ANY, there is no reasonable expectation that we know what
		#	the value should be, so we return it as is
		if self._type == 'any':
			pass

		# Else if it's a basic string type
		elif self._type in ['base64', 'ip', 'string', 'uuid', 'uuid4']:

			# And not already a string
			if not isinstance(value, str):
				value = str(value)

		# Else if it's a BOOL just check if the value flags as positive
		elif self._type == 'bool':

			# If it's specifically a string, it needs to match a specific
			#	pattern to be true
			if isinstance(value, str):
				value = (value in (
					'true', 'True', 'TRUE', 't', 'T', 'yes', 'Yes', 'YES', 'y',
					'Y', 'x', '1'
				) and True or False)

			# Else
			else:
				value = (value and True or False)

		# Else if it's a date type
		elif self._type == 'date':

			# If it's a python type, use strftime on it
			if isinstance(value, (date, datetime)):
				value = value.strftime('%Y-%m-%d')

			# Else if it's already a string
			elif isinstance(value, str):
				pass

			# Else convert it to a string
			else:
				value = str(value)

		# Else if it's a datetime type
		elif self._type == 'datetime':

			# If it's a python type, use strftime on it
			if isinstance(value, datetime):
				value = value.strftime('%Y-%m-%d %H:%M:%S')
			elif isinstance(value, date):
				value = '%s 00:00:00' % value.strftime('%Y-%m-%d')

			# Else if it's already a string
			elif isinstance(value, str):
				pass

			# Else convert it to a string
			else:
				value = str(value)

		# Else if it's a decimal
		elif self._type == 'decimal':

			# If it's not a decimal
			if not isinstance(value, Decimal):
				value = Decimal(value)

			# Convert it to a string
			value = '{0:f}'.format(value)

		# Else if it's a float
		elif self._type == 'float':
			value = float(value)

		# Else if it's an int type
		elif self._type in ['int', 'timestamp', 'uint']:

			# If the value is a string, convert it
			if isinstance(value, str):
				value = int(value, 0)

			# Else if it's not an int already
			elif not isinstance(value, int):
				value = int(value)

		# Else if it's a JSON type
		elif self._type == 'json':

			# If it's already a string
			if isinstance(value, str):
				pass

			# Else, encode it
			else:
				value = jsonb.encode(value)

		# Else if it's an md5 type
		elif self._type == 'md5':

			# If it's a python type, get the hexadecimal digest
			if isinstance(value, _MD5_TYPE):
				value = value.hexdigest()

			# Else if it's a string
			elif isinstance(value, str):
				pass

			# Else, try to convert it to a string
			else:
				value = str(value)

		# Else if it's a price type
		elif self._type == 'price':

			# If it's not already a Decimal
			if not isinstance(value, Decimal):
				value = Decimal(value)

			# Make sure its got 2 decimal places
			value = "{0:f}".format(value.quantize(Decimal('1.00')))

		# Else if it's a time type
		elif self._type == 'time':

			# If it's a python type, use strftime on it
			if isinstance(value, (time, datetime)):
				value = value.strftime('%H:%M:%S')

			# Else if it's already a string
			elif isinstance(value, str):
				pass

			# Else convert it to a string
			else:
				value = str(value)

		# Else we probably forgot to add a new type
		else:
			raise Exception('%s has not been added to .clean()' % self._type)

		# Return the cleaned value
		return value

	def minmax(self, minimum: any = undefined, maximum: any = undefined):
		"""Min/Max

		Sets or gets the minimum and/or maximum values for the Node. For \
		getting, returns {"minimum":mixed,"maximum":mixed}

		Arguments:
			minimum (any): The minimum value
			maximum (any): The maximum value

		Raises:
			TypeError, ValueError

		Returns:
			None | dict
		"""

		# If neither min or max is set, this is a getter
		if minimum is undefined and maximum is undefined:
			return {
				'minimum': self._minimum,
				'maximum': self._maximum
			}

		# If the minimum is set
		if minimum != None:

			# If it's undefined
			if minimum is undefined:
				raise ValueError(
					'"minimum" can only be undefined if "maximum" is also ' \
					'undefined'
				)

			# If the current type is a date, datetime, ip, or time
			if self._type in ['date', 'datetime', 'ip', 'time']:

				# Make sure the value is valid for the type
				if not isinstance(minimum, str) \
					or not constants.regex[self._type].match(minimum):
					raise ValueError(
						'"__minimum__" is not valid for the current type: ' \
						'"%s"' % self._type
					)

			# Else if the type is an int (unsigned, timestamp), or a string in
			# 	which the min/max are lengths
			elif self._type in ['base64', 'int', 'string', 'timestamp', 'uint']:

				# If the value is not a valid int or long
				if not isinstance(minimum, int):

					# If it's a valid representation of an integer, convert it
					if isinstance(minimum, str) \
						and constants.regex['int'].match(minimum):
						minimum = int(minimum, 0)

					# Else, raise an error
					else:
						raise ValueError('"__minimum__" must be an integer')

					# If the type is meant to be unsigned
					if self._type in ['base64', 'string', 'timestamp', 'uint']:

						# And it's below zero
						if minimum < 0:
							raise ValueError(
								'"__minimum__" must be an unsigned integer'
							)

			# Else if the type is decimal
			elif self._type == 'decimal':

				# Store it if it's valid, else throw a ValueError
				try:
					minimum = Decimal(minimum)
				except ValueError:
					raise ValueError('"__minimum__" not a valid decimal')

			# Else if the type is float
			elif self._type == 'float':

				# Store it if it's valid, else throw a ValueError
				try:
					minimum = float(minimum)
				except ValueError:
					raise ValueError('"__minimum__" not a valid float')

			# Else if the type is price
			elif self._type == 'price':

				# If it's not a valid representation of a price
				if not isinstance(minimum, str) or \
					not constants.regex['price'].match(minimum):
					raise ValueError('"__minimum__" not a valid price')

				# Store it as a Decimal
				minimum = Decimal(minimum)

			# Else we can't have a minimum
			else:
				raise TypeError(
					'can not set __minimum__ for "%s" type' % self._type
				)

			# Store the minimum
			self._minimum = minimum

		# If the maximum is set
		if maximum != None:

			# If it's undefined
			if maximum is undefined:
				raise ValueError(
					'"maximum" can only be undefined if "minimum" is also ' \
					'undefined'
				)

			# If the current type is a date, datetime, ip, or time
			if self._type in ['date', 'datetime', 'ip', 'time']:

				# Make sure the value is valid for the type
				if not isinstance(maximum, str) \
					or not constants.regex[self._type].match(maximum):
					raise ValueError(
						'"__maximum__" is not valid for the current type: ' \
						'"%s"' % self._type
					)

			# Else if the type is an int (unsigned, timestamp), or a string in
			# 	which the min/max are lengths
			elif self._type in ['base64', 'int', 'string', 'timestamp', 'uint']:

				# If the value is not a valid int or long
				if not isinstance(maximum, int):

					# If it's a valid representation of an integer
					if isinstance(maximum, str) \
						and constants.regex['int'].match(maximum):

						# Convert it
						maximum = int(maximum, 0)

					# Else, raise an error
					else:
						raise ValueError('"__maximum__" must be an integer')

					# If the type is meant to be unsigned
					if self._type in ['base64', 'string', 'timestamp', 'uint']:

						# And it's below zero
						if maximum < 0:
							raise ValueError(
								'"__maximum__" must be an unsigned integer'
							)

			# Else if the type is decimal
			elif self._type == 'decimal':

				# Store it if it's valid, else throw a ValueError
				try:
					maximum = Decimal(maximum)
				except ValueError:
					raise ValueError('"__maximum__" not a valid decimal')

			# Else if the type is float
			elif self._type == 'float':

				# Store it if it's valid, else throw a ValueError
				try:
					minimum = float(minimum)
				except ValueError:
					raise ValueError('"__maximum__" not a valid float')

			# Else if the type is price
			elif self._type == 'price':

				# If it's not a valid representation of a price
				if not isinstance(maximum, str) or \
					not constants.regex.price.match(maximum):
					raise ValueError('"__maximum__" not a valid price')

				# Store it as a Decimal
				maximum = Decimal(maximum)

			# Else we can't have a maximum
			else:
				raise TypeError(
					'can not set __maximum__ for "%s" type' % self._type
				)

			# If we also have a minimum
			if self._minimum is not None:

				# If the type is an IP
				if self._type == 'ip':

					# If the min is above the max, we have a problem
					if self.compare_ips(self._minimum, maximum) == 1:
						raise ValueError(
							'"__maximum__" can not be below "__minimum__"'
						)

				# Else any other data type
				else:

					# If the min is above the max, we have a problem
					if self._minimum > maximum:
						raise ValueError(
							'"__maximum__" can not be below "__minimum__"'
						)

			# Store the maximum
			self._maximum = maximum

	def options(self, options: list[any] = undefined):
		"""Options

		Setter/Getter for the list of acceptable values for the Node

		Arguments:
			options (list): A list of valid values

		Raises:
			TypeError, ValueError

		Returns:
			None | list
		"""

		# If opts aren't set, this is a getter
		if options is undefined:
			return self._options

		# If the options are not a list
		if not isinstance(options, list):
			raise ValueError('"__options__" must be a list')

		# If the type is not one that can have options
		if self._type not in ['base64', 'date', 'datetime', 'decimal', 'float',
								'int', 'ip', 'md5', 'price', 'string', 'time',
								'timestamp', 'uint', 'uuid', 'uuid4']:
			raise TypeError(
				'can not set __options__ for "%s" type' % self._type
			)

		# Init the list of options to be saved
		lOpts: list = []

		# Go through each item and make sure it's unique and valid
		for i in range(len(options)):

			# Convert the value based on the type
			# If the type is a string one that we can validate
			if self._type in ['base64', 'date', 'datetime', 'ip', 'md5', 'time',
								'uuid', 'uuid4']:

				# If the value is not a string or doesn't match its regex, raise
				# 	an error
				if not isinstance(options[i], str) \
					or not constants.regex[self._type].match(options[i]):
					raise ValueError(
						'"__options__[%d]" is not a valid "%s"' % (
							i, self._type
						)
					)

			# Else if it's decimal
			elif self._type == 'decimal':

				# If it's a Decimal
				if isinstance(options[i], Decimal):
					pass

				# Else if we can't conver it
				else:
					try: options[i] = Decimal(options[i])
					except ValueError:
						raise ValueError(
							'"__options__[%d]" not a valid "decimal"' % i
						)

			# Else if it's a float
			elif self._type == 'float':

				try:
					options[i] = float(options[i])
				except ValueError:
					raise ValueError(
						'"__options__[%d]" not a valid "float"' % i
					)

			# Else if it's an integer
			elif self._type in ['int', 'timestamp', 'uint']:

				# If we don't already have an int
				if not isinstance(options[i], int):

					# And we don't have a string
					if not isinstance(options[i], str):
						raise ValueError(
							'__options__[%d] is not a valid "%s"' % (
								i, self._type
							))

					try:
						options[i] = int(options[i], 0)
					except ValueError:
						raise ValueError(
							'__options__[%d] is not a valid "%s"' % (
								i, self._type
							))

				# If the type is unsigned and negative, raise an error
				if self._type in ['timestamp', 'uint'] and options[i] < 0:
					raise ValueError(
						'__options__[%d] is not a valid "%s"' % (
							i, self._type
						))

			# Else if it's a price
			elif self._type == 'price':

				# If it's a Decimal
				if isinstance(options[i], Decimal):
					pass

				# Else if it's not a valid price representation
				elif not isinstance(options[i], str) or \
					not constants.regex['price'].match(options[i]):
					raise ValueError(
						'__options__[%d] is not a valid "price"' % i
					)

				# Store it as a Decimal
				options[i] = Decimal(options[i])

			# Else if the type is a string
			elif self._type == 'string':

				# If the value is not a string
				if not isinstance(options[i], str):

					# If the value can't be turned into a string
					try:
						options[i] = str(options[i])
					except ValueError:
						raise ValueError(
							'__options__[%d] is not a valid "string"' % i
						)

			# Else we have no validation for the type
			else:
				raise TypeError(
					'can not set __options__ for "%s"' % self._type
				)

			# If it's already in the list, raise an error
			if options[i] in lOpts:
				raise ValueError('__options__[%d] is a duplicate' % i)

			# Store the option
			else:
				lOpts.append(options[i])

		# Store the list of options
		self._options = lOpts

	def regex(self, regex: str | Pattern = undefined):
		"""Regex

		Sets or gets the regular expression used to validate the Node

		Arguments:
			regex (str): A standard regular expression string, or compiled \
				regular expression

		Raises:
			ValueError

		Returns:
			None | str
		"""

		# If regex was not set, this is a getter
		if regex is undefined:
			return self._regex

		# If the type is not a string
		if self._type != 'string':
			raise ValueError('can not set __regex__ for "%s"' % self._type)

		# If it's a string, compile it
		if isinstance(regex, str):
			self._regex = re.compile(regex)

		# Else, if we got a Pattern
		elif type(regex) == _REGEX_TYPE:
			self._regex = regex

		# Else, we got an invalid value
		else:
			raise ValueError('"__regex__" must be a valid string or re.Pattern')

	def to_dict(self):
		"""To Dict

		Returns the Node as a dictionary in the same format as is used in \
		constructing it

		Returns:
			dict
		"""

		# Init the dictionary we will return
		dRet = {
			'__type__': self._type
		}

		# If there is a regex associated, add it
		if self._regex:

			# If we got a pattern
			if type(self._regex) == _REGEX_TYPE:
				dRet['__regex__'] = self._regex.pattern
			else:
				dRet['__regex__'] = self._regex

		# Else if there were options associated, add them
		elif self._options:
			dRet['__options__'] = self._options

		# Else check for min and max and add if either are found
		else:
			if self._minimum:
				dRet['__minimum__'] = self._minimum
			if self._maximum:
				dRet['__maximum__'] = self._maximum

		# Get the parents dict and add it to the return
		dRet.update(super(Node,self).to_dict())

		# Return
		return dRet

	def type(self):
		"""Type

		Returns the type of Node

		Returns:
			str
		"""
		return self._type

	def valid(self,
		value: any,
		ignore_missing = False,
		level: list[str] = undefined
	) -> bool:
		"""Valid

		Checks if a value is valid based on the instance's values. If any \
		errors occur, they can be found in [instance].validation_failures as a \
		list

		Arguments:
			value (any): The value to validate
			ignore_missing (bool): Optional, set to True to ignore missing nodes

		Returns:
			bool
		"""

		# Reset validation failures
		self._validation_failures = []

		# If the level is not passed
		if level is undefined:
			level = []

		# If the value is None
		if value is None:

			# If it's optional, or we're ignoring missing values, we're good
			if self._optional or ignore_missing:
				return True

			# Invalid value
			self._validation_failures.append(['.'.join(level), 'missing'])

		# If we are validating an ANY field, immediately return true
		if self._type == 'any':
			pass

		# If we are validating a DATE, DATETIME, IP or TIME data point
		elif self._type in ['base64', 'date', 'datetime', 'ip', 'md5', 'time',
							'uuid', 'uuid4']:

			# If it's a date or datetime type and the value is a python type
			if self._type == 'date' and isinstance(value, (date, datetime)):
				value = value.strftime('%Y-%m-%d')

			elif self._type == 'datetime' and \
				isinstance(value, (date, datetime)
			):
				if isinstance(value, datetime):
					value = value.strftime('%Y-%m-%d %H:%M:%S')
				elif isinstance(value, date):
					value = '%s 00:00:00' % value.strftime('%Y-%m-%d')

			# If it's a time type and the value is a python type
			elif self._type == 'time' and isinstance(value, (time, datetime)):
				value = value.strftime('%H:%M:%S')

			# Else if the type is md5 and the value is a python type
			elif self._type == 'md5' and isinstance(value, _MD5_TYPE):
				value = value.hexdigest()

			# If the value is not a string
			elif not isinstance(value, str):
				self._validation_failures.append([
					'.'.join(level),
					'not a string'
				])
				return False

			# If there's no match
			if not constants.regex[self._type].match(value):
				self._validation_failures.append(['.'.join(level), 'invalid'])
				return False

			# If we are checking an IP
			if self._type == 'ip':

				# If there's a min or a max
				if self._minimum is not None or self._maximum is not None:

					# If the IP is greater than the maximum
					if self._maximum is not None and \
						self.compare_ips(value, self._maximum) == 1:
						self._validation_failures.append([
							'.'.join(level),
							'exceeds maximum'
						])
						return False

					# If the IP is less than the minimum
					if self._minimum is not None and \
						self.compare_ips(value, self._minimum) == -1:
						self._validation_failures.append([
							'.'.join(level),
							'did not meet minimum'
						])
						return False

					# Return OK
					return True

		# Else if we are validating some sort of integer
		elif self._type in ['int', 'timestamp', 'uint']:

			# If the type is a bool, fail immediately
			if type(value) == bool:
				self._validation_failures.append(['.'.join(level), 'is a bool'])
				return False

			# If it's not an int
			if not isinstance(value, int):

				# And it's a valid representation of an int, convert it
				if isinstance(value, str) \
					and constants.regex['int'].match(value):
					value = int(value, 0)

				# Else, return false
				else:
					self._validation_failures.append([
						'.'.join(level),
						'not an integer'
					])
					return False

			# If it's not signed
			if self._type in ['timestamp', 'uint']:

				# If the value is below 0
				if value < 0:
					self._validation_failures.append([
						'.'.join(level),
						'signed'
					])
					return False

		# Else if we are validating a bool
		elif self._type == 'bool':

			# If it's already a bool
			if isinstance(value, bool):
				return True

			# If it's an int or long at 0 or 1
			if isinstance(value, int) and value in [0, 1]:
				return True

			# Else if it's a string
			elif isinstance(value, str):

				# If it's valid true or false string
				if value.lower() in ['on', 'true', 't', 'yes', 'y', 'x', '1',
			 						'', 'false', 'f', 'no', 'n', 'off', '0']:
					return True
				else:
					self._validation_failures.append([
						'.'.join(level),
						'not a valid string representation of a bool'
					])
					return False

			# Else it's no valid type
			else:
				self._validation_failures.append([
					'.'.join(level),
					'not valid bool replacement'
				])
				return False

		# Else if we are validating a decimal value
		elif self._type == 'decimal':

			# If the type is a bool, fail immediately
			if type(value) == bool:
				self._validation_failures.append(['.'.join(level), 'is a bool'])
				return False

			# If it's already a Decimal
			if isinstance(value, Decimal):
				pass

			# Else if we fail to convert the value
			else:
				try: value = Decimal(value)
				except (DecimalInvalid, TypeError, ValueError):
					self._validation_failures.append([
						'.'.join(level),
						'can not be converted to decimal'
					])
					return False

		# Else if we are validating a floating point value
		elif self._type == 'float':

			# If the type is a bool, fail immediately
			if type(value) == bool:
				self._validation_failures.append(['.'.join(level), 'is a bool'])
				return False

			# If it's already a float
			if isinstance(value, float):
				pass

			# Else if we fail to convert the value
			else:
				try: value = float(value)
				except (ValueError, TypeError):
					self._validation_failures.append([
						'.'.join(level),
						'can not be converted to float'
					])
					return False

		# Else if we are validating a JSON string
		elif self._type == 'json':

			# If it's already a string
			if isinstance(value, str):

				# Try to decode it
				try:
					value = jsonb.decode(value)
					return True
				except ValueError:
					self._validation_failures.append([
						'.'.join(level),
						'Can not be decoded from JSON'
					])
					return False

			# Else
			else:

				# Try to encode it
				try:
					value = jsonb.encode(value)
					return True
				except (ValueError, TypeError):
					self._validation_failures.append([
						'.'.join(level),
						'Can not be encoded to JSON'
					])
					return False

		# Else if we are validating a price value
		elif self._type == 'price':

			# If the type is a bool, fail immediately
			if type(value) == bool:
				self._validation_failures.append(['.'.join(level), 'is a bool'])
				return False

			# If it's not a floating point value
			if not isinstance(value, Decimal):

				# But it is a valid string representing a price, or a float
				if isinstance(value, (str, float)) \
					and constants.regex['price'].match(str(value)):

					# Convert it to a decimal
					value = Decimal(value).quantize(Decimal('1.00'))

				# Else if it's an int
				elif isinstance(value, int):

					# Convert it to decimal
					value = Decimal(str(value) + '.00')

				# Else whatever it is is no good
				else:
					self._validation_failures.append([
						'.'.join(level),
						'invalid'
					])
					return False

			# Else
			else:

				# If the exponent is longer than 2
				if abs(value.as_tuple().exponent) > 2:
					self._validation_failures.append([
						'.'.join(level),
						'too many decimal points'
					])
					return False

		# Else if we are validating a string value
		elif self._type == 'string':

			# If the value is not some form of string
			if not isinstance(value, str):
				self._validation_failures.append([
					'.'.join(level),
					'is not a string'
				])
				return False

			# If we have a regex
			if self._regex:

				# If it doesn't match the regex
				if not self._regex.match(value):
					self._validation_failures.append([
						'.'.join(level),
						'failed regex'
					])
					return False

			# If we have a min or max
			if self._minimum or self._maximum:

				# If there's a minimum length and we don't reach it
				if self._minimum and len(value) < self._minimum:
					self._validation_failures.append([
						'.'.join(level),
						'not long enough'
					])
					return False

				# If there's a maximum length and we surpass it
				if self._maximum and len(value) > self._maximum:
					self._validation_failures.append([
						'.'.join(level),
						'too long'
					])
					return False

				# Return OK
				return True

		# If there's a list of options
		if self._options is not None:

			# Returns based on the option's existance
			if value not in self._options:
				self._validation_failures.append([
					'.'.join(level),
					'not in options'
				])
				return False
			else:
				return True

		# Else check for basic min/max
		else:

			# If the value is less than the minimum
			if self._minimum and value < self._minimum:
				self._validation_failures.append([
					'.'.join(level),
					'did not meet minimum'
				])
				return False

			# If the value is greater than the maximum
			if self._maximum and value > self._maximum:
				self._validation_failures.append([
					'.'.join(level),
					'exceeds maximum'
				])
				return False

		# Value has no issues
		return True

# Register with Base
Node.register('node')
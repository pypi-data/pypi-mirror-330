# coding=utf8
"""Base

Contains the class that all other Define classes extend from
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-18"

# Limit exports
__all__ = ['Base']

# Ouroboros imports
import jsonb
from tools import clone, combine
import undefined

# Python imports
import abc
import copy
import sys
from typing import Literal as TL

# Local imports
from define import constants

class Base(abc.ABC):
	"""Base

	The class all other Define types must extend

	Extends:
		abc.ABC
	"""

	__classes = {}
	"""Classes used to create new define types"""

	__name = None
	"""The name if it's a field of another Define structure"""

	def __init__(self, details: dict, name: str = None):
		"""Constructor (__init__)

		Creates a new instance

		Arguments:
			details (dict): The define structure
			name (str): The name of the field if it is one
		"""

		# If the details are not an object
		if not isinstance(details, dict):
			raise ValueError('details must be a dict in %s.%s' % (
				self.__class__.__name__,
				sys._getframe().f_code.co_name
			))

		# Store the class name for the child
		self.__class = self.__class__.__name__

		# Store the structure name
		self.__name = name

		# Init the list of the last failures generated in valid
		self._validation_failures = None

		# Init the optional flag, assume all nodes are necessary
		self._optional = False

		# If the details contains an optional flag
		if '__optional__' in details:

			# If it's a valid bool, store it
			if isinstance(details['__optional__'], bool):
				self._optional = details['__optional__']

			# Else, raise an error
			else:
				raise ValueError('"__optional__" must be a bool')

			# Remove it from details
			del details['__optional__']

		# Init the special dict
		self.__special = {}

		# If there are any other special fields in the details
		for k in tuple(details.keys()):

			# If the key is used by the child
			if k in constants.special['reserved']:
				continue

			# If key is special
			oMatch = constants.special['key'].match(k)
			if oMatch:

				# Store it with the other specials then remove it
				self.__special[oMatch.group(1)] = details[k]
				del details[k]

	def __repr__(self):
		"""Representation (__repr__)

		Returns a string representation of the instance

		Returns:
			str
		"""
		return '<%s: %s>' % (
			self.class_name(),
			str(self.to_dict())
		)

	def class_name(self):
		"""Class Name

		Returns the class of the Node instance

		Returns:
			str
		"""
		return self.__class

	@abc.abstractmethod
	def clean(self, value: any, level: list[str]):
		"""Clean

		As validation allows for strings representing non-string values, it is \
		useful to be able to "clean" a value and turn it into the value it was \
		representing, making sure that data in data stores is accurate, and \
		not representitive

		Arguments:
			value (any): The value to clean

		Returns:
			any
		"""
		pass

	@classmethod
	def create(cls, details: dict, name: str = None):
		"""Create

		Figure out the child node type necessary and create an instance of it

		Arguments:
			details (dict): An object describing a data point
			name (str): The name if it's a field of another Define

		Returns:
			any
		"""

		# If it's an array, create a list of options
		if isinstance(details, list):
			return cls.__classes['__options__'](details, name = name)

		# Else if we got an object
		elif isinstance(details, dict):

			# Go through the classes that can be created
			for name in cls.__classes:

				# Skip foundation classes
				if name in ['__node__', '__options__', '__parent__']:
					continue

				# If the name exists in the details
				if name in details:
					return cls.__classes[name](details, False, name)

			# Else, if we have a type
			if '__type__' in details:

				# If the __type__ is an object or an array, it's a complex type
				if isinstance(details['__type__'], dict) or \
					isinstance(details['__type__'], list):

					# And we need to use the __type__ as the details
					return cls.create(details['__type__'], name)

				# Else it's just a Node
				else:
					return cls.__classes['__node__'](details, False, name)

			# Else it's most likely a parent
			else:
				return cls.__classes['__parent__'](details, False, name)

		# Else if we got a string, use the value as the type, and create a node
		elif isinstance(details, str):
			return cls.__classes['__node__'](details, False, name)

		# Else, raise an error
		else:
			raise ValueError('details in %s.%s invalid\n%s' % (
				cls.__name__,
				sys._getframe().f_code.co_name,
				str(details)
			))

	@classmethod
	def from_file(cls, filename: str, extend: dict | TL[False] = False):
		"""From File

		Loads a JSON file and creates a Node instance from it

		Arguments:
			filename (str): The filename to load,
			extend (dict | False): Optional, a dictionary to extend the \
				definition

		Returns:
			Base
		"""

		# Load the file as a dict
		dDetails = jsonb.load(filename)

		# Create and return the new instance
		return cls(dDetails, extend)

	@staticmethod
	def make_details(details: dict | str, extend: dict):
		"""Make Details

		Common function for merging the `details` with `extend`

		Arguments:
			details (dict | str): Definition, or path to the file containing it
			extend (dict): A dictionary to extend the definition of `details`

		Returns:
			dict
		"""

		# If the details are a string
		if isinstance(details, str):

			# Consider it a filepath and load the file
			details = jsonb.load(details)

		# If details is not a dict instance
		if not isinstance(details, dict):
			raise ValueError('details must be a dict')

		# Init the return
		dReturn: dict = None

		# If we have no extend at all
		if extend is undefined:

			# Make a copy of the details so we don't screw up the original
			#	object
			dReturn = clone(details)

		# Else, we have an extend value
		else:

			# If it's a dictionary
			if isinstance(extend, dict):

				# Store the details by making a new object from the details and
				#	the extend
				dReturn = combine(details, extend)

			# Else, if it's false
			elif extend == False:

				# Just use the details as is, don't copy it
				dReturn = details

			# Else, we got some sort of invalid value for extend
			else:
				raise ValueError('if set, extend must be a dict or False')

		# Return whatever details were generated
		return dReturn

	def name(self) -> None | str:
		"""Name

		Returns the name of the field if it is one

		Returns:
			str | None
		"""
		return self.__name

	def optional(self, value: bool | None = None):
		"""Optional

		Getter/Setter method for optional flag

		Arguments:
			value (bool): If set, the method is a setter

		Returns:
			bool | None
		"""

		# If there's no value, this is a getter
		if value is None:
			return self._optional

		# Else, set the flag
		else:
			self._optional = value and True or False

	@classmethod
	def register(cls, name: str):
		"""Register

		Registers the class as a child that can be created

		Arguments:
			name (str): the name of the class that will be added

		Returns:
			None
		"""

		# If someone tries to register 'type'
		if name == 'type':
			raise ValueError('"type" is a reserved value in define')

		# Generate the name as a special field
		s = '__%s__' % name

		# If the name already exists
		if s in cls.__classes:
			raise ValueError('"%s" already registered' % name)

		# Store the new constructor
		cls.__classes[s] = cls

	def special(self, name: str, default: any = None) -> any:
		"""Special

		Get special values associated with nodes

		Args:
			name (str): The name of the value to either get
			default (any): The default value. Returned if the special field \
				doesn't exist

		Raises:
			TypeError: If the name is not a valid string
			ValueError: If the name is invalid

		Returns:
			Returns the special value, or the default
		"""

		# Check the name is a string
		if not isinstance(name, str):
			raise TypeError('name must be a string')

		# Check the name is valid
		if not constants.special['name'].match(name):
			raise ValueError(
				'special name must match "%s"' % constants.special['syntax']
			)

		# Return the value or the default
		try:
			return copy.deepcopy(self.__special[name])
		except KeyError:
			return default

	def special_set(self, name: str, value: any) -> bool:
		"""Special

		Traditionally we don't atlter data after instantiation, but just in
		case it is needed, it is possible to overwrite special values

		Arguments:
			name (str): The name of the value to either set
			value (any): The value to set. Must be something that can be \
				converted directly to JSON

		Raises:
			TypeError: If the name is not a valid string
			ValueError: If the name is invalid, or if setting and the value \
				can not be converted to JSON

		Returns:
			None
		"""

		# Check the name is a string
		if not isinstance(name, str):
			raise TypeError('name must be a string')

		# Check the name is valid
		if not constants.special['name'].match(name):
			raise ValueError(
				'special name must match "%s"' % constants.special['syntax']
			)

		# Can the value safely be turned into JSON
		try:
			jsonb.encode(value)
		except TypeError:
			raise ValueError('"%s" can not be encoded to JSON in %s.%s' % (
				self.__class__.__name__,
				sys._getframe().f_code.co_name
			))

		# Save it
		self.__special[name] = value

	def to_dict(self):
		"""To Dict

		Returns the basic node as a dictionary in the same format as is used \
		in constructing it

		Returns:
			dict
		"""

		# Create the dict we will return
		dRet = {}

		# If the optional flag is set
		if self._optional:
			dRet['__optional__'] = True

		# Add all the special fields found
		for k in self.__special.keys():
			dRet['__%s__' % k] = self.__special[k]

		# Return
		return dRet

	def to_json(self):
		"""To JSON

		Returns a JSON string representation of the instance

		Returns:
			str
		"""
		return jsonb.encode(self.to_dict())

	@abc.abstractmethod
	def valid(self,
		value: any,
		ignore_missing = False,
		level: list[str] = undefined
	) -> bool:
		"""Valid

		Checks if a value is valid based on the instance's values

		Args:
			value (mixed): The value to validate
			ignore_missing (bool): Optional, set to True to ignore missing nodes

		Returns:
			bool
		"""
		pass

	@property
	def validation_failures(self) -> list[list[str]]:
		"""Validation Failures

		Returns the last failures as a property so they can't be overwritten

		Returns:
			[field, error][]
		"""
		return self._validation_failures
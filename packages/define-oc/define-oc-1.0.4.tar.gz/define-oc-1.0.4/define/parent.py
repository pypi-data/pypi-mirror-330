# coding=utf8
"""Parent

Represents defined keys mapped to other Nodes which themselves could be Parents
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-19"

# Limit exports
__all__ = ['Parent']

# Ouroboros imports
import undefined

# Python imports
from typing import Literal as TL

# Local imports
from define import constants
from define.base import Base

class Parent(Base):
	"""Parent

	Represents defined keys mapped to other Nodes which themselves could be \
	Parents

	Extends:
		Base
	"""

	def __contains__(self, key):
		"""Contain (__contains__)

		Returns whether a specific key exists in the parent

		Arguments:
			key (str): The key to check for

		Returns:
			bool
		"""
		return key in self._nodes

	def __getitem__(self, key):
		"""Get Item (__getitem__)

		Returns a specific key from the parent

		Arguments:
			key (str): The key to get

		Raises:
			KeyError

		Returns:
			mixed
		"""
		return self._nodes[key]

	def __init__(self,
		details: dict,
		extend: dict | TL[False] = False,
		name: str = None):
		"""Constructor

		Initialises the instance

		Arguments:
			details (dict): Definition
			extend (dict | False): Optional, a dictionary to extend the \
				definition
			name (str): The name if it's a field of another Define

		Raises:
			KeyError, ValueError

		Returns
			Parent
		"""

		# Generate the details
		dDetails = Base.make_details(details, extend)

		# Call the parent constructor
		super(Parent, self).__init__(dDetails, name)

		# Init the nodes and requires dicts
		self._nodes = {}
		self._requires = {}

		# Go through the keys in the details
		for k in tuple(dDetails.keys()):

			# If key is standard
			if constants.standard.match(k):

				# If it's a Node
				if isinstance(dDetails[k], Base):

					# Store it as is
					self._nodes[k] = dDetails[k]

				# Else, create it
				else:
					self._nodes[k] = self.create(dDetails[k], k)

		# If there's a require hash available
		if '__require__' in dDetails:
			self.requires(dDetails['__require__'])

	def __iter__(self):
		"""Iterator (__iter__)

		Returns an iterator to the parent's keys

		Returns:
			dictionary-keyiterator
		"""
		return iter(self._nodes.keys())

	def child(self, key: str, default: any = None):
		"""Get

		Returns the node of a specific key from the parent

		Arguments:
			key (str): The key to get
			default (any): Optional, value to return if the key does not exist

		Returns:
			any
		"""
		try:
			return self._nodes[key]
		except KeyError:
			return default

	def clean(self, value: dict, level: list = undefined):
		"""Clean

		Goes through each of the values in the dict, cleans it, stores it, and \
		returns a new dict

		Arguments:
			value (dict): The value to clean

		Returns:
			dict
		"""

		# If the level isn't passed
		if level is undefined:
			level = []

		# If the value is None
		if value is None:

			# If it's optional, return as is
			if self._optional:
				return None

			# Missing value
			raise ValueError([['.'.join(level), 'missing']])

		# If the value is not a dict
		if not isinstance(value, dict):
			raise ValueError([['.'.join(level), 'not a valid Object']])

		# Init the return value
		dRet = {}

		# Go through each value and clean it using the associated node
		lErrors = []
		for k in value.keys():

			# Add the field to the level
			lLevel = level[:]
			lLevel.append(k)

			try:
				dRet[k] = self._nodes[k].clean(value[k], lLevel)
			except KeyError:
				lErrors.append(['.'.join(lLevel), 'not a valid node'])
			except ValueError as e:
				lErrors.extend(e.args[0])

		# If there's any errors
		if lErrors:
			raise ValueError(lErrors)

		# Return the cleaned values
		return dRet

	def has_key(self, key: str):
		"""Has Key

		Returns whether a specific key exists in the parent

		Arguments:
			key (str): The key to check for

		Returns:
			bool
		"""
		return key in self._nodes

	def keys(self):
		"""Keys

		Returns a list of the node names in the parent

		Returns:
			list
		"""
		return tuple(self._nodes.keys())

	@property
	def nodes(self):
		"""Nodes Property

		Creates a read only attribute to access the instances child nodes

		Returns:
			dict
		"""
		return self._nodes

	def requires(self, require = undefined):
		"""Requires

		Setter/Getter for the require rules used to validate the Parent

		Arguments:
			require (dict): A dictionary expressing requirements of fields

		Raises:
			ValueError

		Returns:
			None
		"""

		# If require is not passed
		if require is undefined:
			return self._requires

		# If it's not a valid dict
		if not isinstance(require, dict):
			raise ValueError('__require__ must be a valid dict')

		# Init the new require
		dRequire: dict = None

		# Go through each key and make sure it goes with a field
		for k,v in require.items():

			# If the field doesn't exist
			if k not in self._nodes:
				raise ValueError(
					'__require__[%s] does not exist in the Parent' % str(k)
				)

			# If the value is a string
			if isinstance(v, str):
				if require[k] not in self._nodes:
					raise ValueError(
						'__require__[%s]: %s' % (str(k), str(require[k]))
					)
				dRequire[k] = [v]

			# Else, if it's a list
			elif isinstance(v, list):

				# Make sure each required field also exists
				for s in v:
					if s not in self._nodes:
						raise ValueError(
							'__require__[%s]: %s' % (str(k), str(v))
						)

			# Else, it's invalid
			else:
				raise ValueError(
					'__require__[%s] must be a single string or a list' % k
				)

		# Set the new requires
		self._requires = dRequire

	def to_dict(self):
		"""To Dict

		Returns the Parent as a dictionary in the same format as is used in \
		constructing it

		Returns:
			dict
		"""

		# Get the parents dict as the starting point of our return
		dRet = super(Parent,self).to_dict()

		# Go through each field and add it to the return
		for k,v in self._nodes.items():
			dRet[k] = v.to_dict()

		# Return
		return dRet

	def valid(self,
		value: dict,
		ignore_missing = False,
		level: list = []
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

		# If the value is None
		if value is None:

			# If it's optional, or we're ignoring missing values, we're good
			if self._optional or ignore_missing:
				return True

			# Invalid value
			self._validation_failures.append(['.'.join(level), 'missing'])

		# If the value isn't a dictionary
		if not isinstance(value, dict):
			self._validation_failures.append(['.'.join(level), str(value)])
			return False

		# Init the return, assume valid
		bRet = True

		# Store the keys of the values sent
		lKeys = list(value.keys())

		# Go through each node in the instance
		for k in self._nodes:

			# Add the field to the level
			lLevel = level[:]
			lLevel.append(k)

			# If we are missing a node
			if k not in value:

				# If the value is not optional and we aren't ignoring missing
				if not self._nodes[k]._optional and not ignore_missing:
					self._validation_failures.append(
						['.'.join(lLevel), 'missing']
					)
					bRet = False

				# Continue to next node
				continue

			# Remove it from the list of keys sent
			lKeys.remove(k)

			# If the element isn't valid, return false
			if not self._nodes[k].valid(value[k], ignore_missing, lLevel):
				self._validation_failures.extend(
					self._nodes[k].validation_failures
				)
				bRet = False
				continue

			# If the element requires others
			if k in self._requires:

				# Go through each required field
				for f in self._requires[k]:

					# If the field doesn't exist in the value
					if f not in value or value[f] in ('0000-00-00','',None):
						self._validation_failures.append([
							'.'.join(lLevel),
							'requires \'%s\' to also be set' % str(f)
						])
						bRet = False

		# If we have any extra keys
		if lKeys:

			# Set this as a failure
			bRet = False

			# Add each as an unknown
			for s in lKeys:
				lLevel = level[:]
				lLevel.append(s)
				self._validation_failures.append(['.'.join(lLevel), 'unknown'])

		# Return whatever the result was
		return bRet

# Register with Base
Parent.register('parent')
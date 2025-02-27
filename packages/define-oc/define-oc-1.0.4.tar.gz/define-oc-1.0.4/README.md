# Define
[![pypi version](https://img.shields.io/pypi/v/define-oc.svg)](https://pypi.org/project/define-oc) ![MIT License](https://img.shields.io/pypi/l/define-oc.svg)

Define uses JSON as a language independant way to describe data types that can
then be validated, and in the case of all strings form data, cleaned up and
turned into the appropriate variable type.

## Install
```bash
pip install define-oc
```

## Using
Defining data can be done at runtime with dicts and lists, but one of the
advantages of creating definition files in JSON is being able to share them with
your front end systems to allow validating data with the same rules in the
browser or app before even sending it to the server.

user.json
```json
{
	"id": "uuid4",
	"email": {
		"__type__": "string",
		"__regex__": ""
	},
	"name": {
		"first": "string",
		"middle": {
			"__type__": "string",
			"__maximum__": 1,
			"__optional__": true
		},
		"last": "string"
	},
	"address": {
		"line1": "string",
		"line2": {
			"__type__": "string",
			"__optional__": true
		},
		"city": "string",
		"state": {
			"__type__": "string",
			"__regex__": "[A-Z]{2}"
		},
		"country": {
			"__type__": "string",
			"__options__": [ "CA", "MX", "US" ]
		}
	},
	"phone": "string",
	"dob": {
		"__type__": "date",
		"__optional__": true
	},
	"height": {
		"feet": {
			"__type__": "uint",
			"__maximum__": 7
		},
		"inches": {
			"__type__": "uint",
			"__maximum__": 11
		},
		"__optional__": true
	}
}
```

Once defined, the data can be used in Python using the available classes.

user.py
```python
from define import Parent
import json
import sys

# Load the file
definition = {}
with open('user.json', 'r') as f:
	definition = json.load(f)

# Create the Parent instance
parent = Parent(definition)

# Test data
data = {
	'id': '52cd4b20-ca32-4433-9516-0c8684ec57c2',
	'email': 'chris@domain.com',
	'name': {
		'first': 'Chris',
		'last': 'Nasr'
	},
	'address': {
		'line1': '123 Main Street',
		'state': 'QC',
		'country': 'CA'
	},
	'phone': '(888) 555-1234',
	'height': {
		'feet': '5',
		'inches': '11'
	}
}

if not parent.valid(data):
	print(tree.validation_failures)
	# [ [ 'address.city', 'missing' ] ]

# Clean the data
data = tree.clean(data)
"""
{ ...
  height: {
    'feet': 5,
    'inches': 11
  }
}
"""
```

## Extending
Any fields marked by two leading and trailing underscores is considered a
special value and can be accessed using the `special` method. This can be used
to add details only relevent to a specific system, either directly, or through
the use of classes that inherit the Define classes.

For example, a class that handles storing the data in a database might need
extra data to know how to convert the Define type to an equivalent database
type, or to limit that type.

user.json
```json
{
	...
	"name": {
		"first": {
			"__type__": "string",
			"__maximum__": 32,
			"__sql_type__": "varchar(32)"
		},
		"middle": {
			"__type__": "string",
			"__maximum__": 1,
			"__optional__": true,
			"__sql_type__": "char(1)"
		},
		"last": {
			"__type__": "string",
			"__maximum__": 32,
			"__sql_type__": "varchar(32)"
		}
	},
	...
}
```

Or, if we don't want this data in the shared file, we can add it at runtime and
let the class merge the two.

user.py
```python
...
# Create the Parent instance
parent = Parent(definition, {
	'name': {
		'__sql_type__': 'varchar(32)'
	},
	'middle': {
		'__sql_type__': 'char(1)'
	},
	'last': {
		'__sql_type__': 'varchar(32)'
	}
})
...
```

Then we can access that data at runtime

```python
...
# Get the SQL type for the first name field
name_first_type = parent['name']['first'].special('sql_type')
```

## Documentation
Full documentation, including information on using Arrays and dynamic Objects,
as well as how to handle errors, can be found on
[ouroboroscoding.com/define](https://ouroboroscoding.com/define)
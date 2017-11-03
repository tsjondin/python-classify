WIP ! WIP ! WIP ! WIP ! WIP ! WIP ! WIP ! WIP

# Classify

Classify takes raw python objects structures, such as dicts, lists, tuples etc.
and creates type-checked datastructures based on given model of classification.

## Example

One may have a REST api which recieves JSON data, but simply loading this data
and assuming that it is correct can be dangerous and error prone. Writing
explicit validators is tedious so simply write a model that the data should
conform to.

	raw_json_blob # A blob of json from an API request

	class ResourceModel:
		name = str
		count = int
		value = float

	try:
		classify(ResourceModel, json.loads(raw_json_blob))
	except TypeError as e:
		# Treat the validation error as you wish

Given this example the data given by json.loads must conform to the ResourceModel, that is it must look something like:

	{
		"name": "some name",
		"count": 2,
		"value": 7.45
	}

Any other types of values, such as an int in the floats position or vice versa will cause a TypeError.

You may also nest models and Classify will follow the model hierarchy and classify the underlying data as well.

	raw_json_blob # A blob of json

	class ResourceModelB:
		a_value = str

	class ResourceModelA:
		a_reference = B

	try:
		classify(ResourceModelA, json.loads(raw_json_blob))
	except TypeError as e:
		# Treat the validation error as you wish

I which case the data provided in the JSON under the key *a_reference* must
conform to the model of ResourceModelB.

Classify returns instances of the models to check against
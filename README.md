# Classify

Classify takes python object structures, such as dicts, lists, tuples etc.
and validates them against given typed models (classes), returning the object
structure as instances of the models they were validated against.

Classify considers all types based on a classes to be models, and expects the
properties on the models to have types as values to validate against, such as:

	class A:
		property = str

To classify data against this model you would have a dict:

	data = {"property": "Hello world!"}

And then call classify:

	obj = classify(A, data)

This would validate against the model A and return an instance of the model A
with its "property" set to "Hello world!"

## Usefullness

One may have a REST api which recieves JSON data, simply loading this data
and assuming that it is correct may be dangerous and error prone. Writing
explicit validators is tedious. With a library such as classify you simply
write a model that the data should conform to.

	class ResourceModel:
		name = str
		count = int
		value = float

Such as this ResourceModel, using it is as easy as:

	raw_json_blob # A blob of json from an API request
	try:
		classify(ResourceModel, json.loads(raw_json_blob))
	except TypeError as e:
		# Treat the validation error as you wish

Given this example the data given by json.loads must conform to the
ResourceModel, that is, it must look something like:

	{
		"name": "some name",
		"count": 2,
		"value": 7.45
	}

Any other types of values, such as an int in the floats position or vice versa
will cause a TypeError.

You may also nest models and Classify will follow the model hierarchy and
classify the underlying data as well.

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

## Types

As said before; classify sees all classes as models, so, while not really
usefull, a model can be as simple as only a string, e.g.:

	classify(str, "Hello world!")

Which in essence will only perform an instanceof check and return the string

So for more interesting types such as lists and enums the model must no be an
instance of a class but the class itself, which works fine in the case of Enum:

	classify(Enum('MyEnum', [('A', 1), ('B', 2)]), 'A')

Enum validates that the key given ('A') exists on the enum and returns MyEnum.A
If using IntEnum you may also retrieve an Enum value based of the integer, e.g.:

	classify(IntEnum('MyIntEnum', [('A', 1), ('B', 2)]), 1)

Which returns MyIntEnum.A

But for lists you have to use classify's supplied "typedlist" interface, which
simply returns a class that contains type information that must be true for all
elements of the list.

	classify(typedlist(str), ["A", "B", "C"])

Above would validate that each element of the list is a string, but more
interestingely you may supply any class (model) to the typedlist:

	class MyComplex:
		a: str
		b: int
		c: float

	classify(typedlist(MyComplex), [ ... ])

And classify will validate that all elements are valid against the MyComplex model.

## Adding types

In classify you do no add new types, it can use "any class" as long as you have
registered a classifier for that class, this is done either via the register
function or the classifier decorator, as an example of registering
ipaddress.IPv4Address:

	# Using register

	def classify_ipaddress(data, model):
		try:
			return model(data)
		except AddressValueError:
			raise TypeError('Given value {} is not a valid IPv¤ address'.format(data))
	register(ipaddress.IPv4Address, classify_ipaddress)

	# Using classifier

	@classifier(ipaddress.IPv4Address)
	def classify_ipaddress(data, model):
		try:
			return model(data)
		except AddressValueError:
			raise TypeError('Given value {} is not a valid IPv¤ address'.format(data))

## Union

Going back to the REST API examples, there may be cases where your API should
accept different values in different situations, such as different combinations
of options, just because it was one of the reasons I started making this
library I will show an example that accepts different permutations of SNMP
options using Unions.

	class SNMPv2:
    		community = str


	class SNMPv3:
    		userName = str
    		authKey = str
    		authProtocol = Enum('AuthProtocol', ('DES'))
    		privKey = str
    		privProtocol = Enum('PrivProtocol', ('AES'))


	class SNMPv3NoAuth:
    		userName = str
    		privKey = str
    		privProtocol = Enum('PrivProtocol', ('AES'))


	class SNMPv3NoAuthNoPriv:
    		userName = str

	class SNMPUsingResource
		snmp = union(SNMPv2, SNMPv3, SNMPv3NoAuth, SNMPv3NoAuthNoPriv)
		...

Here the class SNMPUsingResource represents a resource we want to create from
a POST request, it should contain SNMP options, but the backend supports all
versions of SNMP so how do we validate the options when they depend on other
options?

With classify you can solve this using Unions, if the request only contains a
community property (with a string value) under its "snmp" key, the
resource.snmp of the resource instance will be an instance of SNMPv2.

If all v3 options are supplied you will get an SNMPv3 instance and so on. Any
non-matching combinations will result in a union error (i.e. data does not
match any model in union)

## Intersection

Intersections allow you to combine models to create larger models, this allows
you to abstract commonalities between such things as resources. Given a larger
API where all resources may have uuid and name.

	class IdentifiableResource:
		uuid = UUID
		name = str

	class SpecificResource:
		bee = str
		bop = int
		bido = float

	classify(intersection(SpecificResource, IdentifiableResource), ...data)

The data must now fullfill the interface of both the SpecificResource and
IdentifiableResource, if it does then classify will return an instanceof
with the type Intersection<SpecificResource & IdentifiableResource> which
inherits from both of the classes.

It does this inheritance to that one may use isinstance for checking types
since the Intersection type is dynamic and not accessable from call-site
without retrieving it via the type() function.

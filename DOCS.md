Module classify
---------------

Functions
---------
## classifier(model)
Decorator version of register, see register(model, classifier)
## classify(model, data)
Classifies the given *data* as the *model* type, any type issue will raise
TypeError, if no error is raised it will return an instance of the
type/model given as the *model*

**Keyword arguments**:

* model -- a model (class) to classify the data as
* data -- a python datastructure, such as dict, list etc.
## register(model, classifier)
Registers a classifier for a type, this classifier is used to validate
whether a simpler representation of a type is representative of the type
and should return an instance of type model.

**Keyword arguments**:

* model -- The type to validate
* classifier -- The function that performs the validation

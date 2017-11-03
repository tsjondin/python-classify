Module classify
---------------

Functions
---------
## classifier(T)
Decorator version of register, see register(T, classifier)
## classify(model, data)
Classifies the given *data* as the *model* type, any type issue will raise
TypeError, if no error is raised it will return an instance of the
type/model given as the *model*

**Keyword arguments**:

* model -- a model (class) to classify the data as
* data -- a python datastructure, such as dict, list etc.
## declassify(model, data)
!! NOT YET IMPLEMENTED !!

Declassifies the given *data* from the *model* model/type, any type issue
will raise TypeError, if no error is raised it will return a python type
appropriate for the model/class given

**Keyword arguments**:

* model -- a model (class) to declassify the data from
* data -- a python instance
## register(T, classifier)
Registers a classifier for a type, this classifier is used to validate
whether a simpler representation of a type is representative of the type
and should return an instance of type T.

**Keyword arguments**:

* T -- The type to validate
* classifier -- The function that performs the validation

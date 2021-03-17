# aquacal
A sample project that demonstrates mocking in Python.

# Getting Started

1. Clone the repository and create a new branch:

```bash
git clone https://github.com/Aquaveo/aquacal.git
cd aquacal
git checkout -b tutorial
```

2. Create a conda environment with the needed dependencies:

```bash
conda env create -n environment.yml
```

3. Open the aquacal directory as a new project in PyCharm.

4. Set the Python Interpretter to use the conda environment you created in step 2.

# Python Mock Primer

Many examples in this repo are based on those from this excellent tutorial: https://realpython.com/python-mock-library/#the-mock-object
Python Documentation: https://docs.python.org/3/library/unittest.mock.html

The Mock class can be used as a base class for mocking objects.

```
>>> from unittest.mock import Mock
>>> mock = Mock()
>>> mock
<Mock id='4561344720'>
```

Attributes and methods are defined lazily when you access them:

```python
>>> mock.some_attribute
<Mock name='mock.some_attribute' id='4394778696'>
>>> mock.do_something()
<Mock name='mock.do_something()' id='4394778920'>
```

Notice how the returned value is another mock object and the name of the object is the call path.

## Mocked Methods

1. Require no arguments.
2. Accept any arguments.
3. Returns another Mock.

```python
>>> json = Mock()
>>> json.loads('{"k": "v"}').get('k')
<Mock name='mock.loads().get()' id='4379599424'>
```

Mock objects store data on how you use them. You can use this data to test that they are being used correctly:

## Assertions

Use assertions in your tests to verify methods being called or called with certain arguments.

```python
>>> from unittest.mock import Mock

>>> # Create a mock object
>>> json = Mock()

>>> json.loads('{"key": "value"}')
<Mock name='mock.loads()' id='4550144184'>

>>> # You know that you called loads() so you can
>>> # make assertions to test that expectation
>>> json.loads.assert_called()
>>> json.loads.assert_called_once()
>>> json.loads.assert_called_with('{"key": "value"}')
>>> json.loads.assert_called_once_with('{"key": "value"}')

```

```python
>>> from unittest.mock import Mock

>>> # Create a mock object
>>> json = Mock()

>>> json.loads('{"key": "value"}')
<Mock name='mock.loads()' id='4550144184'>
>>> json.loads('{"key": "value"}')
<Mock name='mock.loads()' id='4550144184'>

>>> # If an assertion fails, the mock will raise an AssertionError
>>> json.loads.assert_called_once()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/unittest/mock.py", line 795, in assert_called_once
    raise AssertionError(msg)
AssertionError: Expected 'loads' to have been called once. Called 2 times.

>>> json.loads.assert_called_once_with('{"key": "value"}')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/unittest/mock.py", line 824, in assert_called_once_with
    raise AssertionError(msg)
AssertionError: Expected 'loads' to be called once. Called 2 times.

>>> json.loads.assert_not_called()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/unittest/mock.py", line 777, in assert_not_called
    raise AssertionError(msg)
AssertionError: Expected 'loads' to not have been called. Called 2 times.
```

## Inspection

For more complex cases, you may need to inspect the calls and call arguments yourself to determine if a method was used correctly.

```python
>>> from unittest.mock import Mock

>>> # Create a mock object
>>> json = Mock()
>>> json.loads('{"key": "value"}')
<Mock name='mock.loads()' id='4391026640'>

>>> # Number of times you called loads():
>>> json.loads.call_count
1
>>> # The last loads() call:
>>> json.loads.call_args
call('{"key": "value"}')
>>> # List of loads() calls:
>>> json.loads.call_args_list
[call('{"key": "value"}')]
>>> # List of calls to json's methods (recursively):
>>> json.method_calls
[call.loads('{"key": "value"}')]
```

## Return Values

You can control the return value of Mock methods:

```python
>>> json = Mock()
>>> json.loads.return_value = {"key": "value"}
>>> json.loads()
{"key": "value"}
```

## Side Effects 

You can control other call behaviors using side_effect. For example you can have the function raise an exception by assigning an exception to side_effect:

```python
>>> json = Mock()
>>> json.loads.side_effect = ValueError
>>> json.loads()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "...\unittest\mock.py", line 1093, in __call__
    return self._mock_call(*args, **kwargs)
  File "...\unittest\mock.py", line 1097, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
  File "...\unittest\mock.py", line 1152, in _execute_mock_call
    raise effect
ValueError
```

Assiging an iterable to side_effect will define the return value or behavior of the called function for each successive call:

```python
>>> json = Mock()
>>> json.loads.side_effect = [{"key": "value"}, ValueError]

>>> # First call
>>> json.loads()
{"key": "value"}

>>> # Second call
>>> json.loads()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "...\unittest\mock.py", line 1093, in __call__
    return self._mock_call(*args, **kwargs)
  File "...\unittest\mock.py", line 1097, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
  File "...\unittest\mock.py", line 1152, in _execute_mock_call
    raise effect
ValueError
```

Finally, you can define a custom function to be called in place of the mocked method when it is called:

```python
>>> def mock_json_loads(*arg):
...     for a in args:
...         print(a)
...
>>> json = Mock()
>>> json.loads.side_effect = mock_json_loads
>>> json.loads('{"key": "value"}')
{"key": "value"}
```

## Configuring Mocks

You can configure return_value and side_effect when creating the Mock objects:

```python
>>> import json
>>> from unittest.mock import Mock
>>> json.loads = Mock(return_value={"key": "value"})
>>> json.dumps = Mock(side_effect=OSError)
>>> json.loads()
{'key': 'value'}
>>> json.dumps()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "...\unittest\mock.py", line 1093, in __call__
    return self._mock_call(*args, **kwargs)
  File "...\unittest\mock.py", line 1097, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
  File "...\unittest\mock.py", line 1152, in _execute_mock_call
    raise effect
OSError
```

## Configure Mock Attributes

When creating a Mock object, you can also define the attribute values. All other attributes will be defined when called as usual:

```python
>>> mock = Mock(a=1, b="foo")
>>> mock.a
1
>>> mock.b
'foo'
>>> mock.c
<Mock name='mock.c' id='1553003785616'>
```

## Special Attributes

Using `name` in the constructor is "special" and probably won't behave as expected:

```python
>>> # Setting the name in the constructor sets the name of the Mock in the repr, which can be helpful when debugging
>>> mock = Mock(name='MyMock')
>>> mock.name
<Mock name='MyMock.name' id='1552999833456'>

>>> # Set the value of a "name" attribute on the Mock by setting it after constructing the Mock
>>> mock.name = 'TheName'
>>> mock.name
'TheName'

# Note that the Mock name is unaffected by setting a "name" attribute
>>> mock.foo
<Mock name='MyMock.foo' id='1553003933552'>
```

## Spec

You can set a spec on a Mock object so that it will pass `isinstance()` tests:

```python
>>> class Thing:
...     a = 1
...     b = "foo"
...
>>> mock_thing = Mock(spec=Thing)
>>> mock_thing
<Mock spec='Thing' id='1553034241744'>
>>> isinstance(mock_thing, Thing)
True
```

Setting the spec also restricts the attributes and methods that can be used on the Mock object. This is helpful for assuring that interface or shape of the object that is being Mocked is honored:

```python
>>> class Thing:
...     a = 1
...     b = "foo"
...
>>> mock_thing = Mock(spec=Thing)
>>> mock_thing.a
<Mock name='mock.a' id='1553003933552'>
>>> mock_thing.b
<Mock name='mock.b' id='1553003978816'>
>>> mock_thing.c
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "...\unittest\mock.py", line 630, in __getattr__
    raise AttributeError("Mock object has no attribute %r" % name)
AttributeError: Mock object has no attribute 'c'

True
```

Use `spec_set` for restrict the attributes that can be set to only those that are defined in the class:

```python
>>> class Thing:
...     a = 1
...     b = "foo"
...
>>> mock_thing = Mock(spec_set=Thing)
>>> mock_thing.a = 2
>>> mock_thing.b = 3.0
>>> mock_thing.c = 'bar'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "...\unittest\mock.py", line 737, in __setattr__
    raise AttributeError("Mock object has no attribute '%s'" % name)
AttributeError: Mock object has no attribute 'c'

```

## MagicMock

The MagicMock class extends Mock by implementing reasonable defaults for the "magic" methods:

* `__lt__`: `NotImplemented`
* `__gt__`: `NotImplemented`
* `__le__`: `NotImplemented`
* `__ge__`: `NotImplemented`
* `__int__`: `1`
* `__contains__`: `False`
* `__len__`: `0`
* `__iter__`: `iter([])`
* `__exit__`: `False`
* `__complex__`: `1j`
* `__float__`: `1.0`
* `__bool__`: `True`
* `__index__`: `1`
* `__hash__`: default hash for the mock
* `__str__`: default str for the mock
* `__sizeof__`: default sizeof for the mock

```python
>>> mock = MagicMock()
>>> int(mock)
1
>>> len(mock)
0
>>> list(mock)
[]
>>> object() in mock
False
```

## Patch

The `unittest.mock` module provides a `patch` function that can be used to lookup an object in a module and replace it with a Mock. The patch function is used most often as a context manager or decorator.

For the examples below assume you have a file called `my_module.py` with the following contents:

```python
import json

def a_function(a_str):
    return json.loads(a_str)
```

## Patch w/ Context Manager

```python
import unittest
from unittest import mock
from my_module import a_function


class TestStuff(unittest.TestCase):
    
    def test_a_function(self):
        with mock.patch('my_module.json') as mock_json:
            mock_json.loads.side_effect = ValueError
            
            with self.assertRaises(ValueError):
                a_function()
```

## Patch w/ Decorator

```python
import unittest
from unittest import mock
from my_module import a_function


class TestStuff(unittest.TestCase):
    
    @mock.patch('my_module.json')
    def test_a_function(self, mock_json):
        with self.assertRaises(ValueError):
            a_function()
```

# aquacal
A sample project that demonstrates mocking in Python.
# Python Mock and MagicMock

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

## Mock Return Values

You can control the return value of Mock objects






















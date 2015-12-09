# worm
Light weight distributed computing for ipython

###TODO:
1. Clean up Status object
* Add support for console
* Add support for non-interactive sessions

# Installation
```
git clone https://github.com/mtconley/worm.git
cd worm
python setup.py install
```

# Example
```python
>>> import worm
>>> data = worm.Collection(df)
>>> data.map(function).collect()
>>> data
[Record({'a': 9, 'c': 9, 'b': 1, 'e': 5, 'd': 4, 'index_record': 0}),
Record({'a': 81, 'c': 3, 'b': 0, 'e': 3, 'd': 5, 'index_record': 1}),
Record({'a': 0, 'c': 6, 'b': 27, 'e': 2, 'd': 5, 'index_record': 2}),
Record({'a': 64, 'c': 0, 'b': 8, 'e': 9, 'd': 7, 'index_record': 3}),
Record({'a': 0, 'c': 0, 'b': 125, 'e': 7, 'd': 2, 'index_record': 4}),
...]

Collection Object with
200000 Record Objects
```

```python
>>> import worm
>>> functions = [func1, func2, func3]
>>> data = worm.run(df, mappers=functions)
```
||a||b||c||d||e||index_record||
|0|81|0|2|4|6|0|
|1|16|512|3|7|8|1|
|2|0|125|4|6|3|2|
|3|16|729|0|9|4|3|
|4|81|216|0|5|8|4|
|5|64|64|2|1|2|5|

#How to use only bytes as internal units

# Introduction #

This article describes the way to move from mixed internal units to only bytes as internal units.

# To Do #

  * Create some functions to convert to bytes and from bytes
  * Create some unit tests

# Implementation #

```
def convert_bytes(self, size, unit, to_bytes=False):
	power = {'KB':1, 'MB':2, 'GB':3}
	if unit in power:
		return size*(1024**power[unit]) if to_bytes else size/(1024**power[unit])
			
def normalize(self, size):
	units = ['B','KB','MB','GB']
	for unit in units:
		if size < 1024:
			return (size, unit)
		else:
			size /= 1024
```
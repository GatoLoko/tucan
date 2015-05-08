# Tips for coding good docstrings. #

**Multi-line docstrings consist of:**
  * _Summary line_
  * _Blank line_
  * _Arguments_: not just the type, but in detail.
  * _Return values_: not just the type, but in detail.

**Example:**
```
def manage_packages(self, packages, packages_info):
	"""Creates the directory of download and the password for the package if needed.

	packages: list of 5-tuple (str::link, str::file_name, int::size, str::size_unit, str::plugin_type)
	packages_info: list of 3-tuple (str::path, str::name, str::password)
	"""
```

More info: http://www.python.org/dev/peps/pep-0257/
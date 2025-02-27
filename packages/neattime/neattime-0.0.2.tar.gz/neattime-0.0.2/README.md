# neattime

This package includes a simple function to create my preferred date-time format for log files.

Example:

```
from neattime import neattime

print(neattime())
```

output:

```
'2025-02-26_08.34.13.636609'
```

How I would actually use it:

```
from neattime import neattime

filepath = f'save_directory/log_{neattime()}'

# some code that saves my logfile

print(f"File saved to {filepath}")
```

output:

```
File saved to save_directory/log_2025-02-26_08.34.13.636609
```
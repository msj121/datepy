# datepy

[Visit Github](https://github.com/msj121/datepy).

datepy is a versatile Python library for parsing dates from various string formats into standardized RFC 3339 timestamps. It supports a wide range of date formats, including ISO 8601, RFC 822, long date formats, and more, with the ability to extend support through custom formats.

## Features

- **Broad Format Support**: Handles numerous standard and custom date formats out of the box.
- **Customizable**: Easily extendable to parse non-standard date formats.
- **Easy to Use**: Simple and intuitive API.

## Installation

To install datepy, simply use pip:

```
pip install datepy
```

## Usage

datepy is easy to use. Simply import the library and call the `parse` function with the date string and the format of the date string. The function will return a standardized RFC 3339 timestamp.

```python
from datepy import datepy

date_string = "2021-01-01 12:00:00"
rfc3339_date = datepy.convert_to_rfc3339(date_string)
print(rfc3339_date)
```

### Additional Formats

Please suggest a request and I can add the code/feature or format!



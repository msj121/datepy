from datetime import datetime, timezone
from dateutil import parser
import dateparser  # Import the dateparser library
import re

# Dictionary of standard and custom date formats.
DATE_FORMATS = {
    'standard': [
        "%Y-%m-%dT%H:%M:%SZ",  # ISO 8601 with UTC timezone
        "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601 with UTC offset
        "%d %b %Y %H:%M:%S %Z",  # RFC 822 with timezone
        "%Y-%m-%dT%H:%M:%S.%fZ",  # ISO 8601 with milliseconds and UTC
        # Add other standard formats here...
    ],
    'custom': {
        'long_date': "%B %d, %Y %I:%M %p",
        'short_date_2_digit': "%m/%d/%y %I:%M %p",
        'short_date_hyphens': "%d-%b-%y %I:%M %p",
        'mixed_date': "%d-%m-%Y %I:%M %p",
        'date_only': "%Y-%m-%d",
        'date_only_slashes': "%m/%d/%Y",
        'abbreviated_year': "%b %d, '%y",
        'long_month_name': "%d-%B-%Y",
        'uppercase_month_abbr': "%d/%b/%Y",
        'compact_format': "%Y%m%dT%H%M%SZ",
        'time_with_long_date': "%I:%M %p, %B %d, %Y",
        'time_with_short_date': "%I:%M %p, %m/%d/%y",
        'time_with_short_format': "%I:%M %p, %d-%b-%y",
        'ordinal_day': "%B %dst, %Y",
        'short_format_timezone': "%d-%b-%Y %I:%M %p %Z",
        'short_format_offset': "%d/%m/%y %I:%M %p %z",
        'dots_separators': "%d.%m.%y %I:%M %p",
        'non_latin': "%Y年%m月%d日 %H:%M:%S",  # For Japanese dates
        'arabic_numerals': "%d %B، %Y %I:%M %p",  # For Arabic dates
        'non_standard_separators': "%Y年%m月%d日 %I:%M %p",
    }
}


def remove_days_of_week(date_str):
    # Compiled regex pattern for efficiency
    days_pattern = re.compile(r'\b(?:Mon|Tues|Wed|Thur|Thurs|Fri|Sat|Sun|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[, ]?\b', re.IGNORECASE)
    
    # Remove the day of the week from the date string
    return days_pattern.sub("", date_str).strip()



    

def convert_to_rfc3339(date_str, debug=False):
    # Try parsing with standard formats.
    if date_str is None:
        return None
    
    new_date_str = remove_days_of_week(date_str)
    if(new_date_str != date_str):
        if(debug):
            print(f"Removed days of week: {date_str}")
        date_str = new_date_str

    try:
        return parser.parse(date_str).isoformat()
    except ValueError:
        pass

    # return None
    for fmt in DATE_FORMATS['standard']:
        try:
            return datetime.strptime(date_str, fmt).isoformat()
        except ValueError:
            continue

    # Try parsing with custom formats.
    for fmt in DATE_FORMATS['custom'].values():
        try:
            return datetime.strptime(date_str, fmt).isoformat()
        except ValueError:
            continue

    # Handle ambiguous year formats.
    if re.match(r'\d{2}-\d{2}-\d{2}', date_str):
        try:
            date_str = re.sub(r'[^\d]', '', date_str)
            return datetime.strptime(date_str, "%y%m%d").isoformat()
        except ValueError:
            pass
    
    try:
        parsed_date = dateparser.parse(date_str)
        if parsed_date:
            return parsed_date.isoformat()
    except ValueError:
        pass

    if(debug):
        return (f"Could not parse the date: {date_str}")
    return None

def main():
    # Example usage with a list of date strings.
    date_formats = [
        "Fri, 22 Mer 2019 10:00:00 +0900",     # RFC 822 with timezone
        "Thur, 2 Dec 2017 1:00:00 GMT",        # RFC 822 with timezone
        "Tues, 04 June 2013 15:00:00 +0900",    # RFC 822 with timezone
        "2024-01-01T12:00:00Z",                 # ISO 8601 with UTC timezone
        "2024-01-01T12:00:00+00:00",           # ISO 8601 with UTC offset
        "01 Jan 2024 12:00:00 GMT",            # RFC 822 with GMT timezone
        "01 Jan 2024 12:00:00 +0000",          # RFC 822 with UTC offset
        "2024-01-01T12:00:00.123456Z",         # ISO 8601 with milliseconds and UTC
        "January 1, 2024 12:00 PM",            # Long date format
        "01/01/24 12:00 PM",                   # Short date format with 2-digit year
        "01-Jan-24 12:00 PM",                  # Short date format with hyphens
        "01-01-2024 12:00 PM",                # Mixed format
        "2024-01-01",                          # Date only
        "01/01/2024",                          # Date only with slashes
        "Jan 1, '24",                          # Abbreviated year
        "01-January-2024",                    # Long month name
        "01/JAN/2024",                         # Uppercase month abbreviation
        "2024-01-01T12:00:00.123Z",            # ISO 8601 with milliseconds and UTC
        "01-Jan-24T12:00:00Z",                # Short format with UTC timezone
        "20240101T120000Z",                   # Compact format with UTC
        "24-01-01",                            # Ambiguous year
        "12:00 PM, January 1, 2024",           # Time with long date format
        "12:00 PM, 01/01/24",                 # Time with short date format
        "12:00 PM, 01-Jan-24",                # Time with short format
        "January 1st, 2024",                   # Ordinal day
        "01-Jan-2024 12:00 PM EST",           # Short format with timezone
        "01/01/24 12:00 PM -0500",            # Short format with offset
        "01-Jan-24 12:00 PM PDT",             # Short format with another timezone
        "Jan 1, '24 12:00 PM PDT",             # Abbreviated year with timezone
        "2024年1月1日 12:00:00",               # Non-Latin characters (e.g., Japanese)
        "١ يناير، ٢٠٢٤ ١٢:٠٠ م",              # Arabic numerals and characters
        "2024/01/01 12:00:00",                # Date with slashes
        "01.01.24 12:00 PM",                  # Dots as separators
        "01-01-24T12:00:00+00:00",            # ISO 8601 with UTC offset
        "01/01/24 12:00:00 GMT",              # Short date format with GMT timezone
        "2024年01月01日 12:00 PM",             # Non-standard separators and time
    ]
    converted_dates = [convert_to_rfc3339(date, debug=True) for date in date_formats]
    for date in converted_dates:
        try:
            date = parser.parse(date)
            if date.tzinfo is None or date.tzinfo.utcoffset(date) is None:
                    date = date.replace(tzinfo=timezone.utc)
            print(date)
        except ValueError:
            print(date)

if __name__ == "__main__":
    main()

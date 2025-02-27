
# TimeBaran Library

TimeBaran is a Python library that provides functionality for working with Persian (Jalali) dates, times, daily supplications, and upcoming events. It allows you to retrieve the current time in Persian format, fetch events for the current date, and more.

## Features

- **Get Current Persian Time**: Retrieve the current time in Persian (Jalali) format, including year, month, day, and time.
- **Daily Supplications**: Get a daily supplication based on the current date.
- **Upcoming Events**: Fetch upcoming events for the month in Persian, with descriptions.
  
## Installation

You can install the library via `pip` by using the following command:

```bash
pip install timebaran
```

## Requirements

- `pytz` for time zone support.
- `jdatetime` for working with Persian (Jalali) dates.
- `requests` for making HTTP requests.
- `BeautifulSoup` for web scraping and parsing event data.
- `tzlocal` for determining the local timezone.

## Usage

To use the `Date_time` class in your project, you can follow the example below:

```python
from timebaran import Date_time

# Initialize the Date_time object
dt = Date_time()

# Get the upcoming events
events = dt.get_events()
print(events)

# Get the current time, day, supplication, and events
time_data = dt.get_time()
print(time_data)
```

### `get_time()` Method

This method returns the current time and date in Persian (Jalali) format, along with:

- `time_now`: Current time in HH:MM:SS format.
- `time_h`: Hour of the current time.
- `time_m`: Minute of the current time.
- `time_s`: Second of the current time.
- `date_now`: Current date in Persian (Jalali) format (YYYY/MM/DD).
- `time_year`: Year part of the current date in Persian.
- `time_month`: Month part of the current date in Persian.
- `time_day`: Day part of the current date in Persian.
- `day_of_week`: Current day of the week in English short form (e.g., Mon, Tue).
- `zekr_today`: Daily supplication based on the current day.
- `events`: A dictionary of upcoming events with dates as keys and descriptions as values.

### `get_events()` Method

This method fetches upcoming events from a public website and returns them in a dictionary format.

Example:

```python
{
    '5 Esfand': 'روز بزرگداشت خواجه نصیرالدین طوسی',
    '7 Esfand': 'سالروز استقلال کانون وکلای دادگستری',
    # More events...
}
```

## License

This library is open-source and distributed under the MIT License.

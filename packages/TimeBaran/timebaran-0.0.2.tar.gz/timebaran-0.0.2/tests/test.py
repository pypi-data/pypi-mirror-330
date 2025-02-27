from TimeBaran import Date_time

# Initialize the Date_time object
dt = Date_time()

# Get the upcoming events
events = dt.get_events()
print(events)

# Get the current time, day, supplication, and events
time_data = dt.get_time()
print(time_data)

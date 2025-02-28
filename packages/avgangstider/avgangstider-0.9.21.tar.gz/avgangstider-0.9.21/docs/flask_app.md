# Web-app Documentation

## Finding a stop_id

- Look it up on the Stop-register: https://stoppested.entur.org/

## Arguments

- `stop_id`: The ID of the stop you want to get departures for.
- `platform`: A platform ID, can be repeated. If not specified, all platforms will be
  included.
- `line_id`: Specific line IDs, can be repeated. If not specified, all lines will be
  included.
- `max_rows`: The maximum number of departures to return. If not specified, all
  departures will be included.

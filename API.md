# API & Data Formats

## Scraped Data Example (CSV/JSON)

| timestamp           | event_name      | location        | crowd_estimate |
|---------------------|-----------------|-----------------|---------------|
| 2025-09-27 20:00:00 | Big Concert     | Rogers Place    | 1200          |

JSON:
```
{
  "timestamp": "2025-09-27T20:00:00",
  "event_name": "Big Concert",
  "location": "Rogers Place",
  "crowd_estimate": 1200
}
```

- All timestamps are UTC
- `crowd_estimate` is an integer

<!-- Yeah, we're gonna do the 12 hour clock please not the 24 hour clock 24 hour. Clock is nurses and like it's so rare nobody uses it at all but maybe like no I've never even seen a cab used 24 hour time yeah so let's just keep it and p.m. not 24 hour even though I agree like I get it at night time concerts are gonna run until 1 AM so it's like 81 I get that but it's just how it is around h. -->
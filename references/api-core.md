# SMS.ir API Core Reference

## Contents
- Base URL and authentication
- Request headers
- Common response envelope
- HTTP status codes
- Time values
- Practical client rules

## Base URL and authentication

Base URL:

```text
https://api.sms.ir/v1
```

For REST methods, send the private API key in the request header:

```http
X-API-KEY: <SMSIR_API_KEY>
```

Recommended additional headers for JSON calls:

```http
Accept: application/json
Content-Type: application/json
```

The official docs mention `Accept: application/json` or `application/xml`; this skill uses JSON by default because it is the common integration path and examples are JSON-oriented.

## Common response envelope

SMS.ir uses a common response structure:

```json
{
  "status": 1,
  "message": "موفق",
  "data": {}
}
```

Fields:

- `status`: SMS.ir application/status code.
- `message`: human-readable result message.
- `data`: endpoint-specific payload; may be object, array, scalar, or null.

A robust client must validate the HTTP status and the application `status` field.

## HTTP status codes

| HTTP | Meaning |
|---:|---|
| 200 | Request processed successfully at HTTP layer |
| 400 | Logical/request error |
| 401 | Authentication error |
| 429 | Too many requests |
| 500 | Unexpected server error |

Do not assume HTTP 200 means the business operation succeeded. Inspect the response envelope.

## Time values

SMS.ir documents time values as Unix Time in UTC.

When converting local application time to SMS.ir:

1. Parse the intended time in the application's explicit timezone.
2. Convert to UTC.
3. Send Unix seconds, not milliseconds.

When receiving timestamps, convert from UTC Unix seconds to the user's/site's timezone only for display.

## Practical client rules

- Keep `SMSIR_API_KEY` in environment/secrets storage.
- Keep `SMSIR_LINE_NUMBER` and template IDs configurable.
- Use TLS (`https://`) only.
- Set network connect/read timeouts.
- Log endpoint, HTTP code, SMS.ir status, message, and request correlation metadata; never log the API key.
- Redact mobile numbers in broad application logs if they are not necessary for operations/debugging.
- Preserve `messageId`, `messageIds`, and `packId` where returned.
- Treat transport failures after request transmission as potentially ambiguous for send operations; avoid blind retries that can duplicate messages.

## Official source

Snapshot reviewed 2026-08-15:

- https://sms.ir/rest-api/

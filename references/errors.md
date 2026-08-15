# SMS.ir Error and Delivery Codes

## Contents
- HTTP-level errors
- SMS.ir application status codes
- Delivery status codes
- Handling guidance

## HTTP-level errors

| HTTP | Meaning |
|---:|---|
| 200 | HTTP-level success |
| 400 | Logical/request error |
| 401 | Authentication error |
| 429 | Too many requests |
| 500 | Unexpected server error |

## SMS.ir application status codes

| Code | Meaning from official docs | Agent action |
|---:|---|---|
| 1 | Operation successful | Continue and parse `data` |
| 0 | System problem; contact support | Surface provider error; avoid blind send retry |
| 10 | Invalid web-service key | Check secret/config; never print key |
| 11 | Web-service key disabled | Ask user/admin to enable/replace key |
| 12 | Key restricted to configured IPs | Check source IP and API-key IP restrictions |
| 13 | User account inactive | Account action required |
| 14 | User account suspended | Account/support action required |
| 20 | Too many requests | Respect rate limit; bounded backoff where safe |
| 101 | Invalid sender line | Fetch `/line`; verify configured line |
| 102 | Insufficient credit | Add credit or reduce scope |
| 103 | Empty message text(s) | Validate non-empty message(s) |
| 104 | Invalid mobile number(s) | Validate destination values |
| 105 | More than 100 mobiles | Chunk into batches of <=100 |
| 106 | More than 100 texts | Chunk like-to-like requests |
| 107 | Mobile list empty | Validate required list |
| 108 | Text list empty | Validate required list |
| 109 | Invalid send time | Check UTC Unix seconds and scheduling window |
| 110 | Mobile/text counts differ | Ensure equal array lengths for like-to-like |
| 111 | No send found for ID | Verify message/pack identifier |
| 112 | No record found to delete | Scheduled pack may not exist/be cancellable |
| 113 | Template not found | Verify template ID/account/environment |
| 114 | Parameter value exceeds 25 characters | Shorten/validate Verify parameter value |
| 115 | Mobile number(s) are blacklisted | Respect service rules; use Verify only for legitimate approved service templates |
| 116 | Parameter name cannot be empty | Validate Verify parameter names |
| 117 | Sent text is not approved | Check message/template/provider rules |
| 118 | Message count exceeds allowed limit | Reduce/chunk scope |
| 119 | Plan upgrade required for personalized template | User/account plan action required |
| 123 | Sender line requires activation | Activate/configure sender line |

## Delivery status codes

| Code | Meaning |
|---:|---|
| 1 | Delivered to handset |
| 2 | Not delivered to handset |
| 3 | Processing at telecom |
| 4 | Not reached telecom |
| 5 | Reached telecom |
| 6 | Error |
| 7 | Blacklist |

Do not collapse all non-1 states into a permanent failure immediately. Some states are transitional, especially `3` (processing at telecom). If the product needs final delivery state, re-query later using an application-appropriate schedule.

## Retry guidance

- Transport timeout after request upload: ambiguous for send operations; do not blindly resend.
- HTTP 429 / code 20: retry with bounded backoff only when the operation's duplicate risk is controlled.
- 500 / code 0: surface and retry cautiously; for sends, use identifiers/reporting if available before repeating.
- Validation/account errors: do not retry unchanged input.

## Official source

Snapshot reviewed 2026-08-15:

- https://sms.ir/rest-api/

# SMS.ir Sending Reference

## Contents
- Bulk send
- Like-to-like send
- Cancel scheduled send
- Verify send
- Legacy URL send
- Selection guide

## Bulk send

**Endpoint**: `POST https://api.sms.ir/v1/send/bulk`

Use when one text should be sent to multiple recipients.

Documented constraints:

- Maximum destination mobiles per request: 100.
- `lineNumber`: required.
- `messageText`: required.
- `mobiles`: required array.
- `sendDateTime`: optional Unix UTC time; null/omitted means immediate send.
- Scheduled time: from one hour in the future up to 365 days in the future.

Request:

```json
{
  "lineNumber": 300000000000,
  "messageText": "Your message",
  "mobiles": ["09120000000", "09190000000"],
  "sendDateTime": null
}
```

Success data:

```json
{
  "packId": "2b99e63c-9bf8-4a21-9bfe-3f72dc1b46f1",
  "messageIds": [86522023, 86522024],
  "cost": 2.0
}
```

The official docs note that a `messageIds` element can be `0` for a blacklisted recipient and may be `null` for an invalid number or an overlong/invalid text condition. Preserve positional mapping to recipients.

## Like-to-like send

**Endpoint**: `POST https://api.sms.ir/v1/send/likeToLike`

Use when each recipient has its own message text.

Rules:

- Maximum 100 recipients/messages per request.
- `messageTexts.length` must equal `mobiles.length`.
- `lineNumber`: required.
- `messageTexts`: required array of strings.
- `mobiles`: required array of strings.
- `sendDateTime`: optional Unix UTC time.
- Scheduled time follows the same one-hour-to-365-days documented window.

Request:

```json
{
  "lineNumber": 300000000000,
  "messageTexts": ["Text A", "Text B"],
  "mobiles": ["09120000000", "09190000000"],
  "sendDateTime": null
}
```

Success data has the same `packId`, `messageIds`, and `cost` shape as bulk sending.

## Cancel scheduled send

**Endpoint**: `DELETE https://api.sms.ir/v1/send/scheduled/{packId}`

Use the pack ID returned by bulk or like-to-like sending.

Documented rule: cancellation is allowed until a maximum of 3 minutes before the scheduled send time.

Example success data:

```json
{
  "returnedCreditCount": 10.0,
  "smsCount": 5
}
```

## Verify send

**Endpoint**: `POST https://api.sms.ir/v1/send/verify`

Use for OTP/verification codes and other high-priority templated service messages. A template must exist in the SMS.ir panel.

Request fields:

| Field | Type | Required | Meaning |
|---|---|---|---|
| `mobile` | string | yes | Destination mobile |
| `templateId` | integer | yes | Template ID from panel |
| `parameters` | array | yes | Template replacement values |

Parameter item:

```json
{
  "name": "Code",
  "value": "12345"
}
```

Use parameter names without the `#` markers that appear in the template text.

Request example:

```json
{
  "mobile": "09190000000",
  "templateId": 123456,
  "parameters": [
    {"name": "Code", "value": "12345"}
  ]
}
```

Success data:

```json
{
  "messageId": 89545112,
  "cost": 1.0
}
```

Error code `114` documents a maximum parameter value length of 25 characters. Validate known dynamic values before sending when practical.

The provider's product page describes Verify as using service lines, high priority, and able to reach recipients who have blocked advertising SMS. This should not be interpreted as permission to use Verify for advertising; use it for the approved service/template purpose.

## Legacy URL send

**Endpoint**: `GET` or `POST https://api.sms.ir/v1/send`

Documented query/body parameters:

- `username`
- `password` (private key/API key)
- `line`
- `mobile`
- `text`

Example form:

```text
https://api.sms.ir/v1/send?username=...&password=...&line=...&mobile=...&text=...
```

Security recommendation: prefer the header-authenticated REST endpoints whenever possible. Query-string credentials can leak into access logs, reverse proxies, analytics, browser history, error reporting, and monitoring systems.

## Selection guide

- Login/register OTP -> Verify.
- Order/payment/status template -> Verify if implemented as an approved template.
- Same notification/marketing text to many recipients -> Bulk, subject to sender-line/service rules.
- Personalized text per recipient without a template -> Like-to-like.
- Existing legacy system that cannot set headers -> URL send only if migration is not currently possible.

## Official source

Snapshot reviewed 2026-08-15:

- https://sms.ir/rest-api/
- https://sms.ir/web-service/

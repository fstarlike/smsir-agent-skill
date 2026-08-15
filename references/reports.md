# SMS.ir Reports and Receive Reference

## Contents
- One-message delivery report
- Today's send packs
- Send pack details
- Today's sends
- Archived sends
- Latest unread inbound messages
- Today's inbound messages
- Archived inbound messages

## One-message delivery report

**Endpoint**: `GET /send/{messageId}`

Returns information such as:

- `messageId`
- `mobile`
- `messageText`
- `sendDateTime` (Unix UTC)
- `lineNumber`
- `cost`
- `deliveryState`
- `deliveryDateTime` (nullable Unix UTC)

Use delivery-state mapping from `errors.md`.

## Today's send packs

**Endpoint**: `GET /send/pack`

Optional query parameters:

- `pageSize` — default 100.
- `pageNumber` — default 1.

Items include:

- `packId`
- `recipientCount`
- `creationDateTime`

## Send pack details

**Endpoint**: `GET /send/pack/{packId}`

Returns an array of messages in a send pack with delivery information. Use when a bulk/like-to-like call returns a `packId` and you need per-recipient outcome.

## Today's sends

**Endpoint**: `GET /send/live`

Optional query parameters:

- `pageSize` — max 100, default 100.
- `pageNumber` — default 1.

Returns the day's sent-message records.

## Archived sends

**Endpoint**: `GET /send/archive`

Use for historical sends up to the end of the previous day.

Optional query parameters:

- `fromDate` — Unix UTC.
- `toDate` — Unix UTC.
- `pageSize` — max 100, default 100.
- `pageNumber` — default 1.

## Latest unread inbound messages — destructive/read-once behavior

**Endpoint**: `GET /receive/latest`

Optional query parameter:

- `count` — max/default 100.

Important: the official docs state that each inbound message can be obtained only once through this method. After retrieval it is marked read and is not returned again by this endpoint.

Use this endpoint only when the application intentionally consumes a queue-like stream of unread inbound SMS. If processing can fail, persist the response before executing downstream side effects so a crash does not lose the message.

Returned fields include:

- `receiveReturnId`
- `messageText`
- `number` (recipient line)
- `mobile` (sender)
- `receivedDateTime`

## Today's inbound messages

**Endpoint**: `GET /receive/live`

Optional query parameters:

- `pageSize` — max 100, default 100.
- `pageNumber` — default 1.
- `sortByNewest` — boolean; docs describe default as false/ascending.

This report includes read and unread messages for the current day. The docs note that during the early hours of a day, the previous day's inbound messages may also be available through this method.

Use this endpoint for repeatable listing rather than queue consumption.

## Archived inbound messages

**Endpoint**: `GET /receive/archive`

Historical inbound messages up to the end of the previous day.

Optional query parameters:

- `fromDate` — Unix UTC.
- `toDate` — Unix UTC.
- `pageSize` — max 100, default 100.
- `pageNumber` — default 1.

Records include `receiveReturnId`, `messageText`, `number`, `mobile`, and `receivedDateTime`.

## Pagination pattern

When a report is paginated:

1. Start at `pageNumber=1`.
2. Request a page size no larger than documented max 100.
3. Continue until the returned array length is less than the requested page size, or until the application's own limit is reached.
4. Add a hard page/record cap for background jobs so a bug cannot create an unbounded loop.

## Official source

Snapshot reviewed 2026-08-15:

- https://sms.ir/rest-api/

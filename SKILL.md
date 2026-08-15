---
name: smsir-agent-skill
description: Integrates applications with the SMS.ir REST API for transactional and bulk SMS, Verify/OTP templates, scheduled sends, delivery and inbound-message reports, account credit, sender lines, Sandbox testing, error handling, and API security. Use when implementing, debugging, reviewing, or documenting SMS.ir integrations in PHP/WordPress, JavaScript/TypeScript, Python, Java, C#, or other HTTP-capable environments.
license: MIT
compatibility: Requires HTTPS/network access to api.sms.ir for live calls. Designed for Agent Skills-compatible coding agents such as Cursor and Claude Code.
metadata:
  author: fstarlike
  version: "1.0.0"
  provider: "SMS.ir"
  docs-snapshot: "2026-08-15"
---

# SMS.ir REST API Skill

Use this skill to implement and troubleshoot SMS.ir integrations reliably. Prefer the current REST API at `https://api.sms.ir/v1` and keep credentials out of source code.

## Non-negotiable rules

1. Never hardcode a real SMS.ir API key in source, examples, logs, tests, commits, screenshots, or generated documentation.
2. Prefer `X-API-KEY` header authentication. Read the key from an environment variable or the project's existing secret/config system.
3. Treat sending as a side effect. Do not send a real SMS during tests unless the user explicitly asks for a live send and provides/has configured valid credentials and recipients.
4. Prefer Sandbox for integration tests. Read [references/account-and-sandbox.md](references/account-and-sandbox.md) before designing test flows.
5. For OTP, login codes, order-status notifications, invoices, or other high-priority templated messages, prefer `POST /send/verify` rather than bulk sending.
6. For one text to many recipients, use `POST /send/bulk`. For one text per recipient, use `POST /send/likeToLike`.
7. Never poll `GET /receive/latest` casually: it is consumptive/read-once for each inbound message. Use live/archive reports when repeated access is required.
8. Use UTC Unix timestamps when the API expects time values. Convert user/site-local time explicitly; do not rely on server-local timezone.
9. Handle both HTTP status and the SMS.ir response body's `status`, `message`, and `data`. Do not treat HTTP 200 alone as sufficient application-level validation.
10. If an endpoint detail conflicts across official SMS.ir examples, follow the dedicated endpoint contract and document the ambiguity. Do not invent undocumented parameters.

## Choose the operation

| Need | Endpoint | Method | Read |
|---|---|---|---|
| Send one message to up to 100 mobiles | `/send/bulk` | POST | [sending.md](references/sending.md) |
| Send different texts to matching mobiles | `/send/likeToLike` | POST | [sending.md](references/sending.md) |
| OTP / Verify / templated service message | `/send/verify` | POST | [sending.md](references/sending.md) |
| Cancel a scheduled pack | `/send/scheduled/{packId}` | DELETE | [sending.md](references/sending.md) |
| Legacy URL-based send | `/send` | GET or POST | [sending.md](references/sending.md) |
| Query one sent message | `/send/{messageId}` | GET | [reports.md](references/reports.md) |
| Today's send packs | `/send/pack` | GET | [reports.md](references/reports.md) |
| Messages inside a pack | `/send/pack/{packId}` | GET | [reports.md](references/reports.md) |
| Today's sends | `/send/live` | GET | [reports.md](references/reports.md) |
| Archived sends | `/send/archive` | GET | [reports.md](references/reports.md) |
| Consume latest unread inbound SMS | `/receive/latest` | GET | [reports.md](references/reports.md) |
| Today's inbound SMS | `/receive/live` | GET | [reports.md](references/reports.md) |
| Archived inbound SMS | `/receive/archive` | GET | [reports.md](references/reports.md) |
| Current credit | `/credit` | GET | [account-and-sandbox.md](references/account-and-sandbox.md) |
| Available sender lines | `/line` | GET | [account-and-sandbox.md](references/account-and-sandbox.md) |

## Default implementation workflow

1. Inspect the existing project language/framework and its current HTTP/secrets conventions.
2. Read [references/api-core.md](references/api-core.md) for authentication, response shape, HTTP behavior, and time handling.
3. Read only the operation-specific reference file needed for the task.
4. Reuse the project's HTTP client; do not add a new dependency when the standard library/framework already has a suitable client.
5. Put the API key behind a secret/config abstraction such as `SMSIR_API_KEY`. Put sender line/template IDs in config, not scattered literals.
6. Add an explicit timeout and surface transport errors separately from SMS.ir application errors.
7. Parse the common response envelope. On failure, map known status codes using [references/errors.md](references/errors.md).
8. For any real send, return or persist `messageId`/`messageIds` and `packId` where available so delivery can be queried later.
9. Add tests that mock HTTP by default. Use Sandbox for end-to-end tests when network access and a Sandbox key are available.
10. Before finishing, verify that no secret was introduced and that mobile/message arrays obey documented limits.

## Coding patterns

Read [references/examples.md](references/examples.md) for safe examples in cURL, TypeScript/JavaScript, PHP/WordPress, and Python.

When adding a reusable client, prefer an interface shaped around domain operations rather than raw URLs, for example:

- `sendVerify(mobile, templateId, parameters)`
- `sendBulk(lineNumber, messageText, mobiles, sendDateTime?)`
- `sendLikeToLike(lineNumber, messageTexts, mobiles, sendDateTime?)`
- `cancelScheduled(packId)`
- `getMessage(messageId)`
- `getCredit()`
- `getLines()`

Return a normalized project-level result while preserving the original SMS.ir response for diagnostics when appropriate.

## Error handling

Read [references/errors.md](references/errors.md) whenever a request fails or when implementing a reusable client. Important categories include invalid/disabled API key, IP restriction, suspended account, rate limiting, invalid line, insufficient credit, invalid mobiles, invalid scheduling, missing template, blacklisted numbers, and inactive sender line.

For HTTP `429`, implement bounded retry with backoff only when retrying is safe. Do not automatically retry a non-idempotent send if the client cannot determine whether the first request was accepted; duplicate SMS is worse than surfacing an ambiguous result.

## Security and infrastructure

Read [references/security.md](references/security.md) before implementing firewall allowlists or production secret handling. SMS.ir publishes primary/failover service IPs, but infrastructure values can change; verify the current official documentation before applying firewall rules.

The legacy `/send` endpoint places username/password-like credentials in URL parameters. Support it only when required for compatibility. Prefer header-authenticated REST methods because query strings can be exposed through logs, proxies, history, and monitoring systems.

## Documentation freshness

This skill is based on SMS.ir's official REST documentation reviewed on 2026-08-15. API behavior, IP addresses, limits, and product rules can change. If the task is production-critical and internet access is available, verify time-sensitive details against:

- `https://sms.ir/rest-api/`
- `https://sms.ir/web-service/`

Do not silently overwrite a documented project-specific integration contract just because this snapshot differs; explain the mismatch first.

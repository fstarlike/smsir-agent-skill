# SMS.ir Security and Production Operations

## Contents
- Secret handling
- IP restrictions and firewall allowlisting
- Published service IPs
- Logging and privacy
- Safe production checks

## Secret handling

Use an environment variable or the application's existing secret store:

```text
SMSIR_API_KEY=...
```

Never commit `.env` files containing real credentials. Do not echo the key in error messages. If an API response indicates an authentication problem, report the status code without revealing the key value.

If an API key has been committed accidentally, removing it from the latest file is not enough: rotate/revoke the key and clean repository history as appropriate.

## IP restrictions and firewall allowlisting

SMS.ir supports API-key IP restrictions and publishes service infrastructure IPs for firewall whitelisting scenarios.

As of the official documentation snapshot reviewed **2026-08-15**, the published web-service IPs are:

- Primary: `185.211.56.44`
- Failover/backup: `78.158.166.99`

These are time-sensitive infrastructure values. Before changing a production firewall, verify the current values at `https://sms.ir/rest-api/` because provider infrastructure can change.

If both are required by the official docs, allow both; allowing only the primary can break traffic during failover.

## Logging and privacy

Recommended logging fields:

- operation name / endpoint path
- HTTP status
- SMS.ir `status` and `message`
- `packId` / `messageId` when returned
- application correlation/request ID
- duration

Avoid logging:

- API keys
- full message body when it can contain OTP/PII
- full mobile numbers unless operationally necessary

For OTP flows, never log the OTP value at normal production log levels.

## Safe production checks

Before a live deployment:

1. Confirm API key comes from secret storage.
2. Confirm environment uses the correct key type (Sandbox vs production).
3. Confirm configured line exists in `/line` when using line-based sends.
4. Confirm template ID exists in the intended account/environment for Verify.
5. Confirm request timeout and error handling.
6. Confirm duplicate-send behavior for retries/timeouts.
7. Confirm logs do not expose secrets or OTP values.
8. Confirm scheduled timestamps are UTC Unix seconds.
9. Confirm batch chunking stays at or below 100 destinations/messages.

## Official source

Snapshot reviewed 2026-08-15:

- https://sms.ir/rest-api/

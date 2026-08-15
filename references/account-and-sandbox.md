# SMS.ir Account, Lines, and Sandbox

## Contents
- Current credit
- Sender lines
- Sandbox behavior
- Sandbox Verify template
- Sandbox documentation inconsistency
- Testing strategy

## Current credit

**Endpoint**: `GET https://api.sms.ir/v1/credit`

Success `data` is the current credit as a decimal value.

Use this for dashboards/preflight checks, but do not rely on a separate credit check as a guarantee that a subsequent send will succeed; state can change between calls.

## Sender lines

**Endpoint**: `GET https://api.sms.ir/v1/line`

Success `data` is an array of sender line numbers available for sending.

When building an integration UI, prefer choosing from this endpoint rather than accepting an arbitrary line number when feasible.

## Sandbox behavior

SMS.ir documents a Sandbox mode that uses a Sandbox-specific API key while keeping production URLs, inputs, outputs, and validation/error behavior similar to production.

Key properties documented by SMS.ir:

- No real SMS is sent.
- No real credit is deducted.
- Returned data is simulated.
- Sandbox activity is not stored as reports in the SMS.ir panel.
- Create a Sandbox key in the SMS.ir developer/API key area.

## Sandbox Verify template

The docs publish a default Sandbox Verify template:

- Template ID: `123456`
- Template text: `کد تایید شما: #CODE#`

Request parameter should use the name without hash markers, for example `Code`/`CODE` according to the template key expected by the environment.

## Sandbox documentation inconsistency

The Sandbox section of the official page shows a Verify example labeled `Request Method: GET`, while the dedicated Verify endpoint contract and the provider's code examples use `POST /v1/send/verify`. The same Sandbox section also states that URLs/inputs/outputs are the same as production.

For implementations, use **POST** for `/send/verify` in Sandbox unless SMS.ir support or a newer official contract explicitly says otherwise. Treat the GET label as a documentation inconsistency, not a separate API contract.

## Testing strategy

Recommended order:

1. Unit tests with mocked HTTP — no network or SMS.ir credentials.
2. Sandbox integration test — explicit Sandbox key, no real SMS.
3. Production smoke test — only when explicitly requested, using a designated test mobile/template and a tiny scope.

Do not make test suites call production by default.

## Official source

Snapshot reviewed 2026-08-15:

- https://sms.ir/rest-api/

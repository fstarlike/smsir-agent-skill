# SMS.ir Integration Examples

## Contents
- cURL Verify
- TypeScript reusable client
- PHP / WordPress Verify
- Python Verify
- Bulk request body
- Report request

All examples use placeholders. Never paste a real API key into source code.

## cURL Verify

```bash
curl --request POST 'https://api.sms.ir/v1/send/verify' \
  --header "X-API-KEY: ${SMSIR_API_KEY}" \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json' \
  --data '{
    "mobile": "09120000000",
    "templateId": 123456,
    "parameters": [
      {"name": "Code", "value": "12345"}
    ]
  }'
```

## TypeScript reusable client

```ts
type SmsIrEnvelope<T> = {
  status: number;
  message: string;
  data: T;
};

type VerifyResult = {
  messageId: number;
  cost: number;
};

export async function smsIrRequest<T>(
  path: string,
  init: RequestInit = {},
): Promise<SmsIrEnvelope<T>> {
  const apiKey = process.env.SMSIR_API_KEY;
  if (!apiKey) throw new Error("SMSIR_API_KEY is not configured");

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15_000);

  try {
    const response = await fetch(`https://api.sms.ir/v1${path}`, {
      ...init,
      signal: controller.signal,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": apiKey,
        ...(init.headers ?? {}),
      },
    });

    const body = (await response.json()) as SmsIrEnvelope<T>;
    if (!response.ok || body.status !== 1) {
      throw new Error(
        `SMS.ir request failed: HTTP ${response.status}, status ${body.status}, ${body.message}`,
      );
    }
    return body;
  } finally {
    clearTimeout(timeout);
  }
}

export async function sendVerify(
  mobile: string,
  templateId: number,
  parameters: Array<{ name: string; value: string }>,
) {
  return smsIrRequest<VerifyResult>("/send/verify", {
    method: "POST",
    body: JSON.stringify({ mobile, templateId, parameters }),
  });
}
```

For production-grade send retry logic, do not blindly retry an aborted/ambiguous POST; first consider duplicate-send risk.

## PHP / WordPress Verify

```php
<?php
function imagineit_smsir_verify($mobile, $template_id, array $parameters) {
    $api_key = getenv('SMSIR_API_KEY');
    if (!$api_key) {
        return new WP_Error('smsir_config', 'SMSIR_API_KEY is not configured.');
    }

    $response = wp_remote_post('https://api.sms.ir/v1/send/verify', [
        'timeout' => 15,
        'headers' => [
            'Accept'       => 'application/json',
            'Content-Type' => 'application/json',
            'X-API-KEY'    => $api_key,
        ],
        'body' => wp_json_encode([
            'mobile'     => (string) $mobile,
            'templateId' => (int) $template_id,
            'parameters' => $parameters,
        ]),
    ]);

    if (is_wp_error($response)) {
        return $response;
    }

    $http_code = wp_remote_retrieve_response_code($response);
    $body = json_decode(wp_remote_retrieve_body($response), true);

    if ($http_code < 200 || $http_code >= 300 || !is_array($body) || (int)($body['status'] ?? 0) !== 1) {
        return new WP_Error(
            'smsir_api',
            isset($body['message']) ? (string) $body['message'] : 'SMS.ir request failed.',
            [
                'http_status' => $http_code,
                'smsir_status' => $body['status'] ?? null,
            ]
        );
    }

    return $body['data'];
}
```

In WordPress projects that already use constants/options/secret managers, adapt configuration to the existing project pattern rather than introducing `getenv()` inconsistently.

## Python Verify

Standard-library example:

```python
import json
import os
import urllib.request


def send_verify(mobile: str, template_id: int, parameters: list[dict[str, str]]):
    api_key = os.environ.get("SMSIR_API_KEY")
    if not api_key:
        raise RuntimeError("SMSIR_API_KEY is not configured")

    payload = json.dumps({
        "mobile": mobile,
        "templateId": template_id,
        "parameters": parameters,
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://api.sms.ir/v1/send/verify",
        data=payload,
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-KEY": api_key,
        },
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        body = json.load(response)

    if body.get("status") != 1:
        raise RuntimeError(
            f"SMS.ir error {body.get('status')}: {body.get('message')}"
        )

    return body.get("data")
```

## Bulk request body

```json
{
  "lineNumber": 300000000000,
  "messageText": "Your message",
  "mobiles": ["09120000000", "09190000000"],
  "sendDateTime": null
}
```

Chunk recipient lists into at most 100 mobiles per request. Store the returned `packId` and positional `messageIds`.

## Report request

```bash
curl --request GET 'https://api.sms.ir/v1/send/live?pageSize=100&pageNumber=1' \
  --header "X-API-KEY: ${SMSIR_API_KEY}" \
  --header 'Accept: application/json'
```

## Official source

API contracts/examples were derived from the official SMS.ir documentation snapshot reviewed 2026-08-15:

- https://sms.ir/rest-api/
- https://sms.ir/web-service/

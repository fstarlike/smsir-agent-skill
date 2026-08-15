# SMS.ir Agent Skill

یک **Agent Skill کامل برای وب‌سرویس SMS.ir** که به Agentهای کدنویسی مثل Cursor و Claude Code دانش لازم برای پیاده‌سازی، دیباگ و بررسی اتصال به SMS.ir را می‌دهد.

این پروژه بر اساس مستندات رسمی REST API سامانه SMS.ir تهیه شده و ساختارش با استاندارد باز **Agent Skills** سازگار است. آخرین بازبینی مستندات برای نسخه فعلی: **2026-08-15**.

> این ریپازیتوری مستقل است و وابستگی رسمی/سازمانی به SMS.ir ندارد. قراردادهای API از مستندات عمومی رسمی SMS.ir استخراج شده‌اند.

## چه چیزهایی پوشش داده شده؟

- احراز هویت با `X-API-KEY`
- ساختار استاندارد Response و HTTP statusها
- ارسال گروهی `bulk`
- ارسال نظیر به نظیر `likeToLike`
- ارسال OTP / Verify و پارامترهای قالب
- ارسال زمان‌بندی‌شده و لغو ارسال
- متد قدیمی ارسال از طریق URL
- گزارش وضعیت یک پیامک
- گزارش Packها و پیام‌های داخل Pack
- گزارش ارسال‌های روز و آرشیو
- دریافت آخرین پیامک‌های ورودی
- گزارش دریافت‌های روز و آرشیو
- اعتبار حساب
- لیست خطوط ارسال
- Sandbox و قالب تست Verify
- تمام کدهای خطای مستندشده
- Delivery Statusها
- نکات امنیتی و IP Whitelisting
- نمونه کد cURL، TypeScript/JavaScript، PHP/WordPress و Python
- قواعد امن برای نگهداری API Key، retry و جلوگیری از ارسال تکراری

## ساختار Skill

```text
smsir-agent-skill/
├── SKILL.md
├── README.md
├── LICENSE
├── references/
│   ├── api-core.md
│   ├── sending.md
│   ├── reports.md
│   ├── account-and-sandbox.md
│   ├── errors.md
│   ├── security.md
│   └── examples.md
└── scripts/
    └── validate_skill.py
```

`SKILL.md` عمداً کوتاه‌تر از مستند کامل نگه داشته شده و Agent بر اساس نیاز فقط فایل مرجع مربوط را می‌خواند؛ این همان مدل **progressive disclosure** در استاندارد Agent Skills است.

## نصب در Cursor

> آدرس رسمی این Skill: `https://github.com/fstarlike/smsir-agent-skill`

### روش ۱ — نصب مستقیم از GitHub داخل رابط Cursor

طبق مستندات فعلی Cursor:

1. پنل **Customize** را باز کنید.
2. به **Rules** بروید و **Add Rule** را بزنید.
3. گزینه **Remote Rule (Github)** را انتخاب کنید.
4. آدرس ریپازیتوری این Skill را وارد کنید.

Cursor ساختار Agent Skills را می‌شناسد و `SKILL.md` را برای کشف Skill استفاده می‌کند.

### روش ۲ — نصب برای یک پروژه

داخل ریشه پروژه:

```bash
REPO_URL=https://github.com/fstarlike/smsir-agent-skill.git
mkdir -p .cursor/skills
git clone "$REPO_URL" .cursor/skills/smsir-agent-skill
```

ساختار نهایی:

```text
YOUR_PROJECT/
└── .cursor/
    └── skills/
        └── smsir-agent-skill/
            ├── SKILL.md
            └── references/
```

یک Chat/Agent جدید باز کنید. Cursor می‌تواند Skill را با توجه به `description` به‌صورت خودکار انتخاب کند و در نسخه‌های پشتیبانی‌کننده از منوی `/` نیز قابل فراخوانی است.

### روش ۳ — نصب سراسری Cursor

```bash
REPO_URL=https://github.com/fstarlike/smsir-agent-skill.git
mkdir -p ~/.cursor/skills
git clone "$REPO_URL" ~/.cursor/skills/smsir-agent-skill
```

Cursor در حال حاضر این مسیرها را برای Skillها می‌شناسد: `.cursor/skills/` و `.agents/skills/` در سطح پروژه، و `~/.cursor/skills/` و `~/.agents/skills/` در سطح کاربر. برای این README مسیر native خود Cursor یعنی `.cursor/skills/` انتخاب شده است.

## نصب در Claude Code

### Skill سطح پروژه

در ریشه پروژه:

```bash
REPO_URL=https://github.com/fstarlike/smsir-agent-skill.git
mkdir -p .claude/skills
git clone "$REPO_URL" .claude/skills/smsir-agent-skill
```

نتیجه باید چنین باشد:

```text
YOUR_PROJECT/
└── .claude/
    └── skills/
        └── smsir-agent-skill/
            ├── SKILL.md
            └── references/
```

### Skill شخصی/سراسری Claude Code

```bash
REPO_URL=https://github.com/fstarlike/smsir-agent-skill.git
mkdir -p ~/.claude/skills
git clone "$REPO_URL" ~/.claude/skills/smsir-agent-skill
```

Claude Code، Skillهای پروژه را از `.claude/skills/` و Skillهای شخصی را از `~/.claude/skills/` می‌خواند.

### استفاده در Claude.ai

اگر از قابلیت Custom Skills در Claude.ai استفاده می‌کنید، پوشه `smsir-agent-skill` را به‌صورت ZIP بسته‌بندی کنید و از بخش **Settings → Features** آن را به‌عنوان Skill آپلود کنید. در پلن/محیطی که Custom Skills و code execution برای آن فعال باشد، Claude می‌تواند فایل‌های مرجع این Skill را برحسب نیاز بارگذاری کند.

### Claude API

Custom Skillها در Claude API نیز قابل آپلود هستند، اما runtime مربوط به Skill در Claude API طبق مستندات فعلی **دسترسی شبکه مستقیم ندارد**. بنابراین این Skill در آن محیط برای فهم قرارداد SMS.ir، تولید/بررسی کد و طراحی integration مفید است، ولی برای فراخوانی زنده `api.sms.ir` باید درخواست HTTP از اپلیکیشن/ابزار خارجی دارای network access انجام شود. Claude Code این محدودیت را ندارد و از دسترسی شبکه سیستم کاربر استفاده می‌کند.

## اگر می‌خواهید خود Agent این Skill را نصب کند

بعد از انتشار repo می‌توانید به خود Agent هم دستور نصب بدهید. نمونه برای Cursor:

```text
این Agent Skill را از https://github.com/fstarlike/smsir-agent-skill.git داخل
.cursor/skills/smsir-agent-skill نصب کن. بعد SKILL.md را بخوان و از آن
برای تمام کارهای مربوط به SMS.ir این پروژه استفاده کن. هیچ API Key واقعی را
داخل سورس یا لاگ قرار نده.
```

نمونه برای Claude Code:

```text
این Agent Skill را از https://github.com/fstarlike/smsir-agent-skill.git داخل
.claude/skills/smsir-agent-skill نصب کن. سپس SKILL.md را به‌عنوان راهنمای
SMS.ir این پروژه استفاده کن و فقط reference موردنیاز هر کار را بخوان.
```

این Skill خودش یک proxy یا credential provider نیست. برای اجرای واقعی درخواست‌های SMS.ir، Agent یا برنامه باید دسترسی شبکه داشته باشد و API Key باید از secret/config امن پروژه تأمین شود.

## نصب عمومی برای Agentهای سازگار با Agent Skills

قاعده کلی استاندارد:

```text
<skills-directory>/smsir-agent-skill/SKILL.md
```

نام پوشه باید با مقدار `name` در frontmatter هماهنگ باشد.

می‌توانید فقط repo را clone کنید و مسیر آن را به سیستم Skill Agent معرفی کنید.

## چطور به Agent بگوییم از Skill استفاده کند؟

بعد از نصب، معمولاً لازم نیست کل مستندات SMS.ir را داخل Prompt کپی کنید. نمونه درخواست‌ها:

```text
SMS.ir رو به سرویس لاگین این پروژه وصل کن. برای OTP از Verify استفاده کن و API Key رو داخل کد هاردکد نکن.
```

```text
این خطای SMS.ir با status 113 رو پیدا کن و درستش کن.
```

```text
ارسال گروهی SMS.ir رو طوری پیاده‌سازی کن که لیست‌های بیشتر از 100 شماره رو chunk کنه و packIdها رو ذخیره کنه.
```

```text
برای وردپرس یک سرویس SMS.ir بساز که با wp_remote_request کار کنه و خطاهای API رو به WP_Error تبدیل کنه.
```

```text
گزارش delivery پیامک‌های این packId رو بگیر و وضعیت‌ها رو به مدل داخلی پروژه map کن.
```

## تنظیم API Key در پروژه

پیشنهاد عمومی:

```env
SMSIR_API_KEY=your-secret-key
SMSIR_LINE_NUMBER=300000000000
SMSIR_VERIFY_TEMPLATE_ID=123456
```

فایل env واقعی را commit نکنید.

Agent طبق Skill موظف است API Key را در source code، test fixture عمومی، log یا commit قرار ندهد.

## انتخاب متد مناسب

| سناریو | متد پیشنهادی |
|---|---|
| کد ورود، ثبت‌نام، OTP | Verify |
| اطلاع‌رسانی قالب‌دار با اولویت بالا | Verify |
| یک متن برای چند شماره | Bulk |
| متن متفاوت برای هر شماره | Like-to-Like |
| دریافت وضعیت یک پیام | Message Report |
| دریافت پیام‌های ورودی جدید به شکل queue | Receive Latest |
| مشاهده تکرارشونده پیام‌های دریافتی | Receive Live / Archive |

`receive/latest` را با دقت استفاده کنید: طبق مستندات SMS.ir هر پیام از این endpoint فقط یک بار قابل دریافت است و بعد خوانده‌شده محسوب می‌شود.

## Sandbox

SMS.ir یک API Key از نوع Sandbox ارائه می‌کند که با همان URLها و ساختار API کار می‌کند، ولی پیام واقعی ارسال نمی‌شود و اعتبار واقعی کم نمی‌شود.

قالب Verify پیش‌فرض مستندشده در Sandbox:

```text
Template ID: 123456
کد تایید شما: #CODE#
```

در صفحه رسمی Sandbox یک ناسازگاری مستندی وجود دارد: مثال Verify در بخشی `GET` نوشته شده، در حالی که قرارداد اصلی Verify و نمونه‌های رسمی `POST /v1/send/verify` هستند و خود بخش Sandbox می‌گوید ساختار مشابه Production است. در این Skill، `POST` مبنا قرار گرفته است.

## محدودیت‌های مهمی که Agent باید رعایت کند

- Bulk: حداکثر 100 شماره در هر درخواست.
- Like-to-Like: حداکثر 100 شماره/متن و تعداد دو آرایه باید برابر باشد.
- زمان‌بندی: طبق مستندات از حداقل یک ساعت آینده تا حداکثر 365 روز آینده.
- لغو ارسال زمان‌بندی‌شده: حداکثر تا 3 دقیقه مانده به ارسال.
- زمان‌ها: Unix Time بر پایه UTC.
- مقدار پارامتر Verify: خطای رسمی 114 برای مقدار بیش از 25 کاراکتر تعریف شده است.
- API Key: در Header با `X-API-KEY`.

## اعتبارسنجی Skill

این repo یک validator سبک و بدون dependency دارد:

```bash
python scripts/validate_skill.py .
```

در صورت نصب ابزار رسمی `skills-ref` نیز می‌توانید طبق استاندارد Agent Skills از validator آن استفاده کنید.

## منابع رسمی

- SMS.ir Web Service: https://sms.ir/web-service/
- SMS.ir REST API: https://sms.ir/rest-api/
- Agent Skills Specification: https://agentskills.io/specification
- Cursor Agent Skills: https://cursor.com/docs/skills
- Claude Agent Skills docs: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

## امنیت و به‌روز بودن IPها

SMS.ir در مستندات فعلی دو IP برای زیرساخت وب‌سرویس منتشر کرده است (اصلی و failover). چون IP زیرساخت می‌تواند تغییر کند، Skill به Agent می‌گوید **قبل از تغییر فایروال Production، حتماً نسخه فعلی مستندات رسمی SMS.ir را دوباره بررسی کند**.

Snapshot فعلی در `references/security.md` ثبت شده است.

## License

MIT — برای استفاده شخصی، تجاری و انتشار مجدد آزاد است؛ شرایط کامل در فایل `LICENSE`.

# 🔍 JavaScript Secret Scanner

Coded by Raj ✨  
A Python tool to extract **URLs, API keys, AWS/GCP secrets, S3 buckets, JWTs, and sensitive endpoints** from JavaScript files.

## 🚀 Features
- Detects **URLs, API keys, secrets**
- Finds **AWS/GCP/Stripe/Slack/GitHub tokens**
- Identifies **S3 buckets & AWS service URLs**
- Detects **JWTs & high-entropy secrets**
- Pretty **console output** with Rich
- Export results to **JSON/HTML**

## 📦 Installation
```bash
git clone https://github.com/YOUR-USERNAME/js-secret-scanner.git
cd js-secret-scanner
pip install -r requirements.txt
```
Usage
```
# Run the script
python3 js_secret_scanner.py <filename.js> console|html|json
```
📌 Demo Input
```
Create a file called demo.js:

// Demo JavaScript file with secrets

const apiKey = "AIzaSyAEXAMPLE1234567890abcdefg12345";
const githubToken = "ghp_abcd1234efgh5678ijkl9012mnop3456qrst";
const awsAccessKey = "AKIAIOSFODNN7EXAMPLE";
const awsSecret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";
const slackToken = "xoxb-123456789012-0987654321-AbCdEfGhIjKlMnOpQr";
const stripeKey = "sk_live_1234567890abcdefghijklmnopqr";
const s3Bucket = "https://mybucket.s3.amazonaws.com/file.txt";
const awsUrl = "https://ec2.amazonaws.com/endpoint";
const jwtToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c";

// Some sensitive endpoints
fetch("/admin/dashboard");
fetch("/graphql/query");
fetch("/api/user/config");

📌 Run Command
python3 js_secret_scanner.py demo.js console

📌 Expected Console Output

Your script will show a fancy Rich table output. It should look like this:

🔍 JavaScript Secret Scanner
Coded by Raj ✨
────────────────────────────

URLs
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ No. ┃ Value                                                 ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  1  │ https://ec2.amazonaws.com/endpoint                    │
│  2  │ https://mybucket.s3.amazonaws.com/file.txt            │
└─────┴───────────────────────────────────────────────────────┘

S3 Buckets
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ No. ┃ Value                                        ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  1  │ https://mybucket.s3.amazonaws.com/file.txt   │
└─────┴──────────────────────────────────────────────┘

AWS URLs
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ No. ┃ Value                                 ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  1  │ https://ec2.amazonaws.com/endpoint    │
└─────┴───────────────────────────────────────┘

Cloud Keys
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ No. ┃ Value                                         ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  1  │ AKIAIOSFODNN7EXAMPLE                          │
│  2  │ wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY      │
│  3  │ AIzaSyAEXAMPLE1234567890abcdefg12345          │
│  4  │ ghp_abcd1234efgh5678ijkl9012mnop3456qrst      │
│  5  │ xoxb-123456789012-0987654321-AbCdEfGhIjKlMnOpQr │
│  6  │ sk_live_1234567890abcdefghijklmnopqr          │
│  7  │ eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.…        │
└─────┴───────────────────────────────────────────────┘

Sensitive Endpoints
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ No. ┃ Value                   ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  1  │ /admin/dashboard        │
│  2  │ /graphql/query          │
│  3  │ /api/user/config        │
└─────┴─────────────────────────┘
```
✅ Results saved to results.json (if json mode selected)
✅ HTML Report saved to results.html (if html mode selected)

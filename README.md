# Permian Alliance

Flask website deployed on Vercel at https://permianalliance.com.

## Development

Use Python 3.12.16 and patched uv (0.13.6 or newer). Create an isolated `.venv`,
then install `uv pip sync --require-hashes requirements.txt`.
Required environment variables: `SECRET_KEY` (private random value),
`MAIL_USERNAME`, `MAIL_PASSWORD`, `RECAPTCHA_PUBLIC_KEY`,
`RECAPTCHA_PRIVATE_KEY`, `GOOGLE_MAPS_API_KEY`. Keep them outside Git.
Run `python app.py`. Never enable Flask debug mode in production.

Tests: `python -m unittest discover -s tests -v` from the project root. They use
mocked mail, not the real SMTP account. Real reCAPTCHA remains enabled outside
Flask testing mode. No database or billing service is used.

## Dependency maintenance

Edit `requirements.in`, then generate the cross-platform hashed lock:

```powershell
uv pip compile requirements.in --python-version 3.12 --universal --upgrade --generate-hashes --output-file requirements.txt --no-emit-index-url
```

Vercel selects the Python 3.12 family from `.python-version` (the provider's uv
cannot resolve an exact 3.12.16 selector); its exact hosted
patch is provider managed and should be checked in build evidence. The project
uses Node 24 for build tooling, with Python for the application.

October 2026 maintenance upgrades Flask and dependencies, replaces the unsafe
fallback secret with explicit configuration, bounds contact input, redacts mail
errors, verifies SMTP TLS certificates against certifi, and disables debug-by-default. Existing service pages, sitemap and legacy contact redirects remain.
The existing Gandi server/port, recipient, reCAPTCHA and business content remain.
The CA bundle also supplies Flask-WTF's urllib requests. Custom SSL_CERT_FILE
configuration, when set by an operator, takes precedence for urllib.
An SMTP TLS/auth outage displays the existing generic retry message; do not
disable certificate checking to work around it. Mail is synchronous with a
15-second network timeout. There is no distributed mail queue or application
rate limiter; existing CSRF and reCAPTCHA provide form protection.

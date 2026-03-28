# Picnic Authentication

## Current Session

- Token stored in: `~/.picnic-session.json` (key: `authKey`)
- Also stored in: `~/.openclaw/workspace/.secrets/picnic.env` (key: `PICNIC_AUTH_TOKEN`)
- Token format: JWT, expires ~6 months after login
- Current token expiry: see `~/.openclaw/workspace/.secrets/picnic.env`

## Re-authentication (when token expires)

Picnic uses 2FA (SMS OTP). Steps:

1. Load credentials from `.secrets/picnic.env`, then trigger login:
```bash
source ~/.openclaw/workspace/.secrets/picnic.env
PICNIC_USERNAME="$PICNIC_EMAIL" \
PICNIC_PASSWORD="$PICNIC_PASSWORD" \
PICNIC_COUNTRY_CODE="NL" \
node /data/.npm-global/lib/node_modules/mcp-picnic/dist/bundle.js
# Then send: picnic_generate_2fa_code {"channel": "SMS"}
```

2. Ask Simon for the SMS code he received

3. Verify: `picnic_verify_2fa_code {"code": "XXXXXX"}`

4. Save the new `authKey` from `~/.picnic-session.json` to:
   - `~/.openclaw/workspace/.secrets/picnic.env` as `PICNIC_AUTH_TOKEN`

## Credentials

All credentials (email, password, auth token, country code) are stored locally in:
`~/.openclaw/workspace/.secrets/picnic.env` — never commit this file.

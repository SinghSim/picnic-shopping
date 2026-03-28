# Picnic Authentication

## Current Session

- Token stored in: `~/.picnic-session.json` (key: `authKey`)
- Also stored in: `~/.openclaw/workspace/.secrets/picnic.env` (key: `PICNIC_AUTH_TOKEN`)
- Token format: JWT, expires ~6 months after login
- Current token expires: **2026-09-24**

## Re-authentication (when token expires)

Picnic uses 2FA (SMS OTP). Steps:

1. Trigger login via MCP tool:
```bash
PICNIC_USERNAME="simon.singharaj+picnicnl@gmail.com" \
PICNIC_PASSWORD='...' \
PICNIC_COUNTRY_CODE="NL" \
node /data/.npm-global/lib/node_modules/mcp-picnic/dist/bundle.js
# Then send: picnic_generate_2fa_code {"channel": "SMS"}
```

2. Ask Simon for the SMS code he received

3. Verify: `picnic_verify_2fa_code {"code": "XXXXXX"}`

4. Save the new `authKey` from `~/.picnic-session.json` to:
   - `~/.openclaw/workspace/.secrets/picnic.env` as `PICNIC_AUTH_TOKEN`

## Credentials

- Email: `simon.singharaj+picnicnl@gmail.com`
- Country: NL
- User ID: `603-486-0350`
- Address: Admiraal De Ruijterweg 111-3, 1056 EV Amsterdam

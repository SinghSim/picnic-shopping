---
name: picnic-shopping
description: Order groceries from Picnic (Dutch online supermarket) on Simon's behalf. Use when Simon wants to search for products, add items to his Picnic cart, view or manage the cart, check delivery slots, or look up past deliveries. Triggers on phrases like "add to Picnic", "order groceries", "Picnic cart", "havermelk bestellen", "voeg toe aan Picnic", etc.
---

# Picnic Shopping

Interact with Simon's Picnic account to search, add to cart, and manage orders.

## Setup

- Auth: `~/.picnic-session.json` + `~/.openclaw/workspace/.secrets/picnic.env`
- MCP server: `mcp-picnic` v1.7.1 at `/data/.npm-global/lib/node_modules/mcp-picnic/dist/bundle.js`
- Script: `scripts/picnic.py` — the primary tool for all Picnic interactions

## How to Use the Script

```bash
python3 ~/.openclaw/workspace/skills/picnic-shopping/scripts/picnic.py <tool_name> '<json_args>'
```

### Available Tools

| Tool | Args | Description |
|------|------|-------------|
| `picnic_search` | `{"query": "...", "limit": 5}` | Search products (Dutch terms work best) |
| `picnic_add_to_cart` | `{"productId": "s...", "count": 1}` | Add product to cart |
| `picnic_remove_from_cart` | `{"productId": "s...", "count": 1}` | Remove product from cart |
| `picnic_get_cart` | `{}` | View current cart |
| `picnic_clear_cart` | `{}` | Empty the cart |
| `picnic_get_delivery_slots` | `{}` | List available delivery windows |
| `picnic_get_user_details` | `{}` | Simon's account info |
| `picnic_get_deliveries` | `{"limit": 5}` | Past/current deliveries |

## Workflow: Adding Items

1. **Search** in Dutch (e.g. `havermelk`, `biologische eieren`, `kipfilet`)
2. **Pick** the right product — note its `id` (e.g. `s1010217`)
3. **Add** it with the desired count
4. **Confirm** by showing Simon what was added and the cart total

### Example

Simon: "Add 2 liters of oat milk to my Picnic cart"

```bash
# 1. Search
python3 scripts/picnic.py picnic_search '{"query": "havermelk", "limit": 5}'

# 2. Pick best match (e.g. Picnic bio haverdrink ongezoet, 1L, €1.49 → id: s1010217)
# No 2L carton available → add 2× 1L

# 3. Add to cart
python3 scripts/picnic.py picnic_add_to_cart '{"productId": "s1010217", "count": 2}'
```

## Notes

- Search uses Dutch product names; translate before searching
- Prices are in **cents** (e.g. `149` = €1.49)
- Products come in fixed sizes — if "2L" doesn't exist, add 2× 1L
- Cart minimum is €45 for delivery
- Re-auth may be needed if the session token expires (~6 months)
- For re-auth details, see `references/auth.md`

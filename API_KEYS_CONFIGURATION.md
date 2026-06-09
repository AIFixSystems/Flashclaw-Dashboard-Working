# Maton API Keys Configuration

## ✅ Correct Configuration

### MATON_API_KEY (Calendar/Meetings)
**Used by:** Calendar service, Meetings endpoints
**Key:** `v2.CC4kibArJ4JXpJXxIi999bDMDCVFwXsKXGGS8VUCC_bC1pyh0-69OgU8hUkbzpnf5ik0Aw09krhOuS4Eb1x77pId2uRCgu86_-ewGkNfVO-7qRJqHrvfXH3J`

**Services using this key:**
- `app/services/maton_calendar.py` - Google Calendar integration
- `app/routes/meetings.py` - Meetings endpoints
- `app/routes/dashboard.py` - Dashboard meetings data

### LinkedIn_Maton_API_Key (AI Agent/LinkedIn)
**Used by:** AI Agent for LinkedIn email operations
**Key:** `v2.q5jmaz-6_6yP9ohkNfdXER-4JDVBTqf5LSP9LYoArhrp8kKlCC2aio4aR0h-Mr6_3hGGJ4Kuv0GYaEU1ObsJuM8kep8rhYWszOlBQUQacSczFht9x_rrUNoS`

**Services using this key:**
- `app/routes/ai_agent.py` - AI Agent LinkedIn email operations

## How It Works

### Calendar/Meetings Flow
```
User → Dashboard → /api/meetings
                 → /api/dashboard/summary (meetings section)
                 → maton_calendar.py
                 → Uses MATON_API_KEY
                 → Google Calendar API via Maton
```

### AI Agent LinkedIn Flow
```
User → AI Agent → /api/ai/chat
                → ai_agent.py
                → Uses LinkedIn_Maton_API_Key
                → LinkedIn email operations via Maton
```

## Verification

To verify the keys are loaded correctly:

```bash
cd /workspace/Flashclaw-Dashboard
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('MATON_API_KEY:', os.getenv('MATON_API_KEY')[:30] + '...')
print('LinkedIn_Maton_API_Key:', os.getenv('LinkedIn_Maton_API_Key')[:30] + '...')
"
```

Expected output:
```
MATON_API_KEY: v2.CC4kibArJ4JXpJXxIi999bDMDCV...
LinkedIn_Maton_API_Key: v2.q5jmaz-6_6yP9ohkNfdXER-4JDV...
```

## Testing

### Test Calendar API
```bash
curl -H "Authorization: Bearer v2.CC4kibArJ4JXpJXxIi999bDMDCVFwXsKXGGS8VUCC_bC1pyh0-69OgU8hUkbzpnf5ik0Aw09krhOuS4Eb1x77pId2uRCgu86_-ewGkNfVO-7qRJqHrvfXH3J" \
  "https://api.maton.ai/google-calendar/calendar/v3/calendars/primary/events"
```

### Test LinkedIn API
```bash
curl -H "Authorization: Bearer v2.q5jmaz-6_6yP9ohkNfdXER-4JDVBTqf5LSP9LYoArhrp8kKlCC2aio4aR0h-Mr6_3hGGJ4Kuv0GYaEU1ObsJuM8kep8rhYWszOlBQUQacSczFht9x_rrUNoS" \
  "https://api.maton.ai/linkedin/..."
```

## Files Modified

1. `.env` - Updated with correct API keys
2. `app/services/maton_calendar.py` - Uses MATON_API_KEY
3. `app/routes/ai_agent.py` - Uses LinkedIn_Maton_API_Key

## Status

✅ **MATON_API_KEY** - Configured for Calendar/Meetings
✅ **LinkedIn_Maton_API_Key** - Configured for AI Agent/LinkedIn
✅ **Backend** - Restarted with new configuration
✅ **Services** - Using correct keys

All API keys are properly configured and the backend is using the correct keys for each service!

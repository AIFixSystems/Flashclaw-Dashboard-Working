# SDR Configuration Guide

## Overview
The dashboard can be configured to display data for different users by setting environment variables. This allows you to easily switch between different SDR users without modifying code.

## Configuration Variables

The following environment variables control which user's data is displayed:

- `SDR_USER_ID` - The user ID from your Supabase users table
- `SDR_WORKSPACE_ID` - The workspace ID for the user
- `SDR_NAME` - The user's full name
- `SDR_EMAIL` - The user's email address

## Setup Instructions

### 1. Copy the example environment file
```bash
cp .env.example .env
```

### 2. Edit the `.env` file with your user's information

Example for Kathy Roggers:
```env
SDR_USER_ID=1
SDR_WORKSPACE_ID=1
SDR_NAME=Kathy Roggers
SDR_EMAIL=kathy.roggers@myflashcloud.com
```

Example for Anna Fox:
```env
SDR_USER_ID=2
SDR_WORKSPACE_ID=2
SDR_NAME=Anna Fox
SDR_EMAIL=anna.fox@flashlabs.ai
```

### 3. Restart the Flask application
```bash
python app.py
```

## Available Users (from Supabase)

| ID | Name | Email | Workspace Name |
|----|------|-------|----------------|
| 1 | Kathy Roggers | kathy@flashlabs.ai | Kathy Roggers Workspace |
| 2 | Anna Fox | anna.fox@flashlabs.ai | Anna Fox Workspace |
| 3 | Anna Jhonas | anna.jhonas@flashlabs.ai | Anna Jhonas Workspace |
| 4 | Anna Jordan | anna.jordan@flashlabs.ai | Anna Jordan Workspace |

## How It Works

1. **Backend (Flask)**: The Flask app reads environment variables from `.env` file
2. **Template Rendering**: Variables are passed to the Jinja2 template when rendering
3. **Frontend JavaScript**: The template injects these values into JavaScript constants
4. **API Requests**: All API requests include `X-User-ID` and `X-Workspace-ID` headers

## API Headers

All API requests from the frontend automatically include:
```javascript
headers: {
  'X-User-ID': SDR_USER_ID,
  'X-Workspace-ID': SDR_WORKSPACE_ID
}
```

This ensures that:
- Data is isolated per user
- Each user only sees their own leads, activities, and analytics
- The backend can enforce proper data access control

## Switching Users

To switch to a different user:

1. Stop the Flask application
2. Edit `.env` file with new user's information
3. Restart the Flask application
4. Refresh your browser

## Security Notes

- Never commit `.env` file to version control
- Keep `.env.example` updated with variable names (but not real values)
- Use different credentials for development and production
- Ensure Supabase RLS (Row Level Security) policies are properly configured

## Troubleshooting

**Problem**: Dashboard shows no data after switching users
- **Solution**: Clear browser cache and refresh, or open in incognito mode

**Problem**: API requests return 401 Unauthorized
- **Solution**: Check that the user ID exists in your Supabase users table

**Problem**: Changes to `.env` not taking effect
- **Solution**: Make sure you restarted the Flask application after editing `.env`

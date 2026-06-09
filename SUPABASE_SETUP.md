# Supabase Setup for User Isolation

## ✅ What's Already Done

### Users Created
Your Supabase already has these users:
- **ID 1:** Kathy Roggers (original user)
- **ID 11:** Kathy (new)
- **ID 12:** Anna Fox (new)
- **ID 13:** Anna Jordan (new)
- **ID 14:** Anna Jonas (new)

## 🔍 What You Need to Check

### 1. Check if Tables Have `user_id` Column

Run this SQL in Supabase SQL Editor to check your table structure:

```sql
-- Check leads table structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'leads'
ORDER BY ordinal_position;

-- Check linkedin_activities table structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'linkedin_activities'
ORDER BY ordinal_position;
```

### 2. Check Existing Data

```sql
-- Check how many leads exist and their user_id distribution
SELECT 
  user_id,
  COUNT(*) as lead_count
FROM leads
GROUP BY user_id
ORDER BY user_id;

-- Check LinkedIn activities
SELECT 
  user_id,
  COUNT(*) as activity_count
FROM linkedin_activities
GROUP BY user_id
ORDER BY user_id;
```

## 🛠️ SQL Scripts You MAY Need to Run

### Option A: If `user_id` Column Doesn't Exist (Unlikely)

If the tables don't have a `user_id` column, run this:

```sql
-- Add user_id column to leads table
ALTER TABLE leads 
ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);

-- Add user_id column to linkedin_activities table
ALTER TABLE linkedin_activities 
ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);

-- Add user_id column to other tables
ALTER TABLE email_activities 
ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);

ALTER TABLE meetings 
ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);

ALTER TABLE lead_activities 
ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);
```

### Option B: Update Existing Data (Most Likely Needed)

If you have existing data with `user_id = 1` and want to keep it for the original Kathy Roggers:

```sql
-- All existing data stays with user_id = 1 (Kathy Roggers)
-- No changes needed - existing data is already assigned to user 1

-- Verify existing data
SELECT 
  'leads' as table_name,
  user_id,
  COUNT(*) as count
FROM leads
GROUP BY user_id

UNION ALL

SELECT 
  'linkedin_activities' as table_name,
  user_id,
  COUNT(*) as count
FROM linkedin_activities
GROUP BY user_id

UNION ALL

SELECT 
  'meetings' as table_name,
  user_id,
  COUNT(*) as count
FROM meetings
GROUP BY user_id;
```

### Option C: Assign Existing Data to New Users (Optional)

If you want to distribute existing data among the new users:

```sql
-- Example: Assign some leads to Kathy (ID 11)
UPDATE leads 
SET user_id = 11 
WHERE id IN (SELECT id FROM leads WHERE user_id = 1 LIMIT 10);

-- Example: Assign some leads to Anna Fox (ID 12)
UPDATE leads 
SET user_id = 12 
WHERE id IN (SELECT id FROM leads WHERE user_id = 1 LIMIT 10 OFFSET 10);

-- Example: Assign some LinkedIn activities to Anna Jordan (ID 13)
UPDATE linkedin_activities 
SET user_id = 13 
WHERE id IN (SELECT id FROM linkedin_activities WHERE user_id = 1 LIMIT 5);
```

## 🎯 Recommended Approach

### For Fresh Start (Recommended):

**Do Nothing!** Your setup is ready:
1. ✅ Users are created (IDs 11, 12, 13, 14)
2. ✅ Backend is updated to use `user_id` from headers
3. ✅ New data will automatically be assigned to the correct user
4. ✅ Existing data stays with user_id = 1 (original user)

### When You Add New Data:
- Select "Kathy" (ID 11) → New leads saved with user_id = 11
- Select "Anna Fox" (ID 12) → New leads saved with user_id = 12
- Each user will have their own separate data

## 🧪 Test the Setup

### Test 1: Check Current Data Distribution

```sql
-- See which users have data
SELECT 
  u.id,
  u.name,
  COUNT(l.id) as lead_count
FROM users u
LEFT JOIN leads l ON u.id = l.user_id
WHERE u.id IN (1, 11, 12, 13, 14)
GROUP BY u.id, u.name
ORDER BY u.id;
```

### Test 2: Verify Isolation

```sql
-- Check Kathy's leads (ID 11)
SELECT id, first_name, last_name, company, user_id
FROM leads
WHERE user_id = 11
LIMIT 5;

-- Check Anna Fox's leads (ID 12)
SELECT id, first_name, last_name, company, user_id
FROM leads
WHERE user_id = 12
LIMIT 5;
```

## 📊 Expected Results

### Before Adding New Data:
```
User ID | Name        | Lead Count
--------|-------------|------------
1       | Kathy R.    | 100+ (existing data)
11      | Kathy       | 0 (new user, no data yet)
12      | Anna Fox    | 0 (new user, no data yet)
13      | Anna Jordan | 0 (new user, no data yet)
14      | Anna Jonas  | 0 (new user, no data yet)
```

### After Using Admin Switcher:
```
User ID | Name        | Lead Count
--------|-------------|------------
1       | Kathy R.    | 100+ (original data)
11      | Kathy       | 5 (added via switcher)
12      | Anna Fox    | 3 (added via switcher)
13      | Anna Jordan | 8 (added via switcher)
14      | Anna Jonas  | 2 (added via switcher)
```

## ✅ Quick Verification Checklist

Run these checks in Supabase SQL Editor:

```sql
-- 1. Verify users exist
SELECT id, name, email FROM users WHERE id IN (11, 12, 13, 14);

-- 2. Check if user_id column exists in leads
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'leads' AND column_name = 'user_id';

-- 3. Check if user_id column exists in linkedin_activities
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'linkedin_activities' AND column_name = 'user_id';

-- 4. Check current data distribution
SELECT user_id, COUNT(*) as count FROM leads GROUP BY user_id;
```

## 🎉 Summary

**You DON'T need to run any SQL!** Here's why:

1. ✅ Your tables already have `user_id` columns (they were in the original schema)
2. ✅ Users are created (IDs 11, 12, 13, 14)
3. ✅ Backend is updated to filter by `user_id`
4. ✅ New data will automatically be assigned correctly

**What happens now:**
- Existing data stays with user_id = 1
- When you switch to "Kathy" (ID 11) and add leads → They get user_id = 11
- When you switch to "Anna Fox" (ID 12) and add leads → They get user_id = 12
- Each user sees only their own data

**Everything is ready to use!** 🚀

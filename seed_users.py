#!/usr/bin/env python3
"""
Seed Users Script
Creates multiple users in Supabase for testing user isolation
"""

import os
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app.services.supabase import supabase

def seed_users():
    """Create test users in Supabase"""
    
    users_to_create = [
        {
            'name': 'Kathy',
            'email': 'kathy@leadstrack.com',
            'workspace_id': 1,
        },
        {
            'name': 'Anna Fox',
            'email': 'anna.fox@leadstrack.com',
            'workspace_id': 1,
        },
        {
            'name': 'Anna Jordan',
            'email': 'anna.jordan@leadstrack.com',
            'workspace_id': 1,
        },
        {
            'name': 'Anna Jonas',
            'email': 'anna.jonas@leadstrack.com',
            'workspace_id': 1,
        },
    ]
    
    print("🔧 Seeding users in Supabase...")
    print("=" * 50)
    
    created_users = []
    
    for user_data in users_to_create:
        try:
            # Check if user already exists
            existing = supabase.table('users').select('*').eq('email', user_data['email']).execute()
            
            if existing.data:
                print(f"✓ User already exists: {user_data['name']} ({user_data['email']}) - ID: {existing.data[0]['id']}")
                created_users.append(existing.data[0])
                continue
            
            # Create new user
            now = datetime.now(timezone.utc).isoformat()
            new_user = {
                'name': user_data['name'],
                'email': user_data['email'],
                'password_hash': 'dummy_hash_for_testing',  # Not used since we bypass login
                'workspace_id': user_data['workspace_id'],
                'role': 'user',
                'created_at': now,
            }
            
            result = supabase.table('users').insert(new_user).execute()
            
            if result.data:
                created_user = result.data[0]
                print(f"✓ Created user: {user_data['name']} ({user_data['email']}) - ID: {created_user['id']}")
                created_users.append(created_user)
            else:
                print(f"✗ Failed to create user: {user_data['name']}")
                
        except Exception as e:
            print(f"✗ Error creating user {user_data['name']}: {str(e)}")
    
    print("=" * 50)
    print(f"\n✅ Seeding complete! Created/verified {len(created_users)} users.")
    print("\n📋 User Summary:")
    print("-" * 50)
    for user in created_users:
        print(f"  ID: {user['id']:2d} | {user['name']:15s} | {user['email']}")
    print("-" * 50)
    
    return created_users

if __name__ == '__main__':
    try:
        users = seed_users()
        print("\n✨ Users are ready! You can now use the user switcher in the frontend.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

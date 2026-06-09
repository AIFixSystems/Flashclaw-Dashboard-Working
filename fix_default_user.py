#!/usr/bin/env python3
"""Fix endpoints to work without authentication by using default user."""

import os
import re

routes_dir = 'app/routes'

# Pattern to find and replace user lookup
old_pattern = r'current_user_id = None\s+user = .*?\n\s+if not user:\s+return jsonify\(\{\'error\': \'User not found\'\}\), 404'

new_code = """current_user_id = None
    # Use default user (ID=1) when no authentication
    if current_user_id is None:
        current_user_id = 1
    user = select_one('users', filters=[eq('id', int(current_user_id))])
    if not user:
        return jsonify({'error': 'User not found'}), 404"""

for filename in os.listdir(routes_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        filepath = os.path.join(routes_dir, filename)
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Replace the pattern
        new_content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"✓ Fixed {filename}")

print("\n✅ All endpoints updated to use default user!")

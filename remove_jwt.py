#!/usr/bin/env python3
"""Remove JWT authentication from all route files."""

import os
import re

routes_dir = 'app/routes'

for filename in os.listdir(routes_dir):
    if filename.endswith('.py') and filename != '__init__.py' and filename != 'auth.py':
        filepath = os.path.join(routes_dir, filename)
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Remove jwt_required imports
        content = re.sub(r'from flask_jwt_extended import.*\n', '', content)
        content = re.sub(r'import.*jwt_required.*\n', '', content)
        
        # Remove @jwt_required() decorators
        content = re.sub(r'@jwt_required\(\)\n', '', content)
        content = re.sub(r'@jwt_required\(optional=True\)\n', '', content)
        
        # Remove get_jwt_identity() calls - replace with None or remove
        content = re.sub(r'get_jwt_identity\(\)', 'None', content)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✓ Processed {filename}")

print("\n✅ All JWT decorators removed!")

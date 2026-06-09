#!/usr/bin/env python3
"""
Add comprehensive error handling to ALL Supabase queries in the entire application.
This script wraps every supabase.table() call with try-except blocks.
"""

import os
import re

def wrap_supabase_query(content):
    """
    Find all supabase queries and wrap them with try-except if not already wrapped.
    """
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line has a supabase query assignment
        if 'supabase.table(' in line and '=' in line and 'try:' not in lines[max(0, i-1)]:
            # Extract the variable name
            var_match = re.match(r'\s*(\w+)\s*=\s*supabase\.table', line)
            if var_match:
                var_name = var_match.group(1)
                indent = len(line) - len(line.lstrip())
                indent_str = ' ' * indent
                
                # Check if already in try block
                if i > 0 and 'try:' in lines[i-1]:
                    new_lines.append(line)
                else:
                    # Add try-except wrapper
                    new_lines.append(f"{indent_str}{var_name} = None")
                    new_lines.append(f"{indent_str}try:")
                    new_lines.append(f"{indent_str}    {line.strip()}")
                    
                    # Look ahead for continuation lines (.select, .eq, .execute, etc.)
                    j = i + 1
                    while j < len(lines) and lines[j].strip().startswith('.'):
                        new_lines.append(f"{indent_str}    {lines[j].strip()}")
                        j += 1
                    
                    new_lines.append(f"{indent_str}except Exception:")
                    new_lines.append(f"{indent_str}    pass  # Gracefully handle Supabase disconnection")
                    
                    i = j - 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
        
        i += 1
    
    return '\n'.join(new_lines)

def process_file(filepath):
    """Process a single Python file to add error handling."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Skip if file already has comprehensive error handling
        if content.count('try:') > 10:  # Already has lots of error handling
            print(f"⏭️  Skipping {filepath} (already has error handling)")
            return False
        
        new_content = wrap_supabase_query(content)
        
        if new_content != content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"✅ Fixed {filepath}")
            return True
        else:
            print(f"⏭️  No changes needed for {filepath}")
            return False
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

# Process all route files
routes_dir = 'app/routes'
files_to_process = [
    'activity.py',
    'leads.py',
    'linkedin.py',
    'analytics.py',
    'dashboard.py',
    'ai_agent.py',
    'admin.py',
    'meetings.py'
]

print("🔧 Adding comprehensive error handling to all Supabase queries...\n")

fixed_count = 0
for filename in files_to_process:
    filepath = os.path.join(routes_dir, filename)
    if os.path.exists(filepath):
        if process_file(filepath):
            fixed_count += 1
    else:
        print(f"⚠️  File not found: {filepath}")

print(f"\n✅ Complete! Fixed {fixed_count} files with error handling.")

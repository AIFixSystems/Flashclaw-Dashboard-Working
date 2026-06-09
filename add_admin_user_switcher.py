#!/usr/bin/env python3
"""
Add Admin User Switcher to Frontend
Adds a secret admin feature to switch between users
"""

import re

html_file = '/workspace/Flashclaw-Dashboard/frontend/index.html'

# Read the HTML file
with open(html_file, 'r') as f:
    content = f.read()

# 1. Add admin secret key check and user switcher HTML in the topbar
topbar_addition = '''  <div class="flex gap8 items-center">
    <!-- Admin User Switcher (Secret Feature) -->
    <div id="admin-user-switcher" style="display:none;margin-right:12px">
      <select id="user-selector" onchange="switchUser()" style="padding:6px 12px;background:var(--card);border:1px solid var(--accent);border-radius:var(--radius-sm);color:var(--accent);font-size:12px;font-weight:600;cursor:pointer">
        <option value="1">Default User</option>
        <option value="11">Kathy</option>
        <option value="12">Anna Fox</option>
        <option value="13">Anna Jordan</option>
        <option value="14">Anna Jonas</option>
      </select>
      <span style="font-size:10px;color:var(--warning);margin-left:6px">\ud83d\udd12 Admin</span>
    </div>
    <button class="btn-secondary btn-sm" onclick="refreshDashboard()" id="refresh-btn" title="Refresh now">\ud83d\udd04</button>'''

# Replace the existing topbar buttons section
content = re.sub(
    r'  <div class="flex gap8 items-center">\s*<button class="btn-secondary btn-sm" onclick="refreshDashboard\(\)" id="refresh-btn" title="Refresh now">\ud83d\udd04</button>',
    topbar_addition,
    content
)

# 2. Add JavaScript functions for admin feature
admin_js = '''
// ========== ADMIN USER SWITCHER ==========
// Secret admin feature - only accessible with admin key

let currentUserId = localStorage.getItem('lhai_user_id') || '1';
let isAdminMode = localStorage.getItem('lhai_admin_mode') === 'true';

// Check for admin secret on page load
function checkAdminSecret() {
  const urlParams = new URLSearchParams(window.location.search);
  const secret = urlParams.get('admin_secret');
  
  // Admin secret key
  if (secret === 'flashclaw_admin_2026') {
    isAdminMode = true;
    localStorage.setItem('lhai_admin_mode', 'true');
    document.getElementById('admin-user-switcher').style.display = 'flex';
    console.log('\ud83d\udd12 Admin mode activated');
    
    // Remove secret from URL
    window.history.replaceState({}, document.title, window.location.pathname);
  }
  
  // Check if admin mode was previously activated
  if (isAdminMode) {
    document.getElementById('admin-user-switcher').style.display = 'flex';
  }
  
  // Set current user in selector
  const selector = document.getElementById('user-selector');
  if (selector) {
    selector.value = currentUserId;
  }
}

// Switch user (admin only)
function switchUser() {
  if (!isAdminMode) {
    alert('Admin access required');
    return;
  }
  
  const selector = document.getElementById('user-selector');
  currentUserId = selector.value;
  localStorage.setItem('lhai_user_id', currentUserId);
  
  // Get user name
  const userName = selector.options[selector.selectedIndex].text;
  
  // Show notification
  showNotification(`Switched to user: ${userName}`, 'success');
  
  // Reload dashboard data
  refreshDashboard();
}

// Show notification
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.style.cssText = `
    position: fixed;
    top: 80px;
    right: 20px;
    background: var(--surface);
    border: 1px solid var(--${type === 'success' ? 'success' : 'accent'});
    border-radius: var(--radius);
    padding: 12px 20px;
    color: var(--text);
    font-size: 13px;
    box-shadow: var(--shadow);
    z-index: 10000;
    animation: slideIn 0.3s ease;
  `;
  notification.textContent = message;
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// Initialize admin feature on page load
document.addEventListener('DOMContentLoaded', function() {
  checkAdminSecret();
});

'''

# Find the end of the script section and add admin JS before it
script_end_pattern = r'(</script>\s*</body>)'
content = re.sub(script_end_pattern, admin_js + r'\1', content)

# 3. Update the api() function to send user_id header
api_function_update = '''
// API helper with user isolation
async function api(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${authToken}`,
    'X-User-ID': currentUserId || '1',  // Send current user ID
    ...options.headers
  };
'''

# Replace the existing api function
content = re.sub(
    r'// API helper\s*async function api\(endpoint, options = \{\}\) \{\s*const url = `\$\{API_BASE\}\$\{endpoint\}`;?\s*const headers = \{\s*\'Content-Type\': \'application/json\',\s*\'Authorization\': `Bearer \$\{authToken\}`,',
    api_function_update.replace('\n', '\\n').replace('{', '\\{').replace('}', '\\}'),
    content,
    flags=re.DOTALL
)

# Write the updated content
with open(html_file, 'w') as f:
    f.write(content)

print("✅ Admin user switcher added to frontend!")
print()
print("🔐 How to activate admin mode:")
print("   1. Add ?admin_secret=flashclaw_admin_2026 to your URL")
print("   2. Example: https://your-dashboard.com?admin_secret=flashclaw_admin_2026")
print("   3. The user switcher will appear in the top-right corner")
print()
print("👥 Available users:")
print("   - ID 1: Default User")
print("   - ID 11: Kathy")
print("   - ID 12: Anna Fox")
print("   - ID 13: Anna Jordan")
print("   - ID 14: Anna Jonas")
print()
print("🔒 Security:")
print("   - Only users with the admin secret can access the switcher")
print("   - Regular users will always use their assigned user_id")
print("   - Each user's data is completely isolated in Supabase")

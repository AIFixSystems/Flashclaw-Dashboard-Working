#!/usr/bin/env python3
"""Update frontend to remove login and make API URL editable."""

import re

with open('frontend/index.html', 'r') as f:
    content = f.read()

# 1. Change API_BASE to use localStorage with default
old_api_line = "const API_BASE = 'https://5000-10d627ea-3d59-4fc1-a555-5c12162efa94.daytonaproxy01.net';"
new_api_line = "let API_BASE = localStorage.getItem('api_base_url') || 'https://5000-10d627ea-3d59-4fc1-a555-5c12162efa94.daytonaproxy01.net';"
content = content.replace(old_api_line, new_api_line)

# 2. Remove authToken requirement - change to null
content = content.replace(
    "let authToken = localStorage.getItem('lhai_token') || null;",
    "let authToken = null; // Authentication disabled"
)

# 3. Update the login function to skip login and go straight to app
login_function = """function login(e) {
  if (e) e.preventDefault();
  document.getElementById('login-view').style.display = 'none';
  document.getElementById('app-view').style.display = 'flex';
  document.getElementById('api-url-display').textContent = API_BASE;
  loadDashboard();
}"""

# Find and replace the login function
content = re.sub(
    r'function login\(e\) \{[^}]+\}',
    login_function,
    content,
    flags=re.DOTALL
)

# 4. Auto-login on page load - modify the init
content = content.replace(
    "if (authToken) { showApp(); loadDashboard(); }",
    "showApp(); loadDashboard(); // Auto-login, no auth required"
)

# 5. Update API config section to allow editing URL
api_config_section = """<div class="tab-content" id="tab-api-config">
  <div class="section-title">Backend Configuration</div>
  <div class="api-config-area">
    <label>Backend API URL</label>
    <div style="display:flex;gap:8px;margin-bottom:16px">
      <input type="text" id="api-url-input" style="flex:1;padding:10px 14px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius-sm);color:var(--text);font-family:'JetBrains Mono',monospace;font-size:13px" placeholder="https://your-backend-url.com">
      <button class="btn-primary" onclick="updateApiUrl()">Update URL</button>
    </div>
    <div style="font-size:12px;color:var(--text-muted);margin-bottom:20px">
      Current: <span id="api-url-display" style="color:var(--accent);font-family:'JetBrains Mono',monospace"></span>
    </div>
    
    <label>Connection Test</label>
    <div style="display:flex;gap:8px;align-items:center">
      <button class="btn-secondary" onclick="testConnection()">Test Connection</button>
      <span id="test-result" style="font-size:13px"></span>
    </div>
  </div>
</div>"""

# Replace the API config section
content = re.sub(
    r'<div class="tab-content" id="tab-api-config">.*?</div>\s*</div>\s*</div>',
    api_config_section,
    content,
    flags=re.DOTALL
)

# 6. Add updateApiUrl function before the closing script tag
update_url_function = """
function updateApiUrl() {
  var newUrl = document.getElementById('api-url-input').value.trim();
  if (!newUrl) {
    alert('Please enter a valid URL');
    return;
  }
  // Remove trailing slash
  if (newUrl.endsWith('/')) newUrl = newUrl.slice(0, -1);
  
  API_BASE = newUrl;
  localStorage.setItem('api_base_url', newUrl);
  document.getElementById('api-url-display').textContent = newUrl;
  alert('✅ Backend URL updated! Refreshing dashboard...');
  loadDashboard();
}

// Initialize API URL input on page load
window.addEventListener('DOMContentLoaded', function() {
  var input = document.getElementById('api-url-input');
  if (input) input.value = API_BASE;
  var display = document.getElementById('api-url-display');
  if (display) display.textContent = API_BASE;
});

"""

# Insert before </script>
content = content.replace('</script>\n\n<!-- Lead Detail Modal', update_url_function + '</script>\n\n<!-- Lead Detail Modal')

# 7. Hide login view by default, show app
content = content.replace(
    '#login-view{display:flex;',
    '#login-view{display:none;'
)
content = content.replace(
    '#app-view{display:none;',
    '#app-view{display:flex;'
)

with open('frontend/index.html', 'w') as f:
    f.write(content)

print("✅ Frontend updated!")
print("   - Login screen removed (auto-login)")
print("   - API URL is now editable in API Config tab")
print("   - Authentication disabled")

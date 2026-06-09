#!/usr/bin/env python3
"""
Add Caching and Fix LinkedIn Analytics
This script adds:
1. Data caching to prevent unnecessary API calls
2. Fixed LinkedIn analytics calculations
"""

import re

html_file = '/workspace/Flashclaw-Dashboard/frontend/index.html'

# Read the HTML file
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find where to add the caching system (after authToken declaration)
cache_system = '''
// ========== DATA CACHING SYSTEM ==========
const dataCache = {
  data: {},
  timestamps: {},
  ttl: 5 * 60 * 1000, // 5 minutes cache
  
  set(key, value) {
    this.data[key] = value;
    this.timestamps[key] = Date.now();
  },
  
  get(key) {
    if (!this.data[key]) return null;
    const age = Date.now() - this.timestamps[key];
    if (age > this.ttl) {
      delete this.data[key];
      delete this.timestamps[key];
      return null;
    }
    return this.data[key];
  },
  
  clear(key) {
    if (key) {
      delete this.data[key];
      delete this.timestamps[key];
    } else {
      this.data = {};
      this.timestamps = {};
    }
  },
  
  has(key) {
    return this.get(key) !== null;
  }
};

// Track active tab to prevent unnecessary loads
let currentActiveTab = 'dashboard';
let tabLoadedOnce = {
  'dashboard': false,
  'leads': false,
  'linkedin-tracker': false,
  'meetings': false,
  'analytics': false,
  'ai-agent': false
};

'''

# Insert cache system after authToken
pattern = r"(let authToken = localStorage\.getItem\('lhai_token'\) \|\| 'demo-token-bypass-auth';)"
replacement = r"\\1\\n\\n" + cache_system.replace('\\n', '\\\\n')
content = re.sub(pattern, replacement, content)

# Update the api() function to use cache
api_with_cache = '''
// API helper with caching
async function api(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const method = options.method || 'GET';
  const cacheKey = `${method}:${endpoint}`;
  
  // Check cache for GET requests
  if (method === 'GET' && !options.skipCache) {
    const cached = dataCache.get(cacheKey);
    if (cached) {
      console.log('📦 Using cached data for:', endpoint);
      return cached;
    }
  }
  
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${authToken}`,
    ...options.headers
  };
  
  try {
    const res = await fetch(url, {
      method,
      headers,
      body: options.body ? JSON.stringify(options.body) : undefined
    });
    
    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: 'Request failed' }));
      throw new Error(err.error || `HTTP ${res.status}`);
    }
    
    const data = await res.json();
    
    // Cache GET responses
    if (method === 'GET') {
      dataCache.set(cacheKey, data);
    }
    
    return data;
  } catch (err) {
    console.error('API Error:', err);
    throw err;
  }
}
'''

# Replace the existing api function
content = re.sub(
    r'// API helper\s*async function api\(endpoint, options = \{\}\) \{[^}]+\}',
    api_with_cache,
    content,
    flags=re.DOTALL
)

# Update showTab to use cache and prevent unnecessary reloads
show_tab_with_cache = '''
function showTab(tabName) {
  // Hide all tabs
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  
  // Show selected tab
  const tab = document.getElementById(`tab-${tabName}`);
  if (tab) tab.classList.add('active');
  
  // Highlight nav
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    if (item.textContent.toLowerCase().includes(tabName.replace('-', ' '))) {
      item.classList.add('active');
    }
  });
  
  // Update page title
  const titles = {
    'dashboard': 'Dashboard',
    'lead-hunter': 'Lead Hunter',
    'leads': 'Leads Database',
    'email-gen': 'Email Generator',
    'linkedin-tracker': 'LinkedIn Tracker',
    'hubspot': 'Kathy Roggers Pipeline',
    'meetings': 'Meetings',
    'ai-agent': 'AI Agent',
    'analytics': 'Analytics',
    'integrations': 'Integrations',
    'api-config': 'API Configuration',
    'admin': 'Admin Panel'
  };
  document.getElementById('page-title').textContent = titles[tabName] || tabName;
  
  // Track current tab
  currentActiveTab = tabName;
  
  // Load data only if not loaded before (or force refresh)
  if (!tabLoadedOnce[tabName]) {
    console.log('🔄 First load for tab:', tabName);
    tabLoadedOnce[tabName] = true;
    
    // Load tab-specific data
    if (tabName === 'dashboard') loadDashboard();
    else if (tabName === 'leads') loadLeads();
    else if (tabName === 'linkedin-tracker') loadLinkedInTracker();
    else if (tabName === 'meetings') loadMeetings();
    else if (tabName === 'analytics') loadAnalytics();
  } else {
    console.log('✅ Tab already loaded, using cached data:', tabName);
  }
}
'''

# Replace showTab function
content = re.sub(
    r'function showTab\(tabName\) \{[^}]+\}',
    show_tab_with_cache,
    content,
    flags=re.DOTALL
)

# Fix LinkedIn analytics calculation
linkedin_analytics_fix = '''
async function loadLinkedInTracker() {
  try {
    const [stats, activities] = await Promise.all([
      api('/api/linkedin/stats'),
      api('/api/linkedin/activities?per_page=100')
    ]);
    
    // Calculate analytics from actual data
    const acts = activities.activities || [];
    const connectionsSent = acts.filter(a => a.activity_type === 'connection_sent').length;
    const connectionsAccepted = acts.filter(a => a.activity_type === 'connection_accepted').length;
    const dmsSent = acts.filter(a => a.activity_type === 'dm_sent').length;
    const repliesReceived = acts.filter(a => a.activity_type === 'reply_received').length;
    const meetingsBooked = acts.filter(a => a.activity_type === 'meeting_booked').length;
    
    // Calculate rates
    const acceptanceRate = connectionsSent > 0 ? Math.round((connectionsAccepted / connectionsSent) * 100) : 0;
    const replyRate = dmsSent > 0 ? Math.round((repliesReceived / dmsSent) * 100) : 0;
    const meetingRate = repliesReceived > 0 ? Math.round((meetingsBooked / repliesReceived) * 100) : 0;
    
    // Update stats display
    document.getElementById('li-stats').innerHTML = `
      <div class="li-stat-card"><div class="val" style="color:var(--accent)">${connectionsSent}</div><div class="lbl">Connections Sent</div></div>
      <div class="li-stat-card"><div class="val" style="color:var(--success)">${connectionsAccepted}</div><div class="lbl">Accepted</div></div>
      <div class="li-stat-card"><div class="val" style="color:#5b8def">${acceptanceRate}%</div><div class="lbl">Accept Rate</div></div>
      <div class="li-stat-card"><div class="val" style="color:var(--warning)">${dmsSent}</div><div class="lbl">DMs Sent</div></div>
      <div class="li-stat-card"><div class="val" style="color:var(--success)">${repliesReceived}</div><div class="lbl">Replies</div></div>
      <div class="li-stat-card"><div class="val" style="color:#5b8def">${replyRate}%</div><div class="lbl">Reply Rate</div></div>
      <div class="li-stat-card"><div class="val" style="color:var(--accent)">${meetingsBooked}</div><div class="lbl">Meetings</div></div>
      <div class="li-stat-card"><div class="val" style="color:var(--success)">${meetingRate}%</div><div class="lbl">Meeting Rate</div></div>
    `;
    
    // Render activities table
    const tbody = acts.map(a => `
      <tr>
        <td>${a.lead_name || 'N/A'}</td>
        <td>${a.company || 'N/A'}</td>
        <td><span class="badge badge-${a.activity_type.replace('_', '-')}">${a.activity_type.replace('_', ' ')}</span></td>
        <td>${a.notes || ''}</td>
        <td>${new Date(a.created_at).toLocaleDateString()}</td>
        <td><button class="btn-danger btn-sm" onclick="deleteLinkedInActivity(${a.id})">Delete</button></td>
      </tr>
    `).join('');
    
    document.getElementById('li-table').innerHTML = `
      <table>
        <thead><tr><th>Name</th><th>Company</th><th>Activity</th><th>Notes</th><th>Date</th><th>Actions</th></tr></thead>
        <tbody>${tbody || '<tr><td colspan="6" style="text-align:center;color:var(--text-muted)">No activities yet</td></tr>'}</tbody>
      </table>
    `;
  } catch (err) {
    console.error('Error loading LinkedIn tracker:', err);
    document.getElementById('li-stats').innerHTML = '<div style="color:var(--danger)">Error loading LinkedIn data</div>';
  }
}
'''

# Replace loadLinkedInTracker function
content = re.sub(
    r'async function loadLinkedInTracker\(\) \{[^}]+\}',
    linkedin_analytics_fix,
    content,
    flags=re.DOTALL
)

# Add refresh button handler to clear cache
refresh_with_cache_clear = '''
function refreshDashboard() {
  console.log('🔄 Refreshing dashboard and clearing cache...');
  dataCache.clear();
  tabLoadedOnce = {
    'dashboard': false,
    'leads': false,
    'linkedin-tracker': false,
    'meetings': false,
    'analytics': false,
    'ai-agent': false
  };
  
  // Reload current tab
  if (currentActiveTab === 'dashboard') loadDashboard();
  else if (currentActiveTab === 'leads') loadLeads();
  else if (currentActiveTab === 'linkedin-tracker') loadLinkedInTracker();
  else if (currentActiveTab === 'meetings') loadMeetings();
  else if (currentActiveTab === 'analytics') loadAnalytics();
}
'''

# Replace refreshDashboard function
content = re.sub(
    r'function refreshDashboard\(\) \{[^}]+\}',
    refresh_with_cache_clear,
    content,
    flags=re.DOTALL
)

# Write the updated content
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added caching system and fixed LinkedIn analytics!")
print()
print("🎯 Changes made:")
print("  1. ✅ Data caching system (5-minute TTL)")
print("  2. ✅ Prevents unnecessary API calls on tab switches")
print("  3. ✅ Fixed LinkedIn analytics calculations")
print("  4. ✅ Refresh button clears cache")
print()
print("📊 How it works:")
print("  - First visit to a tab: Loads data from API")
print("  - Switching back: Uses cached data (no API call)")
print("  - Cache expires after 5 minutes")
print("  - Refresh button: Clears cache and reloads")
print()
print("🔧 LinkedIn Analytics:")
print("  - Now calculates from actual table data")
print("  - Acceptance Rate = Accepted / Sent")
print("  - Reply Rate = Replies / DMs Sent")
print("  - Meeting Rate = Meetings / Replies")

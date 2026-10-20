// Shared helpers for the mkubench site: the main leaderboard (current dataset)
// and the historical page (older dataset version) both load the same
// assets/data/leaderboard.json and filter it by dataset_version.

function fetchLeaderboard() {
  return fetch('assets/data/leaderboard.json').then(function(r) {
    if (!r.ok) throw new Error('leaderboard fetch failed: HTTP ' + r.status);
    return r.json();
  });
}

function escapeHtml(value) {
  return String(value == null ? '' : value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escapeAttr(value) {
  return escapeHtml(value);
}

function pct(value) {
  return (value == null ? '-' : Number(value).toFixed(1) + '%');
}

function providerName(provider) {
  var names = {
    'kilocode': 'KiloCode API',
    'google-ai-studio': 'Google AI Studio',
    'nvidia-nim': 'NVIDIA NIM',
    'hosten': 'Hosten Gateway'
  };
  return names[provider] || provider;
}

function providerLabel(provider) {
  return providerName(provider).toLowerCase().replace(/[^a-z]/g, '');
}

// Provider column: for models reached through the Hosten gateway (which carry an
// "author" field) show the model author; otherwise show the access path name.
function entryProviderLabel(entry) {
  return entry.author || providerName(entry.provider);
}

// Badge colour follows the author when there is one, so the four Hosten
// authors are distinguishable instead of every row sharing the gateway colour.
// Access paths keep their own key ("nvidia-nim"), so the CSS class matches.
function providerBadgeClass(entry) {
  var key = entry.author ? String(entry.author) : String(entry.provider || '');
  // Access-path keys keep their hyphen ("nvidia-nim") so they match the CSS
  // class; author names are slugged without punctuation ("Mistral AI").
  var cls = key.toLowerCase().replace(/[^a-z0-9-]/g, '');
  return cls ? 'provider-' + cls : 'provider-unknown';
}

function statusLabel(status) {
  var labels = { complete: 'Complete', partial: 'Partial', failed: 'Failed' };
  return labels[status] || status;
}

/* ------------------------------------------------------------------ */
/* Search (works on several tables at once)                             */
/* ------------------------------------------------------------------ */

function setupSearch(tableIds) {
  var input = document.getElementById('model-search');
  if (!input) return;
  var tables = tableIds.map(function(id) {
    return document.getElementById(id);
  }).filter(Boolean);
  input.addEventListener('input', function() {
    var query = input.value.toLowerCase().trim();
    tables.forEach(function(table) {
      table.querySelectorAll('tbody tr').forEach(function(row) {
        row.style.display =
          query === '' || row.textContent.toLowerCase().indexOf(query) !== -1
            ? ''
            : 'none';
      });
    });
  });
}

/* ------------------------------------------------------------------ */
/* Theme toggle                                                        */
/* ------------------------------------------------------------------ */

function setupThemeToggle() {
  var toggle = document.getElementById('theme-toggle');
  if (!toggle) return;

  var saved = null;
  try { saved = localStorage.getItem('theme'); } catch (e) { saved = null; }
  applyTheme(saved || 'dark');

  toggle.addEventListener('click', function() {
    var current = document.documentElement.getAttribute('data-theme') || 'dark';
    applyTheme(current === 'dark' ? 'light' : 'dark');
  });
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  try { localStorage.setItem('theme', theme); } catch (e) { /* private mode */ }
  var toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
  }
}

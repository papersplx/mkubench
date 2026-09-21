// mkubench.github.io main script
// Includes: async leaderboard loading, tabbed navigation, model search/filter,
// column sorting, histogram, provider breakdown, and light/dark theme toggle.

document.addEventListener('DOMContentLoaded', function() {
  loadLeaderboard();
  setupTabs();
  setupSearch();
  setupSort();
  setupThemeToggle();
});

/* ------------------------------------------------------------------ */
/* Tabs                                                               */
/* ------------------------------------------------------------------ */

function setupTabs() {
  var tabs = document.querySelectorAll('.tab');
  tabs.forEach(function(tab) {
    tab.addEventListener('click', function() {
      var tabId = this.getAttribute('data-tab');
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    });
  });
}

/* ------------------------------------------------------------------ */
/* Search & Filter                                                    */
/* ------------------------------------------------------------------ */

function setupSearch() {
  var input = document.getElementById('model-search');
  if (!input) return;
  input.addEventListener('input', function() {
    var query = input.value.toLowerCase().trim();
    var rows = document.querySelectorAll('#leaderboard-table tbody tr');
    rows.forEach(function(row) {
      var text = row.textContent.toLowerCase();
      row.style.display = query === '' || text.indexOf(query) !== -1 ? '' : 'none';
    });
  });
}

/* ------------------------------------------------------------------ */
/* Sorting                                                            */
/* ------------------------------------------------------------------ */

var currentSort = { col: null, dir: 'asc' };

function setupSort() {
  var headers = document.querySelectorAll('#leaderboard-table th[data-sort]');
  headers.forEach(function(th) {
    th.style.cursor = 'pointer';
    th.addEventListener('click', function() {
      var col = th.getAttribute('data-sort');
      var dir = currentSort.col === col ? (currentSort.dir === 'asc' ? 'desc' : 'asc') : 'asc';
      currentSort = { col: col, dir: dir };
      sortTable(col, dir);
      updateSortIndicators();
    });
  });
}

function sortTable(col, dir) {
  var tbody = document.querySelector('#leaderboard-table tbody');
  var rows = Array.from(tbody.querySelectorAll('tr'));
  var type = 'number';
  if (col === 'model' || col === 'provider') type = 'string';

  rows.sort(function(a, b) {
    var va = getCellValue(a, col);
    var vb = getCellValue(b, col);
    var cmp;
    if (type === 'number') {
      cmp = parseFloat(va) - parseFloat(vb);
    } else {
      cmp = va.localeCompare(vb);
    }
    return dir === 'desc' ? -cmp : cmp;
  });

  rows.forEach(function(row) { tbody.appendChild(row); });
}

function getCellValue(row, col) {
  var idx = Array.from(row.parentNode.parentNode.querySelectorAll('th')).findIndex(
    th => th.getAttribute('data-sort') === col
  );
  var cell = row.children[idx + 1]; // +1 because rank is the first visible column
  if (!cell) return '';
  return cell.textContent.trim();
}

function updateSortIndicators() {
  var headers = document.querySelectorAll('#leaderboard-table th[data-sort]');
  headers.forEach(function(th) {
    var col = th.getAttribute('data-sort');
    var arrow = col === currentSort.col ? (currentSort.dir === 'asc' ? ' ↑' : ' ↓') : '';
    th.textContent = th.textContent.replace(/ ↑| ↓/, '') + arrow;
  });
}

/* ------------------------------------------------------------------ */
/* Leaderboard Loading                                                */
/* ------------------------------------------------------------------ */

async function loadLeaderboard() {
  try {
    const response = await fetch('assets/data/leaderboard.json');
    const data = await response.json();
    renderSummary(data.summary);
    renderLeaderboard(data.leaderboard);
    renderHistogram(data.leaderboard);
    renderProviderBreakdown(data.leaderboard);
  } catch (e) {
    console.error('Failed to load leaderboard:', e);
  }
}

function renderSummary(summary) {
  document.getElementById('total-models').textContent = summary.total_models_tested;
  document.getElementById('complete-models').textContent = summary.models_with_complete_results;
  document.getElementById('avg-weighted').textContent = summary.average_weighted_accuracy + '%';
  document.getElementById('avg-overall').textContent = summary.average_overall_accuracy + '%';
  document.getElementById('avg-ug').textContent = summary.average_user_generated_accuracy + '%';
  document.getElementById('avg-original').textContent = summary.average_original_accuracy + '%';
  document.getElementById('best-model').textContent = summary.best_model;
  document.getElementById('best-score').textContent = summary.best_weighted_accuracy + '%';
}

function providerName(provider) {
  const names = {
    'kilocode': 'KiloCode API',
    'google-ai-studio': 'Google AI Studio',
    'nvidia-nim': 'NVIDIA NIM'
  };
  return names[provider] || provider;
}

function providerLabel(provider) {
  return providerName(provider).toLowerCase().replace(/[^a-z]/g, '');
}

function renderLeaderboard(entries) {
  const tbody = document.querySelector('#leaderboard-table tbody');
  tbody.innerHTML = '';

  const ranked = entries
    .filter(e => e.status !== 'failed')
    .sort((a, b) => a.rank - b.rank);

  ranked.forEach(entry => {
    const row = document.createElement('tr');
    row.className = 'rank-' + Math.min(entry.rank, 3);

    const badgeClass = entry.rank <= 3 ? 'rank-badge' : '';
    const rankHtml = entry.rank <= 3
      ? '<span class="rank-badge">' + entry.rank + '</span>'
      : '<span class="rank-badge" style="background:var(--border);color:var(--muted);">' + entry.rank + '</span>';

    row.innerHTML =
      '<td>' + rankHtml + '</td>' +
      '<td>' + entry.model + '</td>' +
      '<td><span class="provider-badge provider-' + providerLabel(entry.provider) + '">' + providerName(entry.provider) + '</span></td>' +
      '<td><strong>' + entry.weighted_accuracy.toFixed(1) + '%</strong></td>' +
      '<td>' + entry.overall_accuracy.toFixed(1) + '%</td>' +
      '<td>' + entry.user_generated_accuracy.toFixed(1) + '%</td>' +
      '<td>' + entry.original_accuracy.toFixed(1) + '%</td>';
    tbody.appendChild(row);
  });
}

function renderHistogram(entries) {
  const container = document.getElementById('histogram-bars');
  container.innerHTML = '';

  const ranked = entries
    .filter(e => e.status !== 'failed')
    .sort((a, b) => b.weighted_accuracy - a.weighted_accuracy);

  ranked.forEach(entry => {
    const barClass = entry.weighted_accuracy >= 60 ? 'bar-excellent'
      : entry.weighted_accuracy >= 40 ? 'bar-good'
      : entry.weighted_accuracy >= 20 ? 'bar-moderate'
      : 'bar-poor';

    const displayName = entry.model.replace(/.*\//, '').replace(/:free$/, '');

    const bar = document.createElement('div');
    bar.className = 'histogram-bar';
    bar.innerHTML =
      '<div class="label" style="width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:0.82rem;color:var(--text);">' + displayName + '</div>' +
      '<div class="bar-container" style="flex:1;background:var(--code-bg);border-radius:4px;height:1.2rem;position:relative;">' +
        '<div class="bar-fill ' + barClass + '" style="width:' + entry.weighted_accuracy + '%;height:100%;border-radius:4px;transition:width 0.6s ease;"></div>' +
        '<span class="value" style="position:absolute;right:8px;top:50%;transform:translateY(-50%);font-size:0.78rem;font-weight:600;color:var(--heading);">' + entry.weighted_accuracy.toFixed(1) + '%</span>' +
      '</div>';
    container.appendChild(bar);
  });
}

function renderProviderBreakdown(entries) {
  const container = document.getElementById('provider-breakdown');
  container.innerHTML = '';

  const providers = {};
  entries.filter(e => e.status !== 'failed').forEach(entry => {
    if (!providers[entry.provider]) {
      providers[entry.provider] = [];
    }
    providers[entry.provider].push(entry);
  });

  for (const [provider, models] of Object.entries(providers)) {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML =
      '<h3>' + providerName(provider) + ' (' + models.length + ' models)</h3>' +
      '<table><thead><tr><th>Model</th><th>Weighted</th><th>Overall</th><th>Q31-Q40</th><th>Q1-Q30</th></tr></thead><tbody></tbody></table>';
    const tbody = card.querySelector('tbody');
    models.sort((a, b) => b.weighted_accuracy - a.weighted_accuracy).forEach(m => {
      const row = document.createElement('tr');
      row.innerHTML =
        '<td>' + m.model + '</td>' +
        '<td>' + m.weighted_accuracy.toFixed(1) + '%</td>' +
        '<td>' + m.overall_accuracy.toFixed(1) + '%</td>' +
        '<td>' + m.user_generated_accuracy.toFixed(1) + '%</td>' +
        '<td>' + m.original_accuracy.toFixed(1) + '%</td>';
      tbody.appendChild(row);
    });
    container.appendChild(card);
  }
}

/* ------------------------------------------------------------------ */
/* Theme Toggle                                                       */
/* ------------------------------------------------------------------ */

function setupThemeToggle() {
  var toggle = document.getElementById('theme-toggle');
  if (!toggle) return;

  // Check for saved preference
  var saved = localStorage.getItem('theme');
  if (saved) {
    applyTheme(saved);
  } else {
    applyTheme('dark');
  }

  toggle.addEventListener('click', function() {
    var current = document.documentElement.getAttribute('data-theme') || 'dark';
    var next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
  });
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
  var toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
  }
}

// mkubench.github.io main script - CURRENT dataset leaderboard.
//
// Only rows scored on the current dataset version are shown here. Rows from an
// older dataset version are not comparable (the question set changed), so they
// are filtered out of every view and live on the historical page instead.

document.addEventListener('DOMContentLoaded', function() {
  loadLeaderboard();
  setupTabs();
  setupSearch(['leaderboard-table']);
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
      document.querySelectorAll('.tab').forEach(function(t) {
        t.classList.remove('active');
      });
      document.querySelectorAll('.tab-content').forEach(function(c) {
        c.classList.remove('active');
      });
      this.classList.add('active');
      document.getElementById(tabId).classList.add('active');
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
      var dir = currentSort.col === col
        ? (currentSort.dir === 'asc' ? 'desc' : 'asc')
        : 'asc';
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
    var cmp = type === 'number'
      ? parseFloat(va) - parseFloat(vb)
      : va.localeCompare(vb);
    return dir === 'desc' ? -cmp : cmp;
  });

  rows.forEach(function(row) { tbody.appendChild(row); });
}

function getCellValue(row, col) {
  var idx = Array.from(row.parentNode.parentNode.querySelectorAll('th')).findIndex(
    function(th) { return th.getAttribute('data-sort') === col; }
  );
  var cell = row.children[idx + 1]; // +1 because rank is the first column
  if (!cell) return '';
  // Cells can carry an explicit sort value when the visible text is not the
  // value being compared (e.g. a model name with a route label underneath).
  var explicit = cell.getAttribute('data-sort-value');
  if (explicit != null) return explicit;
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
/* Data                                                               */
/* ------------------------------------------------------------------ */

async function loadLeaderboard() {
  try {
    var data = await fetchLeaderboard();
    var currentVersion = data.summary.dataset_version || '2.0';
    var breakdown = data.summary.version_breakdown || {};
    var current = breakdown[currentVersion] || {};

    renderSummary(current, currentVersion, breakdown);
    renderHistoricalLink(breakdown, currentVersion);

    // Only the current dataset version, and only rows that produced a score.
    var entries = data.leaderboard.filter(function(e) {
      return e.dataset_version === currentVersion && e.status !== 'failed';
    });

    renderLeaderboard(entries);
    renderHistogram(entries);
    renderProviderBreakdown(entries);
    renderBlocked(data.dataset_versions && data.dataset_versions.not_rerun_hosten_endpoints);
  } catch (e) {
    console.error('Failed to load leaderboard:', e);
    var body = document.querySelector('#leaderboard-table tbody');
    if (body) {
      body.innerHTML = '<tr><td colspan="6" class="reason">Could not load leaderboard data.</td></tr>';
    }
  }
}

function renderSummary(current, currentVersion, breakdown) {
  var set = function(id, value) {
    var el = document.getElementById(id);
    if (el) el.textContent = value;
  };

  set('scored-models', current.hosten_endpoints_scored != null ? current.hosten_endpoints_scored : '-');
  set('attempted-models', current.hosten_endpoints_attempted != null ? current.hosten_endpoints_attempted : '-');
  set('blocked-models', current.hosten_endpoints_blocked != null ? current.hosten_endpoints_blocked : '-');
  set('best-score', current.best_weighted_accuracy != null ? pct(current.best_weighted_accuracy) : '-');
  set('avg-weighted', pct(current.average_weighted_accuracy));
  set('avg-overall', pct(current.average_overall_accuracy));
  set('avg-ug', pct(current.average_user_generated_accuracy));
  set('avg-original', pct(current.average_original_accuracy));
  set('best-model', current.best_model || '-');

  var chip = document.getElementById('version-chip');
  if (chip) chip.textContent = 'Dataset v' + currentVersion;

  var sub = document.getElementById('leaderboard-version');
  if (sub) sub.textContent = 'dataset v' + currentVersion;
}

function renderHistoricalLink(breakdown, currentVersion) {
  var link = document.getElementById('historical-link');
  if (!link) return;
  var otherVersion = null;
  Object.keys(breakdown).forEach(function(version) {
    if (version !== currentVersion) otherVersion = version;
  });
  if (!otherVersion) return;
  var other = breakdown[otherVersion];
  var count = other.models_tested != null ? other.models_tested : 0;
  link.textContent = 'Historical results (v' + otherVersion + ') - ' + count + ' entries';
}

/* ------------------------------------------------------------------ */
/* Rendering                                                           */
/* ------------------------------------------------------------------ */

function renderLeaderboard(entries) {
  var tbody = document.querySelector('#leaderboard-table tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  // Rank inside the current dataset version, not the mixed global rank.
  var ranked = entries.slice().sort(function(a, b) {
    return b.weighted_accuracy - a.weighted_accuracy ||
      a.model.localeCompare(b.model);
  });

  ranked.forEach(function(entry, i) {
    var rank = i + 1;
    var row = document.createElement('tr');
    row.className = 'rank-' + Math.min(rank, 3);

    var badgeClass = rank <= 3 ? 'rank-badge' : 'rank-badge muted';

    row.innerHTML =
      '<td><span class="' + badgeClass + '">' + rank + '</span></td>' +
      '<td data-sort-value="' + escapeAttr(entry.model) + '">' + escapeHtml(entry.model) +
        (entry.endpoint_id ? '<span class="model-sub">hosten/' + escapeHtml(entry.endpoint_id) + '</span>' : '') +
      '</td>' +
      '<td><span class="provider-badge ' + providerBadgeClass(entry) + '">' +
        escapeHtml(entryProviderLabel(entry)) + '</span></td>' +
      '<td class="num"><strong>' + pct(entry.weighted_accuracy) + '</strong></td>' +
      '<td class="num">' + pct(entry.user_generated_accuracy) + '</td>' +
      '<td class="num">' + pct(entry.original_accuracy) + '</td>';
    tbody.appendChild(row);
  });
}

function renderHistogram(entries) {
  var container = document.getElementById('histogram-bars');
  if (!container) return;
  container.innerHTML = '';

  var ranked = entries.slice().sort(function(a, b) {
    return b.weighted_accuracy - a.weighted_accuracy;
  });

  ranked.forEach(function(entry) {
    var barClass = entry.weighted_accuracy >= 60 ? 'bar-excellent'
      : entry.weighted_accuracy >= 40 ? 'bar-good'
      : entry.weighted_accuracy >= 20 ? 'bar-moderate'
      : 'bar-poor';

    var displayName = entry.model.replace(/.*\//, '').replace(/:free$/, '');

    var bar = document.createElement('div');
    bar.className = 'histogram-bar';
    bar.innerHTML =
      '<div class="label">' + escapeHtml(displayName) + '</div>' +
      '<div class="bar-container">' +
        '<div class="bar-fill ' + barClass + '" style="width:' + entry.weighted_accuracy + '%;height:100%;border-radius:4px;transition:width 0.6s ease;"></div>' +
        '<span class="value">' + pct(entry.weighted_accuracy) + '</span>' +
      '</div>';
    container.appendChild(bar);
  });
}

function renderProviderBreakdown(entries) {
  var container = document.getElementById('provider-breakdown');
  if (!container) return;
  container.innerHTML = '';

  var providers = {};
  entries.forEach(function(entry) {
    // Hosten models are grouped by author, external runs by access path.
    var key = entry.author || entry.provider;
    if (!providers[key]) providers[key] = [];
    providers[key].push(entry);
  });

  Object.keys(providers).forEach(function(provider) {
    var models = providers[provider];
    var card = document.createElement('div');
    card.className = 'card';
    var title = entryProviderLabel(models[0]) || provider;
    card.innerHTML =
      '<h3>' + escapeHtml(title) + ' (' + models.length +
        (models.length === 1 ? ' model' : ' models') + ')</h3>' +
      '<table><thead><tr><th>Model</th><th class="num">Weighted</th>' +
        '<th class="num">Q31-Q40</th><th class="num">Q1-Q30</th></tr></thead><tbody></tbody></table>';
    var tbody = card.querySelector('tbody');
    models.sort(function(a, b) {
      return b.weighted_accuracy - a.weighted_accuracy;
    }).forEach(function(m) {
      var row = document.createElement('tr');
      row.innerHTML =
        '<td>' + escapeHtml(m.model) + '</td>' +
        '<td class="num">' + pct(m.weighted_accuracy) + '</td>' +
        '<td class="num">' + pct(m.user_generated_accuracy) + '</td>' +
        '<td class="num">' + pct(m.original_accuracy) + '</td>';
      tbody.appendChild(row);
    });
    container.appendChild(card);
  });
}

// Endpoints whose site refused to answer the automated re-run: they keep their
// v1.0 score, which is shown here as history only.
function renderBlocked(detail) {
  var tbody = document.querySelector('#blocked-table tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  var ids = Object.keys(detail || {}).sort();
  if (!ids.length) {
    tbody.innerHTML = '<tr><td colspan="4" class="reason">Every endpoint was re-run.</td></tr>';
    return;
  }

  ids.forEach(function(id) {
    var d = detail[id];
    var row = document.createElement('tr');
    row.innerHTML =
      '<td><code>' + escapeHtml(id) + '</code></td>' +
      '<td>' + escapeHtml(d.model || '-') + '</td>' +
      '<td class="num">' + (d.v1_weighted_accuracy != null ? pct(d.v1_weighted_accuracy) : '-') + '</td>' +
      '<td class="reason">' + escapeHtml(d.reason || 'not re-run') + '</td>';
    tbody.appendChild(row);
  });
}

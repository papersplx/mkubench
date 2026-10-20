// mkubench.github.io - historical leaderboard (dataset v1.0).
//
// Every row here was scored on v1.0. The current dataset version has its own
// page (index.html) because the two sets are not comparable whenever the
// question set changed in between.

document.addEventListener('DOMContentLoaded', function() {
  loadHistorical();
  setupSearch(['historical-table', 'failed-table']);
  setupThemeToggle();
});

async function loadHistorical() {
  try {
    var data = await fetchLeaderboard();
    var currentVersion = data.summary.dataset_version || '2.0';
    var breakdown = data.summary.version_breakdown || {};
    var hist = null;
    Object.keys(breakdown).forEach(function(version) {
      if (version !== currentVersion) hist = breakdown[version];
    });
    var v1 = data.leaderboard.filter(function(e) {
      return e.dataset_version !== currentVersion;
    });

    var ranked = v1.filter(function(e) {
      return e.status !== 'failed';
    }).sort(function(a, b) {
      return b.weighted_accuracy - a.weighted_accuracy ||
        a.model.localeCompare(b.model);
    });

    renderSummary(hist, currentVersion, ranked);
    renderLeaderboard(ranked);
    renderFailed(v1.filter(function(e) {
      return e.status === 'failed';
    }).sort(function(a, b) {
      return a.model.localeCompare(b.model);
    }));
  } catch (e) {
    console.error('Failed to load historical leaderboard:', e);
  }
}

function renderSummary(hist, currentVersion, entries) {
  var set = function(id, value) {
    var el = document.getElementById(id);
    if (el) el.textContent = value;
  };

  if (!hist) return;
  set('hist-tested', hist.models_tested);
  set('hist-complete', hist.models_complete);
  set('hist-partial', hist.models_partial);
  set('hist-failed', hist.models_failed);
  set('hist-best-score', hist.best_weighted_accuracy != null ? pct(hist.best_weighted_accuracy) : '-');
  set('hist-best-model', hist.best_model || '-');

  var complete = (entries || []).filter(function(e) {
    return e.status === 'complete';
  });
  var avg = function(key) {
    if (!complete.length) return '-';
    var sum = complete.reduce(function(acc, e) { return acc + (e[key] || 0); }, 0);
    return pct(sum / complete.length);
  };
  set('hist-avg-weighted', avg('weighted_accuracy'));
  set('hist-avg-overall', avg('overall_accuracy'));
}

function renderLeaderboard(entries) {
  var tbody = document.querySelector('#historical-table tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  entries.forEach(function(entry, i) {
    var rank = i + 1;
    var row = document.createElement('tr');
    row.className = 'rank-' + Math.min(rank, 3);

    var badgeClass = rank <= 3 ? 'rank-badge' : 'rank-badge muted';
    var route = entry.endpoint_id ? 'hosten/' + entry.endpoint_id : providerName(entry.provider);
    var note = '';
    if (entry.v1_only) note = ' (carried over &mdash; v2.0 re-run blocked)';

    row.innerHTML =
      '<td><span class="' + badgeClass + '">' + rank + '</span></td>' +
      '<td data-sort-value="' + escapeAttr(entry.model) + '">' + escapeHtml(entry.model) +
        '<span class="model-sub">' + escapeHtml(route) + note + '</span></td>' +
      '<td><span class="provider-badge ' + providerBadgeClass(entry) + '">' +
        escapeHtml(entryProviderLabel(entry)) + '</span></td>' +
      '<td class="num"><strong>' + pct(entry.weighted_accuracy) + '</strong></td>' +
      '<td class="num">' + pct(entry.user_generated_accuracy) + '</td>' +
      '<td class="num">' + pct(entry.original_accuracy) + '</td>' +
      '<td class="status-' + escapeHtml(entry.status) + '">' + escapeHtml(statusLabel(entry.status)) + '</td>';
    tbody.appendChild(row);
  });
}

function renderFailed(entries) {
  var tbody = document.querySelector('#failed-table tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  entries.forEach(function(entry) {
    var row = document.createElement('tr');
    var route = entry.endpoint_id ? 'hosten/' + entry.endpoint_id : providerName(entry.provider);
    row.innerHTML =
      '<td>' + escapeHtml(entry.model) +
        '<span class="model-sub">' + escapeHtml(route) + '</span></td>' +
      '<td><span class="provider-badge ' + providerBadgeClass(entry) + '">' +
        escapeHtml(entryProviderLabel(entry)) + '</span></td>' +
      '<td class="num">' + pct(entry.weighted_accuracy) + '</td>' +
      '<td class="status-' + escapeHtml(entry.status) + '">' + escapeHtml(statusLabel(entry.status)) + '</td>';
    tbody.appendChild(row);
  });
}

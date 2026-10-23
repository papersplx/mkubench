// mkubench.github.io - endpoints that were NOT re-run on dataset v2.0.
//
// The v2.0 leaderboard page lists the runs that produced a score. The
// endpoints whose site refused the automated run are kept off that page and
// listed here instead, each with the reason recorded at fill time, so the
// leaderboard itself stays a clean "what was actually scored" view.

document.addEventListener('DOMContentLoaded', function() {
  loadNotRerun();
  setupThemeToggle();
});

async function loadNotRerun() {
  try {
    var data = await fetchLeaderboard();
    renderNotRerun(
      data.dataset_versions && data.dataset_versions.not_rerun_hosten_endpoints,
      data.dataset_versions && data.dataset_versions.not_rerun_external_models
    );
  } catch (e) {
    console.error('Failed to load the not-re-run list:', e);
  }
}

// Hosten endpoints whose site refused to answer the automated re-run, and
// external models the provider no longer serves: they keep their v1.0 score,
// which is shown here as history only.
function renderNotRerun(detail, external) {
  var tbody = document.querySelector('#blocked-table tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  var rows = [];
  Object.keys(detail || {}).sort().forEach(function(id) {
    var d = detail[id];
    rows.push({
      endpoint: id,
      model: d.model || '-',
      v1: d.v1_weighted_accuracy
    });
  });
  (external || []).forEach(function(d) {
    rows.push({
      endpoint: d.provider || d.endpoint || d.model,
      model: d.model || '-',
      v1: d.v1_weighted_accuracy
    });
  });

  if (!rows.length) {
    tbody.innerHTML = '<tr><td colspan="3" class="reason">Every endpoint was re-run.</td></tr>';
    return;
  }

  rows.forEach(function(d) {
    var row = document.createElement('tr');
    row.innerHTML =
      '<td><code>' + escapeHtml(d.endpoint) + '</code></td>' +
      '<td>' + escapeHtml(d.model) + '</td>' +
      '<td class="num">' + (d.v1 != null ? pct(d.v1) : '-') + '</td>';
    tbody.appendChild(row);
  });
}

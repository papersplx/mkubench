// mkubench.github.io main script

document.addEventListener('DOMContentLoaded', function() {
  loadLeaderboard();
  setupTabs();
});

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
  
  // Filter to show complete/partial models, sorted by rank
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
        '<div class="bar-fill ' + barClass + '" style="width:' + (entry.weighted_accuracy / 100 * 100) + '%;height:100%;border-radius:4px;transition:width 0.6s ease;"></div>' +
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

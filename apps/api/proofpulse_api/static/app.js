document.addEventListener('DOMContentLoaded', () => {
  const btnSeed = document.getElementById('btn-seed');
  
  // DOM selectors for updates
  const lblTargetName = document.getElementById('lbl-target-name');
  const lblTargetId = document.getElementById('lbl-target-id');
  const lblRiskScore = document.getElementById('lbl-risk-score');
  const lblIncidentSummary = document.getElementById('lbl-incident-summary');
  const lblIncidentCause = document.getElementById('lbl-incident-cause');
  const lblBundleId = document.getElementById('lbl-bundle-id');
  const lblBundleHash = document.getElementById('lbl-bundle-hash');
  const lblAttestationStatus = document.getElementById('lbl-attestation-status');
  const lblAttestationCalldata = document.getElementById('lbl-attestation-calldata');
  const lstRecommendedActions = document.getElementById('lst-recommended-actions');
  const statusDot = document.getElementById('status-dot');
  const statusLabel = document.getElementById('status-label');
  const statusCard = document.querySelector('.status-card');

  // Load latest state on load
  fetchLatestState();

  // Button handler
  btnSeed.addEventListener('click', async () => {
    btnSeed.disabled = true;
    btnSeed.textContent = 'Generating...';
    try {
      const severityOption = Math.random() > 0.5 ? 'critical' : 'high';
      const response = await fetch(`/demo/seed?force_severity=${severityOption}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }
      const data = await response.json();
      updateDashboard(data);
    } catch (err) {
      console.error('Failed to seed demo incident:', err);
      alert('Error seeding demo incident. Check console/logs.');
    } finally {
      btnSeed.disabled = false;
      btnSeed.innerHTML = '<span class="icon-zap"></span> Generate Demo Incident';
    }
  });

  async function fetchLatestState() {
    try {
      const response = await fetch('/demo/latest');
      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }
      const data = await response.json();
      if (data) {
        updateDashboard(data);
      }
    } catch (err) {
      console.error('Failed to load latest state:', err);
    }
  }

  function updateDashboard(data) {
    if (!data || !data.target || !data.incident || !data.bundle || !data.attestation) {
      return;
    }

    // Extract variables
    const target = data.target;
    const incident = data.incident;
    const bundle = data.bundle;
    const attestation = data.attestation;

    // 1. Text elements
    lblTargetName.textContent = target.name || 'EU RPC + RWA Oracle Cluster';
    lblTargetId.textContent = target.id || '—';
    lblRiskScore.textContent = incident.risk_score !== undefined ? incident.risk_score : '100';
    
    // Color risk score based on value
    if (incident.risk_score >= 75) {
      lblRiskScore.className = 'value score-value text-red';
    } else if (incident.risk_score >= 45) {
      lblRiskScore.className = 'value score-value';
      lblRiskScore.style.color = 'var(--warning-color)';
    } else {
      lblRiskScore.className = 'value score-value';
      lblRiskScore.style.color = 'var(--success-color)';
    }

    lblIncidentSummary.textContent = incident.summary || '—';
    lblIncidentCause.textContent = incident.likely_cause || '—';
    
    // 2. Evidence Bundle & Attestation
    lblBundleId.textContent = bundle.bundle_id || '—';
    lblBundleHash.textContent = bundle.bundle_hash || '—';
    
    lblAttestationStatus.textContent = attestation.status ? formatStatus(attestation.status) : 'Prepared';
    lblAttestationStatus.classList.add('active');
    
    // Calldata preview bundleHash
    if (attestation.calldata_preview && attestation.calldata_preview.bundleHash) {
      lblAttestationCalldata.textContent = attestation.calldata_preview.bundleHash;
    } else {
      lblAttestationCalldata.textContent = '0x' + (bundle.bundle_hash || '');
    }

    // 3. Status label & indicator updates
    statusLabel.textContent = 'Incident Detected';
    statusLabel.style.color = 'var(--error-color)';
    statusCard.classList.add('incident-active');

    // 4. Recommended Actions
    lstRecommendedActions.innerHTML = '';
    const actions = incident.recommended_actions || [];
    if (actions.length === 0) {
      lstRecommendedActions.innerHTML = '<li class="placeholder-item">No actions prepared.</li>';
    } else {
      actions.forEach(action => {
        const li = document.createElement('li');
        li.textContent = action;
        lstRecommendedActions.appendChild(li);
      });
    }
  }

  function formatStatus(status) {
    return status.replace(/_/g, ' ').toUpperCase();
  }
});

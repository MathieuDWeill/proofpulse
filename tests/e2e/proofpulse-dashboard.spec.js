const { test, expect } = require('@playwright/test');

test.describe('ProofPulse dashboard demo', () => {
  test('health endpoint returns proofpulse-api', async ({ request }) => {
    const response = await request.get('/health');
    expect(response.ok()).toBeTruthy();

    const json = await response.json();
    expect(json.status).toBe('ok');
    expect(json.service).toContain('proofpulse');
  });

  test('dashboard loads and explains the product', async ({ page }) => {
    await page.goto('/');

    await expect(page).toHaveTitle(/ProofPulse/i);
    await expect(page.getByText(/ProofPulse/i).first()).toBeVisible();
    await expect(page.getByText(/Datadog/i).first()).toBeVisible();
    await expect(page.getByText(/AI SRE/i).first()).toBeVisible();

    // Depending on copy, the dashboard may say "on-chain proof",
    // "on-chain attestation", or "chain-ready attestation".
    await expect(
      page.getByText(/on-chain|chain-ready|attestation/i).first()
    ).toBeVisible();

    await expect(page.getByText(/AWS Activate|AWS/i).first()).toBeVisible();
  });

  test('Generate Demo Incident creates visible evidence and attestation', async ({ page }) => {
    await page.goto('/');

    const generateButton = page.getByRole('button', { name: /Generate Demo Incident/i });
    await expect(generateButton).toBeVisible();

    await generateButton.click();

    await expect(
      page.getByText('EU RPC + RWA Oracle Cluster', { exact: true })
    ).toBeVisible();

    await expect(page.getByText(/critical|high/i).first()).toBeVisible();
    await expect(page.getByText(/bundle/i).first()).toBeVisible();
    await expect(page.getByText(/attestation/i).first()).toBeVisible();

    await expect(page.getByText(/[a-f0-9]{64}/i).first()).toBeVisible();

    await expect(
      page.getByText(/prepared_not_broadcast|prepared|anchorEvidence/i).first()
    ).toBeVisible();
  });

  test('latest demo endpoint returns seeded state after click', async ({ page, request }) => {
    await page.goto('/');
    await page.getByRole('button', { name: /Generate Demo Incident/i }).click();

    const response = await request.get('/demo/latest');
    expect(response.ok()).toBeTruthy();

    const json = await response.json();
    expect(json).toBeTruthy();
    expect(json.bundle).toBeTruthy();
    expect(json.bundle.bundle_hash).toMatch(/^[a-f0-9]{64}$/);

    expect(json.attestation).toBeTruthy();
    expect(json.attestation.calldata_preview).toBeTruthy();
    expect(json.attestation.calldata_preview.bundleHash).toContain(json.bundle.bundle_hash);

    expect(json.incident).toBeTruthy();
    expect(['high', 'critical']).toContain(json.incident.severity);
    expect(json.incident.summary).toBeTruthy();
  });

  test('OpenAPI docs are reachable', async ({ page, request }) => {
    const openapi = await request.get('/openapi.json');
    expect(openapi.ok()).toBeTruthy();

    const spec = await openapi.json();
    expect(spec.openapi).toBeTruthy();

    await page.goto('/docs');

    // Swagger UI can render differently depending on assets/cache,
    // so test for durable OpenAPI/Swagger page signals.
    await expect(page.locator('body')).toContainText(/swagger|openapi|proofpulse|demo/i);
  });
});

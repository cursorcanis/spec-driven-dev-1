// Global Chart Configuration for Aesthetics
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Outfit', sans-serif";
Chart.defaults.scale.grid.color = 'rgba(255, 255, 255, 0.05)';

// Helper to format currency
const formatCurrency = (val) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumSignificantDigits: 3 }).format(val);
const formatNumber = (val) => new Intl.NumberFormat('en-US').format(val);

async function initDashboard() {
    try {
        // Fetch Real Data from backend API but catch individual errors so the whole dashboard doesn't crash
        const fetchSafe = async (url) => {
            try {
                const res = await fetch(url);
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return await res.json();
            } catch (e) {
                console.error(`Failed to fetch ${url}:`, e);
                return { error: true };
            }
        };

        const [censusData, cryptoData, apiData] = await Promise.all([
            fetchSafe('/api/census/demographics'),
            fetchSafe('/api/finance/crypto'),
            fetchSafe('/api/metrics/api-demand')
        ]);

        renderKPIs(censusData, cryptoData, apiData);
        if (!censusData.error) renderCensusChart(censusData);
        if (!cryptoData.error) renderCryptoChart(cryptoData);
        if (!apiData.error) renderApiDemandChart(apiData);

    } catch (err) {
        console.error("Dashboard initialization failed:", err);
    }
}

function renderKPIs(census, crypto, api) {
    // Population KPI updates
    if (census.datasets && census.datasets.population.length > 0) {
        const latestPop = census.datasets.population[census.datasets.population.length - 1];
        const latestGrowth = census.datasets.growth_pct[census.datasets.growth_pct.length - 1];

        document.getElementById('kpi-population').innerText = formatNumber(latestPop);
        const trendEl = document.getElementById('kpi-population-trend');
        trendEl.innerText = `${latestGrowth > 0 ? '↑' : '↓'} ${Math.abs(latestGrowth)}% YoY`;
        trendEl.className = latestGrowth > 0 ? 'kpi-trend positive' : 'kpi-trend negative';
    }

    // Crypto KPI
    if (crypto.metrics) {
        document.getElementById('kpi-marketcap').innerText = formatCurrency(crypto.metrics.total_market_cap_usd);
        document.getElementById('kpi-btc-dom').innerText = `BTC Dominance: ${crypto.metrics.btc_dominance_pct}%`;
    }

    // API KPI
    if (api.metrics) {
        document.getElementById('kpi-apis').innerText = formatNumber(api.metrics.total_apis);
        document.getElementById('kpi-endpoints').innerText = `Total Endpoints: ${formatNumber(api.metrics.total_endpoints)}`;
    }
}

function renderCensusChart(data) {
    const ctx = document.getElementById('censusChart').getContext('2d');

    // Create gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.5)'); // --accent-blue
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'US Population',
                data: data.datasets.population,
                borderColor: '#3b82f6',
                borderWidth: 3,
                backgroundColor: gradient,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#0b0f19',
                pointBorderColor: '#3b82f6',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(11, 15, 25, 0.9)',
                    titleColor: '#f8fafc',
                    bodyColor: '#94a3b8',
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    padding: 12
                }
            },
            scales: {
                y: { beginAtZero: false } // Population shouldn't start at 0
            }
        }
    });
}

function renderCryptoChart(data) {
    if (!data.metrics) return;

    const ctx = document.getElementById('cryptoChart').getContext('2d');

    // We'll show a pie chart of BTC dominance vs "Altcoins"
    const btcDom = data.metrics.btc_dominance_pct;
    const altcoins = 100 - btcDom;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Bitcoin', 'Altcoins'],
            datasets: [{
                data: [btcDom, altcoins],
                backgroundColor: [
                    '#f59e0b', // Bitcoin orange
                    '#8b5cf6'  // Accent purple
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#f8fafc', padding: 20, usePointStyle: true }
                }
            }
        }
    });
}

function renderApiDemandChart(data) {
    if (!data.metrics || !data.chart_data) return;

    const ctx = document.getElementById('apiDemandChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.chart_data.labels,
            datasets: [{
                label: 'Real API Endpoints Hosted (All-Time Snapshot)',
                data: data.chart_data.counts,
                backgroundColor: '#06b6d4', // Accent cyan
                borderColor: 'rgba(6, 182, 212, 0.5)',
                borderWidth: 1,
                borderRadius: 4,
                barPercentage: 0.6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(11, 15, 25, 0.9)',
                    titleColor: '#f8fafc',
                    bodyColor: '#94a3b8',
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    title: {
                        display: true,
                        text: 'Number of Public APIs Hosted',
                        color: '#94a3b8',
                        font: { size: 13 }
                    }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

// Initialize when DOM loads
document.addEventListener('DOMContentLoaded', initDashboard);

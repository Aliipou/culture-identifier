// API Configuration
const API_BASE_URL = 'http://localhost:8080/api';

// DOM Elements
const userTextArea = document.getElementById('userText');
const analyzeBtn = document.getElementById('analyzeBtn');
const wordCountSpan = document.getElementById('wordCount');
const charCountSpan = document.getElementById('charCount');
const topKSelect = document.getElementById('topK');
const loadingDiv = document.getElementById('loading');
const resultsDiv = document.getElementById('results');
const matchesContainer = document.getElementById('matchesContainer');
const processingTimeSpan = document.getElementById('processingTime');
const userSummaryDiv = document.getElementById('userSummary');

let projectionChart = null;

// Event Listeners
userTextArea.addEventListener('input', updateCounts);
analyzeBtn.addEventListener('click', analyzeText);

function updateCounts() {
    const text = userTextArea.value.trim();
    const words = text ? text.split(/\s+/).length : 0;
    const chars = text.length;

    wordCountSpan.textContent = `${words} words`;
    charCountSpan.textContent = `${chars} characters`;

    // Enable button if text is long enough
    analyzeBtn.disabled = chars < 50;
}

async function analyzeText() {
    const text = userTextArea.value.trim();
    const topK = parseInt(topKSelect.value);

    if (text.length < 50) {
        alert('Please write at least 50 characters for analysis.');
        return;
    }

    // Show loading, hide results
    loadingDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');
    analyzeBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                mode: 'detailed',
                top_k: topK
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        alert(`Analysis failed: ${error.message}`);
    } finally {
        loadingDiv.classList.add('hidden');
        analyzeBtn.disabled = false;
    }
}

function displayResults(data) {
    // Processing time
    processingTimeSpan.textContent = `${data.processing_time_ms.toFixed(0)}ms`;

    // Matches
    displayMatches(data.matches);

    // Projection chart
    if (data.projection && data.projection.length > 0) {
        displayProjection(data.projection);
    }

    // User summary
    displayUserSummary(data.user_embedding_summary);

    // Show results
    resultsDiv.classList.remove('hidden');
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function displayMatches(matches) {
    matchesContainer.innerHTML = '';

    matches.forEach((match, index) => {
        const matchCard = document.createElement('div');
        matchCard.className = 'bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow';

        const scorePercent = (match.score * 100).toFixed(1);
        const scoreColor = match.score > 0.75 ? 'text-green-600' : match.score > 0.60 ? 'text-blue-600' : 'text-indigo-600';

        matchCard.innerHTML = `
            <div class="flex items-start justify-between mb-4">
                <div class="flex-1">
                    <div class="flex items-center gap-3 mb-2">
                        <span class="text-3xl font-bold text-gray-300">#${index + 1}</span>
                        <h3 class="text-2xl font-bold text-gray-800">${match.name}</h3>
                    </div>
                    <div class="flex gap-2 mb-2">
                        <span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium">${match.category}</span>
                        <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">${match.period}</span>
                    </div>
                </div>
                <div class="text-right">
                    <div class="text-3xl font-bold ${scoreColor}">${scorePercent}%</div>
                    <div class="text-sm text-gray-500">Match</div>
                </div>
            </div>

            <p class="text-gray-700 mb-4 leading-relaxed">${match.reason}</p>

            ${match.key_themes && match.key_themes.length > 0 ? `
                <div class="mb-4">
                    <div class="text-sm font-semibold text-gray-600 mb-2">Key Themes:</div>
                    <div class="flex flex-wrap gap-2">
                        ${match.key_themes.map(theme => `
                            <span class="px-2 py-1 bg-gray-100 text-gray-600 rounded text-sm">${theme}</span>
                        `).join('')}
                    </div>
                </div>
            ` : ''}

            ${match.recommendation && match.recommendation.book ? `
                <div class="border-t pt-4 mt-4">
                    <div class="text-sm font-semibold text-gray-600 mb-1">Recommended Reading:</div>
                    <div class="text-lg font-medium text-indigo-600">
                        ${match.recommendation.book}
                        ${match.recommendation.year ? `<span class="text-gray-500 text-sm">(${match.recommendation.year})</span>` : ''}
                    </div>
                    ${match.recommendation.type ? `<div class="text-sm text-gray-500">${match.recommendation.type}</div>` : ''}
                </div>
            ` : ''}
        `;

        matchesContainer.appendChild(matchCard);
    });
}

function displayProjection(projectionData) {
    const ctx = document.getElementById('projectionChart').getContext('2d');

    // Destroy existing chart
    if (projectionChart) {
        projectionChart.destroy();
    }

    // Separate user point from others
    const userPoint = projectionData.find(p => p.label === 'You');
    const figurePoints = projectionData.filter(p => p.label !== 'You');

    const datasets = [
        {
            label: 'Cultural Figures',
            data: figurePoints.map(p => ({ x: p.x, y: p.y })),
            backgroundColor: 'rgba(99, 102, 241, 0.6)',
            borderColor: 'rgba(99, 102, 241, 1)',
            pointRadius: 6,
            pointHoverRadius: 8,
        }
    ];

    if (userPoint) {
        datasets.push({
            label: 'You',
            data: [{ x: userPoint.x, y: userPoint.y }],
            backgroundColor: 'rgba(239, 68, 68, 0.8)',
            borderColor: 'rgba(220, 38, 38, 1)',
            pointRadius: 10,
            pointHoverRadius: 12,
            borderWidth: 3,
        });
    }

    projectionChart = new Chart(ctx, {
        type: 'scatter',
        data: { datasets },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const point = projectionData[context.dataIndex];
                            return point ? point.label : '';
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Dimension 1'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Dimension 2'
                    }
                }
            }
        }
    });
}

function displayUserSummary(summary) {
    userSummaryDiv.innerHTML = '';

    if (!summary.features) return;

    const features = summary.features;

    const stats = [
        { label: 'Words', value: features.word_count },
        { label: 'Sentences', value: features.sentence_count },
        { label: 'Avg Sentence Length', value: features.avg_sentence_length.toFixed(1) + ' words' },
        { label: 'Avg Word Length', value: features.avg_word_length.toFixed(1) + ' chars' },
        { label: 'Question Density', value: (features.question_density * 100).toFixed(1) + '%' },
        { label: 'Complex Words', value: (features.complex_word_ratio * 100).toFixed(1) + '%' },
    ];

    stats.forEach(stat => {
        const statDiv = document.createElement('div');
        statDiv.className = 'bg-gray-50 rounded-lg p-4';
        statDiv.innerHTML = `
            <div class="text-sm text-gray-600 mb-1">${stat.label}</div>
            <div class="text-xl font-semibold text-gray-800">${stat.value}</div>
        `;
        userSummaryDiv.appendChild(statDiv);
    });

    // Add themes if available
    if (summary.themes && summary.themes.length > 0) {
        const themesDiv = document.createElement('div');
        themesDiv.className = 'col-span-2 md:col-span-3 bg-indigo-50 rounded-lg p-4';
        themesDiv.innerHTML = `
            <div class="text-sm text-gray-600 mb-2">Detected Themes:</div>
            <div class="flex flex-wrap gap-2">
                ${summary.themes.map(theme => `
                    <span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium">${theme}</span>
                `).join('')}
            </div>
        `;
        userSummaryDiv.appendChild(themesDiv);
    }
}

// Initialize
updateCounts();

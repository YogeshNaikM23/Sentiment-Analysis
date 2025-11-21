// Fake News Detection System - JavaScript Implementation

// Application Data
const appData = {
  systemMetrics: {
    totalAnalyzed: 15847,
    fakeDetected: 3924,
    realDetected: 11923,
    averageConfidence: 0.876,
    uptime: "99.9%",
    processingSpeed: "< 200ms"
  },
  sampleNews: [
    {
      id: 1,
      title: "Bangalore Metro Expansion Project Gets Government Approval",
      content: "The Karnataka government has approved the Phase 3 expansion of Bangalore Metro, which will add 150 km of new lines connecting outer areas to the city center. The project is expected to cost Rs 30,000 crore and will be completed by 2028.",
      source: "The Hindu",
      category: "Infrastructure", 
      timestamp: "2025-08-23T10:30:00Z",
      classification: "Real",
      confidence: 0.92,
      sentiment: "Positive",
      sentimentScore: 0.6,
      credibilityScore: 0.90,
      entities: ["Karnataka", "Bangalore Metro", "Government"],
      region: "Karnataka"
    },
    {
      id: 2,
      title: "SHOCKING: Mysore Palace Made of Pure Gold, Government Hides Truth",
      content: "Secret documents reveal that Mysore Palace is actually made of pure gold worth billions, but the government has been covering this up for decades. Local sources claim this is the biggest scandal in Karnataka history.",
      source: "Karnataka Conspiracy News",
      category: "Politics",
      timestamp: "2025-08-23T09:15:00Z", 
      classification: "Fake",
      confidence: 0.96,
      sentiment: "Negative",
      sentimentScore: -0.4,
      credibilityScore: 0.12,
      entities: ["Mysore Palace", "Government", "Karnataka"],
      region: "Karnataka"
    },
    {
      id: 3,
      title: "Indian Space Research Organisation Launches New Satellite",
      content: "ISRO successfully launched its latest communication satellite from Sriharikota, marking another milestone in India's space program. The satellite will improve telecommunications across rural India.",
      source: "Times of India",
      category: "Science",
      timestamp: "2025-08-23T08:45:00Z",
      classification: "Real", 
      confidence: 0.89,
      sentiment: "Positive",
      sentimentScore: 0.7,
      credibilityScore: 0.85,
      entities: ["ISRO", "India", "Satellite", "Sriharikota"],
      region: "India"
    },
    {
      id: 4,
      title: "Prime Minister Announces Free Gold for All Citizens",
      content: "In a surprise announcement, the Prime Minister declared that every Indian citizen will receive 1kg of free gold from the government treasury. Distribution to start next week across all states.",
      source: "Fake News India",
      category: "Politics",
      timestamp: "2025-08-23T07:20:00Z",
      classification: "Fake",
      confidence: 0.98,
      sentiment: "Positive",
      sentimentScore: 0.8,
      credibilityScore: 0.08,
      entities: ["Prime Minister", "India", "Government"],
      region: "India"
    },
    {
      id: 5,
      title: "Global Climate Summit Reaches Historic Agreement",
      content: "World leaders at the Global Climate Summit have reached a historic agreement to reduce carbon emissions by 50% over the next decade. The agreement includes $100 billion in funding for developing nations.",
      source: "BBC News",
      category: "Environment",
      timestamp: "2025-08-23T06:30:00Z",
      classification: "Real",
      confidence: 0.91,
      sentiment: "Positive", 
      sentimentScore: 0.6,
      credibilityScore: 0.95,
      entities: ["Climate Summit", "World Leaders", "Emissions"],
      region: "International"
    }
  ],
  modelPerformance: {
    accuracy: 0.943,
    precision: 0.912,
    recall: 0.897,
    f1Score: 0.904,
    models: [
      {name: "BERT", accuracy: 0.943, precision: 0.912, recall: 0.897, f1: 0.904, speed: "Slow"},
      {name: "LSTM", accuracy: 0.891, precision: 0.854, recall: 0.878, f1: 0.866, speed: "Medium"},
      {name: "Random Forest", accuracy: 0.876, precision: 0.842, recall: 0.863, f1: 0.852, speed: "Fast"},
      {name: "SVM", accuracy: 0.823, precision: 0.798, recall: 0.834, f1: 0.816, speed: "Fast"}
    ]
  },
  analytics: {
    categoryDistribution: [
      {category: "Politics", fake: 1245, real: 2876, total: 4121},
      {category: "Health", fake: 987, real: 2134, total: 3121},
      {category: "Technology", fake: 456, real: 1987, total: 2443},
      {category: "Sports", fake: 123, real: 1594, total: 1717},
      {category: "Environment", fake: 234, real: 1876, total: 2110}
    ],
    regionDistribution: [
      {region: "Karnataka", fake: 45, real: 156, total: 201},
      {region: "India", fake: 234, real: 567, total: 801},
      {region: "International", fake: 123, real: 445, total: 568}
    ],
    timeSeriesData: [
      {date: "2025-08-16", fake: 45, real: 123},
      {date: "2025-08-17", fake: 52, real: 134}, 
      {date: "2025-08-18", fake: 38, real: 156},
      {date: "2025-08-19", fake: 61, real: 142},
      {date: "2025-08-20", fake: 47, real: 167},
      {date: "2025-08-21", fake: 55, real: 178},
      {date: "2025-08-22", fake: 43, real: 145},
      {date: "2025-08-23", fake: 39, real: 134}
    ]
  }
};

// Chart instances
let trendChart, categoryChart, regionChart, timelineChart, modelChart;

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM loaded, initializing application...');
  initializeTabs();
  initializeDashboard();
  initializeLiveNews();
  initializeManualAnalysis();
  initializeAnalytics();
  initializeModelPerformance();
});

// Tab Management - Fixed Implementation
function initializeTabs() {
  console.log('Initializing tabs...');
  const tabButtons = document.querySelectorAll('.tab-button');
  const tabContents = document.querySelectorAll('.tab-content');

  console.log('Found', tabButtons.length, 'tab buttons and', tabContents.length, 'tab contents');

  tabButtons.forEach((button, index) => {
    console.log(`Setting up tab button ${index}:`, button.getAttribute('data-tab'));
    button.addEventListener('click', (e) => {
      e.preventDefault();
      const targetTab = button.getAttribute('data-tab');
      console.log('Tab clicked:', targetTab);
      
      // Remove active class from all buttons and contents
      tabButtons.forEach(btn => {
        btn.classList.remove('active');
        console.log('Removed active from button:', btn.getAttribute('data-tab'));
      });
      tabContents.forEach(content => {
        content.classList.remove('active');
        console.log('Removed active from content:', content.id);
      });
      
      // Add active class to clicked button and corresponding content
      button.classList.add('active');
      const targetContent = document.getElementById(targetTab);
      if (targetContent) {
        targetContent.classList.add('active');
        console.log('Activated tab:', targetTab);
        
        // Initialize charts when tabs are opened
        if (targetTab === 'analytics') {
          setTimeout(() => {
            console.log('Refreshing analytics charts...');
            refreshAnalyticsCharts();
          }, 100);
        } else if (targetTab === 'model-performance') {
          setTimeout(() => {
            console.log('Refreshing model chart...');
            refreshModelChart();
          }, 100);
        }
      } else {
        console.error('Target content not found:', targetTab);
      }
    });
  });
}

// Dashboard Initialization
function initializeDashboard() {
  console.log('Initializing dashboard...');
  // Update metrics
  document.getElementById('totalAnalyzed').textContent = appData.systemMetrics.totalAnalyzed.toLocaleString();
  document.getElementById('realDetected').textContent = appData.systemMetrics.realDetected.toLocaleString();
  document.getElementById('fakeDetected').textContent = appData.systemMetrics.fakeDetected.toLocaleString();
  document.getElementById('accuracy').textContent = (appData.modelPerformance.accuracy * 100).toFixed(1) + '%';
  
  // Initialize trend chart
  setTimeout(() => {
    initializeTrendChart();
  }, 100);
  
  // Populate recent results
  populateRecentResults();
}

function initializeTrendChart() {
  const ctx = document.getElementById('trendChart');
  if (!ctx) {
    console.error('Trend chart canvas not found');
    return;
  }
  
  console.log('Initializing trend chart...');
  trendChart = new Chart(ctx.getContext('2d'), {
    type: 'line',
    data: {
      labels: appData.analytics.timeSeriesData.map(d => {
        const date = new Date(d.date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
      }),
      datasets: [
        {
          label: 'Real News',
          data: appData.analytics.timeSeriesData.map(d => d.real),
          borderColor: '#1FB8CD',
          backgroundColor: 'rgba(31, 184, 205, 0.1)',
          fill: true,
          tension: 0.4
        },
        {
          label: 'Fake News',
          data: appData.analytics.timeSeriesData.map(d => d.fake),
          borderColor: '#B4413C',
          backgroundColor: 'rgba(180, 65, 60, 0.1)',
          fill: true,
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function populateRecentResults() {
  const container = document.getElementById('recentResults');
  if (!container) return;
  
  const recentNews = appData.sampleNews.slice(0, 3);
  
  container.innerHTML = recentNews.map(news => `
    <div class="result-item">
      <span class="result-title">${news.title.substring(0, 60)}...</span>
      <div class="result-status">
        <span class="status status--${news.classification.toLowerCase() === 'real' ? 'success' : 'error'}">
          ${news.classification}
        </span>
        <span class="confidence-${news.confidence > 0.9 ? 'high' : news.confidence > 0.7 ? 'medium' : 'low'}">
          ${(news.confidence * 100).toFixed(0)}%
        </span>
      </div>
    </div>
  `).join('');
}

// Live News Functionality
function initializeLiveNews() {
  console.log('Initializing live news...');
  const fetchKarnatakaBtn = document.getElementById('fetchKarnataka');
  const fetchIndiaBtn = document.getElementById('fetchIndia');
  const fetchInternationalBtn = document.getElementById('fetchInternational');
  
  if (fetchKarnatakaBtn) {
    fetchKarnatakaBtn.addEventListener('click', () => {
      console.log('Fetching Karnataka news...');
      fetchNews('Karnataka');
    });
  }
  
  if (fetchIndiaBtn) {
    fetchIndiaBtn.addEventListener('click', () => {
      console.log('Fetching India news...');
      fetchNews('India');
    });
  }
  
  if (fetchInternationalBtn) {
    fetchInternationalBtn.addEventListener('click', () => {
      console.log('Fetching International news...');
      fetchNews('International');
    });
  }
}

function fetchNews(region) {
  console.log('Fetching news for region:', region);
  const loadingSpinner = document.getElementById('loadingSpinner');
  const newsResults = document.getElementById('newsResults');
  
  if (loadingSpinner) loadingSpinner.classList.remove('hidden');
  if (newsResults) newsResults.innerHTML = '';
  
  // Simulate API call delay
  setTimeout(() => {
    const filteredNews = appData.sampleNews.filter(news => news.region === region);
    const simulatedNews = generateSimulatedNews(region, 3);
    const allNews = [...filteredNews, ...simulatedNews];
    
    displayNewsResults(allNews);
    if (loadingSpinner) loadingSpinner.classList.add('hidden');
  }, 2000);
}

function generateSimulatedNews(region, count) {
  const newsTemplates = {
    Karnataka: [
      {
        title: "Bangalore IT Sector Reports Record Growth in Q3 2025",
        content: "The Information Technology sector in Bangalore has reported unprecedented growth with over 50,000 new jobs created in the third quarter of 2025. Major tech companies are expanding their operations in the Silicon Valley of India.",
        source: "Deccan Herald",
        classification: "Real",
        confidence: 0.88
      },
      {
        title: "BREAKING: Karnataka Chief Minister Declares All Education Free Forever",
        content: "In a shocking move, Karnataka CM announced that all education from primary to PhD will be completely free for everyone in the state starting tomorrow. No verification or eligibility criteria needed.",
        source: "Karnataka Fake Times",
        classification: "Fake",
        confidence: 0.94
      }
    ],
    India: [
      {
        title: "India's Digital Payment System Crosses 10 Billion Transactions",
        content: "India's Unified Payments Interface (UPI) has achieved a historic milestone by processing over 10 billion transactions in a single month, reinforcing the country's position as a global leader in digital payments.",
        source: "Economic Times",
        classification: "Real",
        confidence: 0.91
      },
      {
        title: "Government Announces Free Smartphones for Every Citizen",
        content: "The Indian government has declared that every citizen will receive a free iPhone 15 Pro as part of a new digital inclusion initiative. Distribution centers will open in every district next Monday.",
        source: "India Misinformation Daily",
        classification: "Fake",
        confidence: 0.97
      }
    ],
    International: [
      {
        title: "European Union Announces Major Climate Initiative",
        content: "The European Union has unveiled a comprehensive climate action plan worth €500 billion to achieve carbon neutrality by 2030, five years ahead of the original target.",
        source: "Reuters",
        classification: "Real",
        confidence: 0.87
      },
      {
        title: "NASA Discovers Alien Life Forms on Mars, Keeps Secret",
        content: "Leaked documents suggest NASA has discovered intelligent alien civilization on Mars but is hiding the truth from the public to prevent global panic and economic collapse.",
        source: "Global Conspiracy Network",
        classification: "Fake",
        confidence: 0.99
      }
    ]
  };
  
  return newsTemplates[region].map((template, index) => ({
    id: `simulated_${region}_${index}`,
    title: template.title,
    content: template.content,
    source: template.source,
    category: "General",
    timestamp: new Date().toISOString(),
    classification: template.classification,
    confidence: template.confidence,
    sentiment: template.classification === "Real" ? "Positive" : "Negative",
    sentimentScore: template.classification === "Real" ? 0.5 : -0.3,
    credibilityScore: template.classification === "Real" ? 0.85 : 0.15,
    entities: [region],
    region: region
  }));
}

function displayNewsResults(newsItems) {
  const container = document.getElementById('newsResults');
  if (!container) return;
  
  container.innerHTML = newsItems.map(news => `
    <div class="news-item ${news.classification.toLowerCase()}">
      <div class="news-header">
        <h3 class="news-title">${news.title}</h3>
        <div class="news-meta">
          <span>📰 ${news.source}</span>
          <span>🏷️ ${news.category}</span>
          <span>⏰ ${new Date(news.timestamp).toLocaleString()}</span>
        </div>
      </div>
      <div class="news-content">
        ${news.content}
      </div>
      <div class="news-analysis">
        <div class="analysis-item">
          <span class="analysis-label">Classification</span>
          <span class="analysis-value ${news.classification.toLowerCase()}">${news.classification}</span>
        </div>
        <div class="analysis-item">
          <span class="analysis-label">Confidence</span>
          <span class="analysis-value">${(news.confidence * 100).toFixed(1)}%</span>
        </div>
        <div class="analysis-item">
          <span class="analysis-label">Sentiment</span>
          <span class="analysis-value">${news.sentiment}</span>
        </div>
        <div class="analysis-item">
          <span class="analysis-label">Credibility</span>
          <span class="analysis-value">${(news.credibilityScore * 100).toFixed(0)}%</span>
        </div>
      </div>
    </div>
  `).join('');
}

// Manual Analysis
function initializeManualAnalysis() {
  console.log('Initializing manual analysis...');
  const analyzeBtn = document.getElementById('analyzeManual');
  if (analyzeBtn) {
    analyzeBtn.addEventListener('click', performManualAnalysis);
  }
}

function performManualAnalysis() {
  console.log('Performing manual analysis...');
  const title = document.getElementById('articleTitle').value.trim();
  const content = document.getElementById('articleContent').value.trim();
  const source = document.getElementById('articleSource').value.trim() || 'Unknown Source';
  
  if (!title || !content) {
    alert('Please enter both title and content for analysis.');
    return;
  }
  
  // Simulate analysis
  const analysisResult = simulateAnalysis(title, content);
  displayManualResults(analysisResult, title, content, source);
}

function simulateAnalysis(title, content) {
  // Simple heuristic-based fake news detection simulation
  const fakeKeywords = ['shocking', 'secret', 'government hides', 'conspiracy', 'leaked documents', 'breaking exclusive', 'you won\'t believe'];
  const realKeywords = ['according to', 'research shows', 'study finds', 'official statement', 'data indicates'];
  
  const text = (title + ' ' + content).toLowerCase();
  let fakeScore = 0;
  let realScore = 0;
  
  fakeKeywords.forEach(keyword => {
    if (text.includes(keyword)) fakeScore += 1;
  });
  
  realKeywords.forEach(keyword => {
    if (text.includes(keyword)) realScore += 1;
  });
  
  // Determine classification
  const isFake = fakeScore > realScore || fakeScore > 2;
  const confidence = Math.min(0.95, 0.7 + (Math.abs(fakeScore - realScore) * 0.1));
  
  return {
    classification: isFake ? 'Fake' : 'Real',
    confidence: confidence,
    sentiment: isFake ? 'Negative' : 'Positive',
    sentimentScore: isFake ? -0.4 : 0.5,
    credibilityScore: isFake ? 0.2 : 0.8,
    entities: extractEntities(text)
  };
}

function extractEntities(text) {
  // Simple entity extraction simulation
  const entities = [];
  const commonEntities = ['government', 'india', 'karnataka', 'bangalore', 'prime minister', 'covid', 'election'];
  
  commonEntities.forEach(entity => {
    if (text.includes(entity)) {
      entities.push(entity.charAt(0).toUpperCase() + entity.slice(1));
    }
  });
  
  return entities;
}

function displayManualResults(result, title, content, source) {
  const container = document.getElementById('manualResults');
  if (!container) return;
  
  container.innerHTML = `
    <div class="news-item ${result.classification.toLowerCase()}">
      <div class="news-header">
        <h3 class="news-title">${title}</h3>
        <div class="news-meta">
          <span>📰 ${source}</span>
          <span>⏰ ${new Date().toLocaleString()}</span>
        </div>
      </div>
      <div class="news-content">
        ${content.substring(0, 300)}${content.length > 300 ? '...' : ''}
      </div>
      <div class="news-analysis">
        <div class="analysis-item">
          <span class="analysis-label">Classification</span>
          <span class="analysis-value ${result.classification.toLowerCase()}">${result.classification}</span>
        </div>
        <div class="analysis-item">
          <span class="analysis-label">Confidence</span>
          <span class="analysis-value">${(result.confidence * 100).toFixed(1)}%</span>
        </div>
        <div class="analysis-item">
          <span class="analysis-label">Sentiment</span>
          <span class="analysis-value">${result.sentiment}</span>
        </div>
        <div class="analysis-item">
          <span class="analysis-label">Credibility</span>
          <span class="analysis-value">${(result.credibilityScore * 100).toFixed(0)}%</span>
        </div>
      </div>
    </div>
  `;
  
  container.classList.remove('hidden');
}

// Analytics
function initializeAnalytics() {
  console.log('Initializing analytics...');
  const exportBtn = document.getElementById('exportData');
  if (exportBtn) {
    exportBtn.addEventListener('click', exportAnalytics);
  }
  
  // Initialize charts with a delay to ensure DOM is ready
  setTimeout(() => {
    initializeAnalyticsCharts();
  }, 500);
}

function initializeAnalyticsCharts() {
  console.log('Initializing analytics charts...');
  initializeCategoryChart();
  initializeRegionChart();
  initializeTimelineChart();
}

function initializeCategoryChart() {
  const ctx = document.getElementById('categoryChart');
  if (!ctx) {
    console.error('Category chart canvas not found');
    return;
  }
  
  console.log('Initializing category chart...');
  categoryChart = new Chart(ctx.getContext('2d'), {
    type: 'doughnut',
    data: {
      labels: appData.analytics.categoryDistribution.map(d => d.category),
      datasets: [{
        label: 'Fake News by Category',
        data: appData.analytics.categoryDistribution.map(d => d.fake),
        backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
}

function initializeRegionChart() {
  const ctx = document.getElementById('regionChart');
  if (!ctx) {
    console.error('Region chart canvas not found');
    return;
  }
  
  console.log('Initializing region chart...');
  regionChart = new Chart(ctx.getContext('2d'), {
    type: 'bar',
    data: {
      labels: appData.analytics.regionDistribution.map(d => d.region),
      datasets: [
        {
          label: 'Real News',
          data: appData.analytics.regionDistribution.map(d => d.real),
          backgroundColor: '#1FB8CD'
        },
        {
          label: 'Fake News',
          data: appData.analytics.regionDistribution.map(d => d.fake),
          backgroundColor: '#B4413C'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function initializeTimelineChart() {
  const ctx = document.getElementById('timelineChart');
  if (!ctx) {
    console.error('Timeline chart canvas not found');
    return;
  }
  
  console.log('Initializing timeline chart...');
  timelineChart = new Chart(ctx.getContext('2d'), {
    type: 'line',
    data: {
      labels: appData.analytics.timeSeriesData.map(d => {
        const date = new Date(d.date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
      }),
      datasets: [
        {
          label: 'Total Articles Analyzed',
          data: appData.analytics.timeSeriesData.map(d => d.fake + d.real),
          borderColor: '#1FB8CD',
          backgroundColor: 'rgba(31, 184, 205, 0.1)',
          fill: true,
          tension: 0.4
        },
        {
          label: 'Fake News Detected',
          data: appData.analytics.timeSeriesData.map(d => d.fake),
          borderColor: '#B4413C',
          backgroundColor: 'rgba(180, 65, 60, 0.1)',
          fill: false,
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function refreshAnalyticsCharts() {
  console.log('Refreshing analytics charts...');
  if (categoryChart) categoryChart.resize();
  if (regionChart) regionChart.resize();
  if (timelineChart) timelineChart.resize();
}

function exportAnalytics() {
  console.log('Exporting analytics data...');
  const data = {
    exportDate: new Date().toISOString(),
    systemMetrics: appData.systemMetrics,
    analytics: appData.analytics,
    modelPerformance: appData.modelPerformance
  };
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `fake-news-analytics-${new Date().toISOString().split('T')[0]}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Model Performance
function initializeModelPerformance() {
  console.log('Initializing model performance...');
  populatePerformanceTable();
  
  // Initialize chart with a delay
  setTimeout(() => {
    initializeModelChart();
  }, 500);
}

function populatePerformanceTable() {
  const tbody = document.getElementById('performanceTableBody');
  if (!tbody) return;
  
  tbody.innerHTML = appData.modelPerformance.models.map(model => `
    <tr>
      <td><strong>${model.name}</strong></td>
      <td>${(model.accuracy * 100).toFixed(1)}%</td>
      <td>${(model.precision * 100).toFixed(1)}%</td>
      <td>${(model.recall * 100).toFixed(1)}%</td>
      <td>${(model.f1 * 100).toFixed(1)}%</td>
      <td><span class="status status--${model.speed.toLowerCase() === 'fast' ? 'success' : model.speed.toLowerCase() === 'medium' ? 'warning' : 'info'}">${model.speed}</span></td>
    </tr>
  `).join('');
}

function initializeModelChart() {
  const ctx = document.getElementById('modelChart');
  if (!ctx) {
    console.error('Model chart canvas not found');
    return;
  }
  
  console.log('Initializing model chart...');
  modelChart = new Chart(ctx.getContext('2d'), {
    type: 'radar',
    data: {
      labels: ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
      datasets: appData.modelPerformance.models.map((model, index) => ({
        label: model.name,
        data: [
          model.accuracy * 100,
          model.precision * 100,
          model.recall * 100,
          model.f1 * 100
        ],
        backgroundColor: `rgba(${['31,184,205', '255,193,133', '180,65,60', '93,135,143'][index]}, 0.1)`,
        borderColor: `rgb(${['31,184,205', '255,193,133', '180,65,60', '93,135,143'][index]})`,
        pointBackgroundColor: `rgb(${['31,184,205', '255,193,133', '180,65,60', '93,135,143'][index]})`,
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: `rgb(${['31,184,205', '255,193,133', '180,65,60', '93,135,143'][index]})`
      }))
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      elements: {
        line: {
          borderWidth: 3
        }
      },
      scales: {
        r: {
          beginAtZero: true,
          max: 100
        }
      }
    }
  });
}

function refreshModelChart() {
  console.log('Refreshing model chart...');
  if (modelChart) modelChart.resize();
}

// Utility Functions
function formatNumber(num) {
  return num.toLocaleString();
}

function formatPercentage(num) {
  return (num * 100).toFixed(1) + '%';
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}
"""
Enhanced Fake News Detection System with Real News API Integration
Fetches live news from free APIs for Karnataka, India, and International sources
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import logging
from datetime import datetime
import os
import re
import sqlite3
import json
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

# Initialize Flask app
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'

class NewsAPIClient:
    """
    Client for fetching news from free APIs
    """
    
    def __init__(self):
        # Free API endpoints (no key required for basic usage)
        self.gnews_base = "https://gnews.io/api/v4/search"
        self.newsdata_base = "https://newsdata.io/api/1/news"
        self.currents_base = "https://api.currentsapi.services/v1/search"
        
        # Backup: Use RSS feeds if APIs are down
        self.rss_feeds = {
            'india': [
                'https://feeds.feedburner.com/NDTV-LatestNews',
                'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
                'https://indianexpress.com/feed/',
            ],
            'karnataka': [
                'https://www.thehindu.com/news/national/karnataka/feeder/default.rss',
                'https://timesofindia.indiatimes.com/city/bengaluru/rss.cms',
            ],
            'international': [
                'https://feeds.bbci.co.uk/news/rss.xml',
                'http://rss.cnn.com/rss/edition.rss',
                'https://feeds.reuters.com/reuters/topNews',
            ]
        }
    
    def fetch_news_gnews(self, query, country=None, lang='en', max_articles=20):
        """Fetch news from GNews API (free tier available)"""
        try:
            params = {
                'q': query,
                'lang': lang,
                'max': min(max_articles, 10),  # Free tier limit
            }
            
            if country:
                params['country'] = country
            
            # Note: For production, you'd add your API key here
            # params['apikey'] = 'your-gnews-api-key'
            
            response = requests.get(self.gnews_base, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_gnews_response(data)
            else:
                logger.warning(f"GNews API returned status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching from GNews: {str(e)}")
            return []
    
    def fetch_indian_news(self, category='general', max_articles=15):
        """Fetch Indian news articles"""
        try:
            # Try multiple approaches for Indian news
            articles = []
            
            # Approach 1: Search for India-specific terms
            indian_queries = [
                'India news',
                'Mumbai Delhi Bangalore',
                'Indian government',
                'Bollywood India'
            ]
            
            for query in indian_queries[:2]:  # Limit queries to avoid rate limits
                news = self.fetch_news_gnews(query, country='in', max_articles=5)
                articles.extend(news)
                time.sleep(1)  # Rate limiting
            
            # Approach 2: Fallback to RSS feeds
            if len(articles) < 5:
                rss_articles = self._fetch_from_rss('india', max_articles=10)
                articles.extend(rss_articles)
            
            return articles[:max_articles]
            
        except Exception as e:
            logger.error(f"Error fetching Indian news: {str(e)}")
            return self._get_sample_indian_news()
    
    def fetch_karnataka_news(self, max_articles=10):
        """Fetch Karnataka-specific news"""
        try:
            articles = []
            
            # Karnataka-specific searches
            karnataka_queries = [
                'Karnataka Bangalore news',
                'Mysore Hubli Karnataka',
                'Karnataka government'
            ]
            
            for query in karnataka_queries[:2]:
                news = self.fetch_news_gnews(query, country='in', max_articles=3)
                articles.extend(news)
                time.sleep(1)
            
            # Fallback to RSS
            if len(articles) < 5:
                rss_articles = self._fetch_from_rss('karnataka', max_articles=8)
                articles.extend(rss_articles)
            
            return articles[:max_articles]
            
        except Exception as e:
            logger.error(f"Error fetching Karnataka news: {str(e)}")
            return self._get_sample_karnataka_news()
    
    def fetch_international_news(self, max_articles=15):
        """Fetch international news"""
        try:
            articles = []
            
            # International queries
            international_queries = [
                'world news',
                'United States Europe',
                'global economy',
                'international politics'
            ]
            
            for query in international_queries[:2]:
                news = self.fetch_news_gnews(query, max_articles=5)
                articles.extend(news)
                time.sleep(1)
            
            # Fallback to RSS
            if len(articles) < 5:
                rss_articles = self._fetch_from_rss('international', max_articles=10)
                articles.extend(rss_articles)
            
            return articles[:max_articles]
            
        except Exception as e:
            logger.error(f"Error fetching international news: {str(e)}")
            return self._get_sample_international_news()
    
    def _fetch_from_rss(self, category, max_articles=10):
        """Fetch news from RSS feeds as fallback"""
        try:
            import feedparser
            articles = []
            
            feeds = self.rss_feeds.get(category, [])
            
            for feed_url in feeds[:2]:  # Limit to 2 feeds to avoid slowdown
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:5]:  # 5 articles per feed
                        articles.append({
                            'title': entry.get('title', ''),
                            'description': entry.get('summary', ''),
                            'content': entry.get('summary', ''),
                            'url': entry.get('link', ''),
                            'source': feed.feed.get('title', 'RSS Feed'),
                            'publishedAt': entry.get('published', datetime.now().isoformat()),
                            'category': category.title()
                        })
                except Exception as e:
                    logger.warning(f"Error parsing RSS feed {feed_url}: {str(e)}")
                    continue
            
            return articles[:max_articles]
            
        except ImportError:
            logger.warning("feedparser not available, using sample data")
            return []
        except Exception as e:
            logger.error(f"Error in RSS fallback: {str(e)}")
            return []
    
    def _format_gnews_response(self, data):
        """Format GNews API response"""
        articles = []
        
        if 'articles' in data:
            for article in data['articles']:
                articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'content': article.get('content', article.get('description', '')),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'publishedAt': article.get('publishedAt', datetime.now().isoformat()),
                    'category': 'General'
                })
        
        return articles
    
    def _get_sample_indian_news(self):
        """Sample Indian news for demo"""
        return [
            {
                'title': 'Prime Minister Announces New Digital India Initiative',
                'content': 'The Prime Minister today announced a comprehensive new Digital India initiative aimed at improving internet connectivity across rural areas...',
                'source': 'Press Information Bureau',
                'category': 'Politics',
                'publishedAt': datetime.now().isoformat(),
                'url': 'https://example.com/digital-india'
            },
            {
                'title': 'Mumbai Metro Expansion Project Approved',
                'content': 'The Maharashtra government has approved the expansion of Mumbai Metro network to cover additional 100 kilometers...',
                'source': 'Times of India',
                'category': 'Infrastructure',
                'publishedAt': datetime.now().isoformat(),
                'url': 'https://example.com/mumbai-metro'
            },
            {
                'title': 'Indian Cricket Team Wins Series Against Australia',
                'content': 'The Indian cricket team secured a historic 3-1 series win against Australia in the recently concluded test series...',
                'source': 'ESPN Cricinfo',
                'category': 'Sports',
                'publishedAt': datetime.now().isoformat(),
                'url': 'https://example.com/cricket-series'
            }
        ]
    
    def _get_sample_karnataka_news(self):
        """Sample Karnataka news for demo"""
        return [
            {
                'title': 'Bangalore IT Sector Reports 15% Growth This Quarter',
                'content': 'The Information Technology sector in Bangalore has reported a significant 15% growth this quarter, driven by increased demand for digital services...',
                'source': 'The Hindu',
                'category': 'Technology',
                'publishedAt': datetime.now().isoformat(),
                'url': 'https://example.com/bangalore-it-growth'
            },
            {
                'title': 'Karnataka Government Launches New Education Policy',
                'content': 'The Karnataka state government has launched a comprehensive new education policy focusing on skill development and digital learning...',
                'source': 'Deccan Herald',
                'category': 'Education',
                'publishedAt': datetime.now().isoformat(),
                'url': 'https://example.com/karnataka-education'
            },
            {
                'title': 'Mysore Palace Tourism Sees Record Visitors',
                'content': 'Mysore Palace has recorded the highest number of tourists this year, with over 2 million visitors in the past six months...',
                'source': 'Karnataka Tourism',
                'category': 'Tourism',
                'publishedAt': datetime.now().isoformat(),
                'url': 'https://example.com/mysore-palace-tourism'
            }
        ]
    
    def _get_sample_international_news(self):
        """Sample international news for demo"""
        return [
            {
                'title': 'Global Climate Summit Reaches Historic Agreement',
                'content': 'World leaders at the Global Climate Summit have reached a historic agreement to reduce carbon emissions by 50% over the next decade...',
                'source': 'BBC News',
                'category': 'Environment',
                'publishedAt': datetime.now().isoformat(),
                'url': 'https://example.com/climate-summit'
            },
            {
                'title': 'Tech Giants Announce AI Safety Initiative',
                'content': 'Major technology companies have announced a collaborative initiative to develop safety standards for artificial intelligence systems...',
                'source': 'Reuters',
                'category': 'Technology',
                'publishedAt': datetime.now().isoformat(),
                'url': 'https://example.com/ai-safety-initiative'
            },
            {
                'title': 'European Space Agency Launches Mars Mission',
                'content': 'The European Space Agency successfully launched its latest Mars exploration mission, marking a significant milestone in space exploration...',
                'source': 'CNN',
                'category': 'Science',
                'publishedAt': datetime.now().isoformat(),
                'url': 'https://example.com/mars-mission'
            }
        ]

class EnhancedFakeNewsDetector:
    """Enhanced fake news detector with temporal awareness"""
    
    def __init__(self):
        self.current_year = 2025
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
    def analyze_article(self, title, content, source):
        """Comprehensive analysis of a news article"""
        full_text = f"{title} {content}"
        
        # Fake news classification
        classification_result = self._classify_news(full_text, source)
        
        # Sentiment analysis
        sentiment_result = self._analyze_sentiment(full_text)
        
        # Extract entities
        entities = self._extract_entities(full_text)
        
        # Source credibility
        credibility = self._assess_source_credibility(source)
        
        # Suspicious patterns
        patterns = self._detect_suspicious_patterns(full_text)
        
        return {
            'title': title,
            'classification': classification_result['classification'],
            'confidence': classification_result['confidence'],
            'reasoning': classification_result['reasoning'],
            'sentiment': sentiment_result['label'],
            'sentiment_score': sentiment_result['score'],
            'credibility_score': credibility,
            'entities': entities,
            'suspicious_patterns': patterns,
            'source': source
        }
    
    def _classify_news(self, text, source):
        """Classify news as real or fake"""
        confidence = 0.5
        reasoning = []
        
        text_lower = text.lower()
        
        # Check for sensational language
        sensational_words = ['shocking', 'unbelievable', 'breaking', 'exclusive', 'secret', 'exposed']
        sensational_count = sum(1 for word in sensational_words if word in text_lower)
        
        if sensational_count > 2:
            confidence -= 0.2
            reasoning.append("Contains excessive sensational language")
        
        # Check for proper attribution
        if any(phrase in text_lower for phrase in ['according to', 'sources say', 'reported by', 'study shows']):
            confidence += 0.15
            reasoning.append("Contains proper source attribution")
        
        # Check punctuation
        exclamation_count = text.count('!')
        if exclamation_count > 3:
            confidence -= 0.1
            reasoning.append("Excessive use of exclamation marks")
        
        # Source credibility impact
        source_score = self._assess_source_credibility(source)
        confidence += (source_score - 0.5) * 0.3
        
        if source_score > 0.8:
            reasoning.append("High credibility source")
        elif source_score < 0.3:
            reasoning.append("Low credibility source")
        
        # Ensure confidence in valid range
        confidence = max(0.1, min(0.95, confidence))
        
        classification = "Real" if confidence > 0.6 else "Fake"
        
        return {
            'classification': classification,
            'confidence': confidence,
            'reasoning': reasoning
        }
    
    def _analyze_sentiment(self, text):
        """Analyze sentiment using VADER"""
        scores = self.sentiment_analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            label = 'Positive'
        elif compound <= -0.05:
            label = 'Negative'
        else:
            label = 'Neutral'
        
        return {
            'label': label,
            'score': compound,
            'confidence': abs(compound)
        }
    
    def _extract_entities(self, text):
        """Simple entity extraction"""
        entities = []
        words = text.split()
        
        for word in words:
            if word.istitle() and len(word) > 2:
                entities.append(word)
        
        return list(set(entities))[:10]
    
    def _assess_source_credibility(self, source):
        """Assess source credibility"""
        if not source:
            return 0.5
        
        source_lower = source.lower()
        
        # High credibility sources
        credible_sources = {
            'bbc': 0.95, 'reuters': 0.98, 'cnn': 0.90, 'times of india': 0.85,
            'the hindu': 0.90, 'indian express': 0.85, 'deccan herald': 0.80,
            'press information bureau': 0.95, 'pib': 0.95
        }
        
        # Low credibility indicators
        suspicious_indicators = ['fake', 'conspiracy', 'hoax', 'clickbait']
        
        for credible, score in credible_sources.items():
            if credible in source_lower:
                return score
        
        if any(indicator in source_lower for indicator in suspicious_indicators):
            return 0.2
        
        return 0.6  # Default for unknown sources
    
    def _detect_suspicious_patterns(self, text):
        """Detect suspicious patterns in text"""
        patterns = []
        
        # Excessive capitalization
        if sum(1 for c in text if c.isupper()) / len(text) > 0.3:
            patterns.append("Excessive capitalization")
        
        # Too many exclamation marks
        if text.count('!') > 5:
            patterns.append("Excessive exclamation marks")
        
        # Clickbait phrases
        clickbait_phrases = ['you won\'t believe', 'doctors hate', 'one weird trick', 'this will shock you']
        if any(phrase in text.lower() for phrase in clickbait_phrases):
            patterns.append("Contains clickbait language")
        
        return patterns

# Initialize components
news_client = NewsAPIClient()
detector = EnhancedFakeNewsDetector()

@app.route('/')
def index():
    """Main dashboard with news fetching options"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Enhanced Fake News Detection with Live News</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .header { text-align: center; margin-bottom: 30px; }
            .news-selector { display: flex; justify-content: center; gap: 20px; margin-bottom: 30px; }
            .news-btn { padding: 15px 25px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            .news-btn:hover { background: #0056b3; }
            .news-btn.active { background: #28a745; }
            .manual-analysis { margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            textarea, input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 3px; }
            .analyze-btn { background: #28a745; color: white; padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer; }
            .news-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; margin-top: 20px; }
            .news-card { border: 1px solid #ddd; border-radius: 8px; padding: 15px; background: white; }
            .news-title { font-weight: bold; margin-bottom: 10px; color: #333; }
            .news-content { margin-bottom: 15px; color: #666; font-size: 14px; }
            .analysis-result { padding: 10px; border-radius: 5px; margin-top: 10px; }
            .real-news { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
            .fake-news { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
            .loading { text-align: center; padding: 20px; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ Enhanced Fake News Detection System</h1>
                <p>Analyze live news from Karnataka, India, and International sources</p>
            </div>

            <!-- Manual Analysis Section -->
            <div class="manual-analysis">
                <h3>📝 Manual Article Analysis</h3>
                <form id="manualForm">
                    <div class="form-group">
                        <label for="manualText">Article Text:</label>
                        <textarea id="manualText" rows="4" placeholder="Paste news article text here..."></textarea>
                    </div>
                    <div class="form-group">
                        <label for="manualSource">Source (Optional):</label>
                        <input type="text" id="manualSource" placeholder="e.g., BBC News, Times of India">
                    </div>
                    <button type="submit" class="analyze-btn">🔍 Analyze Article</button>
                </form>
                <div id="manualResult"></div>
            </div>

            <!-- News Source Selection -->
            <div class="news-selector">
                <button class="news-btn active" data-source="karnataka">🏛️ Karnataka News</button>
                <button class="news-btn" data-source="india">🇮🇳 India News</button>
                <button class="news-btn" data-source="international">🌍 International News</button>
            </div>

            <!-- Loading indicator -->
            <div id="loading" class="loading" style="display: none;">
                <h3>📡 Fetching live news articles...</h3>
                <p>Please wait while we analyze the latest news for fake content</p>
            </div>

            <!-- News Grid -->
            <div id="newsGrid" class="news-grid"></div>
        </div>

        <script>
            let currentSource = 'karnataka';
            
            // Handle manual analysis
            document.getElementById('manualForm').addEventListener('submit', function(e) {
                e.preventDefault();
                
                const text = document.getElementById('manualText').value;
                const source = document.getElementById('manualSource').value || 'Unknown';
                
                if (!text.trim()) {
                    alert('Please enter some text to analyze');
                    return;
                }
                
                fetch('/api/analyze-manual', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, source })
                })
                .then(response => response.json())
                .then(result => {
                    const resultDiv = document.getElementById('manualResult');
                    const isReal = result.classification === 'Real';
                    
                    resultDiv.innerHTML = `
                        <div class="analysis-result ${isReal ? 'real-news' : 'fake-news'}">
                            <strong>Classification:</strong> ${result.classification}<br>
                            <strong>Confidence:</strong> ${(result.confidence * 100).toFixed(1)}%<br>
                            <strong>Sentiment:</strong> ${result.sentiment} (${result.sentiment_score.toFixed(2)})<br>
                            <strong>Credibility Score:</strong> ${(result.credibility_score * 100).toFixed(1)}%<br>
                            <strong>Reasoning:</strong> ${result.reasoning.join(', ')}<br>
                            ${result.entities.length > 0 ? `<strong>Key Entities:</strong> ${result.entities.join(', ')}<br>` : ''}
                            ${result.suspicious_patterns.length > 0 ? `<strong>Suspicious Patterns:</strong> ${result.suspicious_patterns.join(', ')}` : ''}
                        </div>
                    `;
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('manualResult').innerHTML = '<div class="analysis-result fake-news">Error analyzing article. Please try again.</div>';
                });
            });
            
            // Handle news source selection
            document.querySelectorAll('.news-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    // Update active button
                    document.querySelectorAll('.news-btn').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    
                    currentSource = this.dataset.source;
                    fetchAndAnalyzeNews(currentSource);
                });
            });
            
            function fetchAndAnalyzeNews(source) {
                document.getElementById('loading').style.display = 'block';
                document.getElementById('newsGrid').innerHTML = '';
                
                fetch(`/api/fetch-news/${source}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    displayNews(data.articles);
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('newsGrid').innerHTML = '<p>Error fetching news. Please try again.</p>';
                });
            }
            
            function displayNews(articles) {
                const grid = document.getElementById('newsGrid');
                
                articles.forEach(article => {
                    const isReal = article.classification === 'Real';
                    const confidencePercent = (article.confidence * 100).toFixed(1);
                    
                    const card = document.createElement('div');
                    card.className = 'news-card';
                    card.innerHTML = `
                        <div class="news-title">${article.title}</div>
                        <div class="news-content">${article.content.substring(0, 200)}...</div>
                        <div><strong>Source:</strong> ${article.source}</div>
                        <div class="analysis-result ${isReal ? 'real-news' : 'fake-news'}">
                            <strong>${article.classification}</strong> (${confidencePercent}% confidence)<br>
                            <strong>Sentiment:</strong> ${article.sentiment}<br>
                            <strong>Credibility:</strong> ${(article.credibility_score * 100).toFixed(1)}%<br>
                            ${article.reasoning.length > 0 ? `<em>${article.reasoning.join(', ')}</em><br>` : ''}
                            ${article.suspicious_patterns.length > 0 ? `<strong>⚠️ Issues:</strong> ${article.suspicious_patterns.join(', ')}` : ''}
                        </div>
                    `;
                    grid.appendChild(card);
                });
            }
            
            // Load Karnataka news by default
            fetchAndAnalyzeNews('karnataka');
        </script>
    </body>
    </html>
    '''

@app.route('/api/fetch-news/<source>')
def fetch_news(source):
    """Fetch and analyze news from specified source"""
    try:
        # Fetch news articles
        if source == 'karnataka':
            articles = news_client.fetch_karnataka_news(max_articles=12)
        elif source == 'india':
            articles = news_client.fetch_indian_news(max_articles=15)
        elif source == 'international':
            articles = news_client.fetch_international_news(max_articles=15)
        else:
            return jsonify({'error': 'Invalid source'}), 400
        
        # Analyze each article for fake news
        analyzed_articles = []
        
        for article in articles:
            try:
                analysis = detector.analyze_article(
                    article['title'],
                    article.get('content', article.get('description', '')),
                    article['source']
                )
                analyzed_articles.append(analysis)
                
            except Exception as e:
                logger.error(f"Error analyzing article: {str(e)}")
                continue
        
        return jsonify({
            'articles': analyzed_articles,
            'source': source,
            'total_analyzed': len(analyzed_articles),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching news: {str(e)}")
        return jsonify({'error': 'Failed to fetch news'}), 500

@app.route('/api/analyze-manual', methods=['POST'])
def analyze_manual():
    """Analyze manually provided article"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        source = data.get('source', 'Unknown')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Analyze the article
        analysis = detector.analyze_article('Manual Input', text, source)
        
        return jsonify(analysis)
        
    except Exception as e:
        logger.error(f"Error in manual analysis: {str(e)}")
        return jsonify({'error': 'Analysis failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
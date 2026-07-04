from flask import Flask, render_template_string, request
from textblob import TextBlob

app = Flask(__name__)

# ULTRA-LIGHT BLUE THEME - FINAL VERSION
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentiment Analyzer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            background: #e8f4f8;
            background: linear-gradient(135deg, #e8f4f8 0%, #f0f8fc 50%, #f5faff 100%);
            position: relative;
        }

        body::before {
            content: '';
            position: fixed;
            top: -20%;
            right: -10%;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(173, 216, 230, 0.3) 0%, transparent 70%);
            border-radius: 50%;
            filter: blur(80px);
            pointer-events: none;
            z-index: 0;
        }

        body::after {
            content: '';
            position: fixed;
            bottom: -20%;
            left: -10%;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(176, 224, 230, 0.25) 0%, transparent 70%);
            border-radius: 50%;
            filter: blur(80px);
            pointer-events: none;
            z-index: 0;
        }

        .container {
            position: relative;
            z-index: 1;
            background: rgba(255, 255, 255, 0.88);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 28px;
            padding: 48px;
            max-width: 920px;
            width: 100%;
            box-shadow: 
                0 2px 12px rgba(0, 0, 0, 0.02),
                0 8px 32px rgba(0, 0, 0, 0.03),
                0 20px 60px rgba(0, 0, 0, 0.02),
                inset 0 1px 0 rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.7);
            animation: slideUp 0.6s ease-out;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .header {
            text-align: center;
            margin-bottom: 32px;
            padding-bottom: 24px;
            border-bottom: 1px solid rgba(173, 216, 230, 0.2);
        }

        .header .icon {
            font-size: 44px;
            display: block;
            margin-bottom: 8px;
        }

        .header h1 {
            font-size: 34px;
            font-weight: 800;
            color: #1a2a3a;
            letter-spacing: -0.5px;
        }

        .header p {
            color: #7a9aaa;
            font-size: 15px;
            margin-top: 6px;
            font-weight: 400;
        }

        .input-section {
            margin-bottom: 20px;
        }

        .input-section label {
            display: block;
            font-weight: 600;
            color: #1a2a3a;
            margin-bottom: 8px;
            font-size: 14px;
        }

        textarea {
            width: 100%;
            height: 180px;
            padding: 16px 18px;
            font-size: 15px;
            font-family: 'Inter', sans-serif;
            border: 1.5px solid rgba(173, 216, 230, 0.3);
            border-radius: 14px;
            outline: none;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            color: #1a2a3a;
            line-height: 1.6;
            resize: vertical;
        }

        textarea:focus {
            border-color: rgba(74, 144, 217, 0.4);
            background: rgba(255, 255, 255, 0.85);
            box-shadow: 0 0 0 4px rgba(74, 144, 217, 0.04);
        }

        textarea::placeholder {
            color: #aac0d0;
        }

        .button-row {
            display: flex;
            gap: 12px;
            margin-top: 18px;
            flex-wrap: wrap;
        }

        .btn-primary {
            background: linear-gradient(135deg, #7ab8d4 0%, #5ba3c4 100%);
            color: white;
            border: none;
            padding: 14px 36px;
            font-size: 15px;
            font-weight: 600;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            flex: 1;
            min-width: 160px;
            box-shadow: 0 2px 12px rgba(91, 163, 196, 0.15);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 28px rgba(91, 163, 196, 0.25);
            background: linear-gradient(135deg, #6aaccc 0%, #4a96b8 100%);
        }

        .btn-primary:active {
            transform: translateY(0);
        }

        .btn-clear {
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            color: #6a8a9a;
            border: 1px solid rgba(173, 216, 230, 0.2);
            padding: 14px 24px;
            font-size: 14px;
            font-weight: 500;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .btn-clear:hover {
            background: rgba(255, 255, 255, 0.85);
            transform: translateY(-2px);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin: 28px 0 24px 0;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border-radius: 16px;
            padding: 20px 16px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.4);
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            background: rgba(255, 255, 255, 0.7);
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.02);
        }

        .stat-card .number {
            font-size: 32px;
            font-weight: 700;
            display: block;
            line-height: 1.2;
        }

        .stat-card .label {
            font-size: 12px;
            color: #6a8a9a;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }

        .stat-total .number { color: #5ba3c4; }
        .stat-positive .number { color: #10b981; }
        .stat-negative .number { color: #ef4444; }
        .stat-neutral .number { color: #f59e0b; }

        .verdict {
            text-align: center;
            padding: 20px 24px;
            border-radius: 16px;
            margin: 20px 0 28px 0;
            font-size: 22px;
            font-weight: 700;
            animation: fadeIn 0.5s ease-out;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.96); }
            to { opacity: 1; transform: scale(1); }
        }

        .verdict.positive {
            background: rgba(236, 253, 245, 0.5);
            color: #065f46;
            border: 1.5px solid rgba(167, 243, 208, 0.3);
        }

        .verdict.negative {
            background: rgba(254, 242, 242, 0.5);
            color: #991b1b;
            border: 1.5px solid rgba(252, 165, 165, 0.3);
        }

        .verdict.neutral {
            background: rgba(255, 251, 235, 0.5);
            color: #92400e;
            border: 1.5px solid rgba(252, 211, 77, 0.3);
        }

        .verdict .sub-text {
            font-size: 14px;
            font-weight: 400;
            opacity: 0.7;
            display: block;
            margin-top: 4px;
        }

        .results-section {
            margin-top: 8px;
        }

        .results-section .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
        }

        .results-section h3 {
            font-size: 17px;
            font-weight: 600;
            color: #1a2a3a;
        }

        .results-section .count-badge {
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            color: #6a8a9a;
            font-size: 13px;
            font-weight: 500;
            padding: 4px 14px;
            border-radius: 50px;
        }

        .review-list {
            max-height: 380px;
            overflow-y: auto;
            border-radius: 14px;
            border: 1px solid rgba(173, 216, 230, 0.15);
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
        }

        .review-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 18px;
            border-bottom: 1px solid rgba(173, 216, 230, 0.1);
            gap: 12px;
            background: rgba(255, 255, 255, 0.1);
            transition: background 0.2s ease;
        }

        .review-item:last-child {
            border-bottom: none;
        }

        .review-item:hover {
            background: rgba(255, 255, 255, 0.4);
        }

        .review-text {
            flex: 1;
            color: #1a2a3a;
            font-size: 14px;
            line-height: 1.5;
            word-break: break-word;
        }

        .review-badge {
            padding: 4px 16px;
            border-radius: 50px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            white-space: nowrap;
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
        }

        .badge-positive {
            background: rgba(209, 250, 229, 0.7);
            color: #065f46;
        }

        .badge-negative {
            background: rgba(254, 226, 226, 0.7);
            color: #991b1b;
        }

        .badge-neutral {
            background: rgba(254, 243, 199, 0.7);
            color: #92400e;
        }

        .badge-icon {
            font-size: 16px;
            margin-right: 4px;
        }

        .empty-state {
            text-align: center;
            padding: 56px 20px;
            color: #aac0d0;
        }

        .empty-state .big-icon {
            font-size: 60px;
            display: block;
            margin-bottom: 14px;
        }

        .empty-state p {
            font-size: 15px;
            color: #6a8a9a;
        }

        .empty-state .sub-text {
            font-size: 13px;
            color: #aac0d0;
            margin-top: 6px;
        }

        .footer {
            margin-top: 32px;
            padding-top: 20px;
            border-top: 1px solid rgba(173, 216, 230, 0.15);
            text-align: center;
            font-size: 13px;
            color: #8aaaba;
        }

        .review-list::-webkit-scrollbar {
            width: 4px;
        }

        .review-list::-webkit-scrollbar-track {
            background: rgba(173, 216, 230, 0.1);
            border-radius: 4px;
        }

        .review-list::-webkit-scrollbar-thumb {
            background: rgba(173, 216, 230, 0.3);
            border-radius: 4px;
        }

        .review-list::-webkit-scrollbar-thumb:hover {
            background: rgba(173, 216, 230, 0.5);
        }

        @media (max-width: 640px) {
            .container { 
                padding: 24px; 
            }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .header h1 { font-size: 24px; }
            .review-item { flex-direction: column; align-items: flex-start; gap: 6px; }
            .btn-primary { padding: 12px 20px; min-width: 120px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="icon">📊</span>
            <h1>Sentiment Analyzer</h1>
            <p>Analyze product reviews instantly with AI-powered sentiment analysis</p>
        </div>

        <form method="POST">
            <div class="input-section">
                <label for="reviews">📝 Enter Reviews (one per line)</label>
                <textarea 
                    id="reviews" 
                    name="reviews" 
                    placeholder="Example:&#10;This product is amazing! Best purchase ever.&#10;Poor quality, broke after 2 days.&#10;Good value for money, would recommend."
                >{{ reviews_text }}</textarea>
            </div>

            <div class="button-row">
                <button type="submit" class="btn-primary">🚀 Analyze Sentiment</button>
                <button type="reset" class="btn-clear" onclick="document.getElementById('reviews').value=''; this.form.submit();">✕ Clear</button>
            </div>
        </form>

        {% if results %}
        <div class="stats-grid">
            <div class="stat-card stat-total">
                <span class="number">{{ total }}</span>
                <span class="label">Total</span>
            </div>
            <div class="stat-card stat-positive">
                <span class="number">😊 {{ positive }}</span>
                <span class="label">Positive</span>
            </div>
            <div class="stat-card stat-negative">
                <span class="number">😠 {{ negative }}</span>
                <span class="label">Negative</span>
            </div>
            <div class="stat-card stat-neutral">
                <span class="number">😐 {{ neutral }}</span>
                <span class="label">Neutral</span>
            </div>
        </div>

        <div class="verdict {% if positive > negative %}positive{% elif negative > positive %}negative{% else %}neutral{% endif %}">
            {% if positive > negative %}
                ✅ Excellent Product!
                <span class="sub-text">{{ positive }}/{{ total }} customers are satisfied</span>
            {% elif negative > positive %}
                ❌ Poor Product!
                <span class="sub-text">{{ negative }}/{{ total }} customers are dissatisfied</span>
            {% else %}
                🟡 Mixed Reviews
                <span class="sub-text">Reviews are balanced — consider carefully</span>
            {% endif %}
        </div>

        <div class="results-section">
            <div class="section-header">
                <h3>📋 Review Analysis</h3>
                <span class="count-badge">{{ total }} reviews</span>
            </div>
            <div class="review-list">
                {% for review, sentiment in results %}
                <div class="review-item">
                    <span class="review-text">{{ review }}</span>
                    <span class="review-badge 
                        {% if sentiment == 'Positive' %}badge-positive{% elif sentiment == 'Negative' %}badge-negative{% else %}badge-neutral{% endif %}">
                        <span class="badge-icon">
                            {% if sentiment == 'Positive' %}😊{% elif sentiment == 'Negative' %}😠{% else %}😐{% endif %}
                        </span>
                        {{ sentiment }}
                    </span>
                </div>
                {% endfor %}
            </div>
        </div>

        {% else %}
        <div class="empty-state">
            <span class="big-icon">🔍</span>
            <p>Enter product reviews above and click <strong>Analyze Sentiment</strong></p>
            <div class="sub-text">Get instant insights on customer feedback</div>
        </div>
        {% endif %}

        <div class="footer">
            Built with ❤️ using Flask & TextBlob · 100% Free
        </div>
    </div>
</body>
</html>
"""

def analyze_sentiment(review):
    blob = TextBlob(review)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        reviews_text = request.form.get('reviews', '')
        reviews = [r.strip() for r in reviews_text.split('\n') if r.strip()]
        
        results = []
        for review in reviews:
            sentiment = analyze_sentiment(review)
            results.append((review, sentiment))
        
        positive = sum(1 for _, s in results if s == "Positive")
        negative = sum(1 for _, s in results if s == "Negative")
        neutral = sum(1 for _, s in results if s == "Neutral")
        
        return render_template_string(
            HTML_TEMPLATE,
            results=results,
            positive=positive,
            negative=negative,
            neutral=neutral,
            total=len(results),
            reviews_text=reviews_text
        )
    
    return render_template_string(HTML_TEMPLATE, results=None, reviews_text="")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
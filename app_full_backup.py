# ============================================
# E-COMMERCE SENTIMENT ANALYZER - FULL VERSION
# Uses Hugging Face Transformers (DistilBERT)
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
from transformers import pipeline
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from collections import Counter
import re
import random
from io import BytesIO
import base64

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="E-commerce Sentiment Analyzer",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .verdict-box {
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .positive-verdict {
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    .negative-verdict {
        background-color: #f8d7da;
        color: #721c24;
        border: 2px solid #f5c6cb;
    }
    .neutral-verdict {
        background-color: #fff3cd;
        color: #856404;
        border: 2px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD SENTIMENT MODEL (Cached for performance)
# ============================================
@st.cache_resource
def load_sentiment_model():
    """Load the pre-trained sentiment analysis model from Hugging Face"""
    try:
        # Using DistilBERT - small, fast, and accurate
        model = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        return model
    except Exception as e:
        st.error(f"⚠️ Error loading model: {str(e)}")
        st.info("💡 Using fallback mode with TextBlob")
        return None

# ============================================
# DATA LOADING FUNCTIONS
# ============================================
@st.cache_data
def load_sample_data():
    """Generate sample product reviews for demonstration"""
    sample_reviews = {
        'product': 'Sample Product - Wireless Headphones',
        'reviews': [
            "Amazing sound quality! Best purchase ever. Battery life is incredible.",
            "Poor build quality. Stopped working after 2 weeks. Not worth the price.",
            "Good value for money. Comfortable to wear for long hours.",
            "The sound is decent but the Bluetooth keeps disconnecting. Frustrating!",
            "Absolutely love these headphones! Noise cancellation is top-notch.",
            "Cheap materials used. The ear cushions started peeling after 1 month.",
            "Great product for this price range. Would recommend to friends.",
            "Battery doesn't last as advertised. Very disappointed.",
            "Excellent customer service. They replaced my defective unit quickly.",
            "Average product. Nothing special but gets the job done.",
            "Best headphones I've ever owned! 5 stars!",
            "The product looks good but the sound quality is mediocre.",
            "Very comfortable and lightweight. Perfect for workouts.",
            "Worst purchase ever! The left side stopped working in 3 days.",
            "Good product but the packaging was damaged during delivery.",
            "Amazing value! Works exactly as described. Highly recommended.",
            "The noise cancellation is good but the bass is weak.",
            "Decent product. Could be better for the price.",
            "Outstanding! Exceeded my expectations in every way.",
            "Do not buy this. It's a complete waste of money."
        ]
    }
    return sample_reviews

@st.cache_data
def load_amazon_data():
    """Load Amazon reviews dataset from Hugging Face or local CSV"""
    try:
        from datasets import load_dataset
        dataset = load_dataset("amazon_us_reviews", "Wireless_v1_00", split="train[:200]")
        reviews = dataset['review_body']
        return {'product': 'Amazon Wireless Products', 'reviews': reviews}
    except:
        # Fallback to sample data if dataset loading fails
        return load_sample_data()

@st.cache_data
def load_custom_data(uploaded_file):
    """Load custom CSV uploaded by user"""
    try:
        df = pd.read_csv(uploaded_file)
        if 'review' in df.columns or 'Review' in df.columns:
            review_col = 'review' if 'review' in df.columns else 'Review'
            reviews = df[review_col].tolist()
            product_name = df.columns[0] if len(df.columns) > 0 else "Custom Product"
            return {'product': product_name, 'reviews': reviews}
        else:
            st.error("⚠️ CSV must contain a 'review' or 'Review' column")
            return None
    except Exception as e:
        st.error(f"⚠️ Error loading CSV: {str(e)}")
        return None

# ============================================
# SENTIMENT ANALYSIS FUNCTIONS
# ============================================
def analyze_with_transformers(reviews, model):
    """Analyze sentiment using Hugging Face Transformers"""
    results = []
    for review in reviews:
        try:
            # Clean the review
            clean_review = re.sub(r'[^\w\s]', '', review)
            if len(clean_review) < 3:
                results.append({'label': 'NEUTRAL', 'score': 0.5})
                continue
            
            # Get prediction
            prediction = model(clean_review)[0]
            label = prediction['label']
            score = prediction['score']
            
            # Convert to Positive/Negative/Neutral
            if label == 'POSITIVE' and score > 0.6:
                sentiment = 'Positive'
            elif label == 'NEGATIVE' and score > 0.6:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
            
            results.append({
                'sentiment': sentiment,
                'score': score,
                'label': label
            })
        except:
            results.append({'sentiment': 'Neutral', 'score': 0.5, 'label': 'NEUTRAL'})
    
    return results

def analyze_with_textblob(reviews):
    """Fallback sentiment analysis using TextBlob"""
    results = []
    for review in reviews:
        blob = TextBlob(review)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            sentiment = 'Positive'
        elif polarity < -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        results.append({'sentiment': sentiment, 'score': abs(polarity), 'label': sentiment.upper()})
    return results

def analyze_reviews(reviews, model):
    """Main function to analyze reviews"""
    if model:
        return analyze_with_transformers(reviews, model)
    else:
        return analyze_with_textblob(reviews)

def extract_keywords(reviews, sentiment_type=None):
    """Extract common keywords from reviews"""
    words = []
    for review in reviews:
        if sentiment_type:
            # Filter by sentiment if specified
            pass
        blob = TextBlob(review)
        for word in blob.words:
            if len(word) > 3:
                words.append(word.lower())
    
    # Remove common stopwords
    stopwords = {'the', 'this', 'that', 'with', 'from', 'have', 'for', 'not', 
                 'but', 'are', 'you', 'can', 'will', 'was', 'were', 'they', 'your'}
    filtered_words = [w for w in words if w not in stopwords]
    
    counter = Counter(filtered_words)
    return counter.most_common(10)

# ============================================
# VISUALIZATION FUNCTIONS
# ============================================
def create_sentiment_pie_chart(df):
    """Create a pie chart of sentiment distribution"""
    sentiment_counts = df['Sentiment'].value_counts()
    
    colors = {
        'Positive': '#28a745',
        'Negative': '#dc3545',
        'Neutral': '#ffc107'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=sentiment_counts.index,
        values=sentiment_counts.values,
        hole=0.4,
        marker=dict(colors=[colors.get(s, '#gray') for s in sentiment_counts.index]),
        textinfo='label+percent',
        textposition='auto'
    )])
    
    fig.update_layout(
        title='Sentiment Distribution',
        height=400,
        showlegend=True
    )
    
    return fig

def create_sentiment_bar_chart(df):
    """Create a bar chart of sentiment distribution"""
    sentiment_counts = df['Sentiment'].value_counts()
    
    fig = px.bar(
        x=sentiment_counts.index,
        y=sentiment_counts.values,
        color=sentiment_counts.index,
        color_discrete_map={
            'Positive': '#28a745',
            'Negative': '#dc3545',
            'Neutral': '#ffc107'
        },
        title='Sentiment Distribution',
        labels={'x': 'Sentiment', 'y': 'Number of Reviews'}
    )
    
    fig.update_layout(
        height=400,
        showlegend=False
    )
    
    return fig

def create_wordcloud(reviews, sentiment_type=None):
    """Generate a word cloud from reviews"""
    if not reviews:
        return None
    
    # Combine all reviews
    text = ' '.join(reviews)
    
    # Create word cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    return fig

def create_confidence_histogram(df):
    """Create histogram of confidence scores"""
    fig = px.histogram(
        df,
        x='Confidence',
        nbins=20,
        title='Distribution of Confidence Scores',
        labels={'Confidence': 'Confidence Score', 'count': 'Number of Reviews'},
        color_discrete_sequence=['#17a2b8']
    )
    
    fig.update_layout(height=300)
    return fig

def create_sentiment_trend_plot(df):
    """Create a sentiment trend line (for chronological data)"""
    if 'index' not in df.columns:
        df = df.reset_index()
    
    # Convert sentiments to numeric values
    sentiment_map = {'Positive': 2, 'Neutral': 1, 'Negative': 0}
    df['Sentiment_Score'] = df['Sentiment'].map(sentiment_map)
    
    # Calculate rolling average
    df['Rolling_Avg'] = df['Sentiment_Score'].rolling(window=5, min_periods=1).mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['index'],
        y=df['Sentiment_Score'],
        mode='markers',
        name='Individual Reviews',
        marker=dict(color=df['Sentiment_Score'], colorscale='RdYlGn', showscale=False),
        text=df['Review'],
        hoverinfo='text'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['index'],
        y=df['Rolling_Avg'],
        mode='lines',
        name='Rolling Average (5 reviews)',
        line=dict(color='blue', width=3)
    ))
    
    fig.update_layout(
        title='Sentiment Trend',
        xaxis_title='Review Number',
        yaxis_title='Sentiment Score (0=Negative, 2=Positive)',
        height=300,
        showlegend=True
    )
    
    return fig

# ============================================
# UTILITY FUNCTIONS
# ============================================
def get_verdict(positive_count, negative_count, total):
    """Generate a verdict based on sentiment analysis"""
    positive_pct = (positive_count / total) * 100
    negative_pct = (negative_count / total) * 100
    neutral_pct = 100 - positive_pct - negative_pct
    
    if positive_pct > 50:
        return {
            'verdict': '✅ EXCELLENT PRODUCT!',
            'class': 'positive-verdict',
            'message': f'{positive_pct:.1f}% customers are satisfied with this product',
            'emoji': '🌟'
        }
    elif positive_pct > 35:
        return {
            'verdict': '👍 GOOD PRODUCT',
            'class': 'neutral-verdict',
            'message': f'{positive_pct:.1f}% positive reviews - generally well received',
            'emoji': '👌'
        }
    elif negative_pct > 50:
        return {
            'verdict': '❌ POOR PRODUCT!',
            'class': 'negative-verdict',
            'message': f'{negative_pct:.1f}% customers are dissatisfied - avoid buying',
            'emoji': '⚠️'
        }
    else:
        return {
            'verdict': '🟡 MIXED REVIEWS',
            'class': 'neutral-verdict',
            'message': 'Reviews are mixed - consider carefully before buying',
            'emoji': '🤔'
        }

def get_rating_recommendation(df):
    """Generate a 5-star rating recommendation based on sentiment"""
    sentiment_counts = df['Sentiment'].value_counts()
    positive = sentiment_counts.get('Positive', 0)
    negative = sentiment_counts.get('Negative', 0)
    total = len(df)
    
    # Calculate rating out of 5
    if total == 0:
        return 3.0
    
    # Weighted calculation
    positive_weight = 1.0
    negative_weight = 0.2
    neutral_weight = 0.6
    
    rating = ((positive * positive_weight) + (negative * negative_weight) + 
              ((total - positive - negative) * neutral_weight)) / total * 5
    
    return round(rating, 1)

def display_review_samples(df, sentiment_type, n=5):
    """Display sample reviews of a specific sentiment"""
    filtered = df[df['Sentiment'] == sentiment_type]
    if len(filtered) == 0:
        st.info(f"No {sentiment_type} reviews found")
        return
    
    samples = filtered.head(n)
    for _, row in samples.iterrows():
        st.write(f"• {row['Review'][:200]}..." if len(row['Review']) > 200 else f"• {row['Review']}")

# ============================================
# MAIN APPLICATION UI
# ============================================
def main():
    # Load model
    model = load_sentiment_model()
    
    # Header
    st.markdown('<p class="main-header">🛍️ E-commerce Sentiment Analyzer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analyze product reviews from ANY e-commerce website in seconds</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/sentiment-analysis.png", width=80)
        st.title("⚙️ Settings")
        
        # Data Source Selection
        data_source = st.radio(
            "📊 Choose Data Source:",
            ["📱 Sample Data", "🛒 Amazon Dataset", "📂 Upload CSV"]
        )
        
        st.divider()
        
        # Display settings
        st.subheader("🎨 Display Options")
        show_wordcloud = st.checkbox("Show Word Cloud", value=True)
        show_confidence = st.checkbox("Show Confidence Distribution", value=True)
        show_trend = st.checkbox("Show Sentiment Trend", value=True)
        show_sample_reviews = st.checkbox("Show Sample Reviews", value=True)
        
        st.divider()
        
        # Info
        st.info(
            "💡 **How it works:**\n\n"
            "1. Select data source\n"
            "2. Click 'Analyze' button\n"
            "3. Get instant sentiment analysis"
        )
        
        st.caption("Made with ❤️ | 100% Free | No API Costs")
    
    # Main content
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.subheader("📂 Select Product")
        product_name = st.text_input(
            "Product Name (optional):",
            placeholder="e.g., Wireless Headphones, Smart Watch, etc."
        )
    
    with col2:
        product_category = st.selectbox(
            "Product Category:",
            ["Electronics", "Clothing", "Books", "Beauty", "Home & Kitchen", "Sports", "Other"]
        )
    
    with col3:
        st.write("")
        st.write("")
        analyze_clicked = st.button("🔍 Analyze Sentiment", type="primary", use_container_width=True)
    
    # Data Loading Logic
    data = None
    if data_source == "📱 Sample Data":
        data = load_sample_data()
    elif data_source == "🛒 Amazon Dataset":
        data = load_amazon_data()
    elif data_source == "📂 Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV file with review column", type=['csv'])
        if uploaded_file:
            data = load_custom_data(uploaded_file)
    
    if data and analyze_clicked:
        reviews = data['reviews']
        product_name = product_name if product_name else data['product']
        
        # Display product info
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📦 Product", product_name)
        with col2:
            st.metric("📝 Total Reviews", len(reviews))
        with col3:
            st.metric("🏷️ Category", product_category)
        with col4:
            st.metric("🤖 Model", "DistilBERT" if model else "TextBlob (Fallback)")
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Analyze reviews
        status_text.text("🔄 Analyzing sentiments...")
        progress_bar.progress(30)
        
        results = analyze_reviews(reviews, model)
        
        progress_bar.progress(60)
        status_text.text("📊 Generating visualizations...")
        
        # Create DataFrame
        df = pd.DataFrame({
            'Review': reviews,
            'Sentiment': [r['sentiment'] for r in results],
            'Confidence': [r['score'] for r in results]
        })
        
        progress_bar.progress(80)
        status_text.text("📈 Creating dashboard...")
        
        # Calculate metrics
        sentiment_counts = df['Sentiment'].value_counts()
        positive_count = sentiment_counts.get('Positive', 0)
        negative_count = sentiment_counts.get('Negative', 0)
        neutral_count = sentiment_counts.get('Neutral', 0)
        
        # Rating
        rating = get_rating_recommendation(df)
        
        # Verdict
        verdict = get_verdict(positive_count, negative_count, len(df))
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        
        # ============================================
        # DASHBOARD
        # ============================================
        
        # Verdict Box
        st.markdown(f"""
        <div class="verdict-box {verdict['class']}">
            {verdict['verdict']}<br>
            <span style="font-size: 1rem;">{verdict['message']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Key Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("😊 Positive", f"{positive_count} ({positive_count/len(df)*100:.1f}%)", delta=f"{positive_count/len(df)*100:.1f}%")
        with col2:
            st.metric("😠 Negative", f"{negative_count} ({negative_count/len(df)*100:.1f}%)", delta=f"{negative_count/len(df)*100:.1f}%", delta_color="inverse")
        with col3:
            st.metric("🟡 Neutral", f"{neutral_count} ({neutral_count/len(df)*100:.1f}%)")
        with col4:
            st.metric("⭐ Rating", f"{rating}/5.0")
        with col5:
            st.metric("🎯 Accuracy", f"{df['Confidence'].mean()*100:.1f}%")
        
        st.divider()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie Chart
            pie_chart = create_sentiment_pie_chart(df)
            st.plotly_chart(pie_chart, use_container_width=True)
        
        with col2:
            # Bar Chart
            bar_chart = create_sentiment_bar_chart(df)
            st.plotly_chart(bar_chart, use_container_width=True)
        
        # Word Cloud
        if show_wordcloud:
            st.subheader("☁️ Word Cloud")
            wordcloud_fig = create_wordcloud(reviews)
            if wordcloud_fig:
                st.pyplot(wordcloud_fig)
        
        # Additional Charts
        if show_confidence:
            conf_chart = create_confidence_histogram(df)
            st.plotly_chart(conf_chart, use_container_width=True)
        
        if show_trend and len(df) > 5:
            trend_chart = create_sentiment_trend_plot(df)
            st.plotly_chart(trend_chart, use_container_width=True)
        
        # Sample Reviews
        if show_sample_reviews:
            st.subheader("📝 Sample Reviews")
            
            tabs = st.tabs(["😊 Positive", "😠 Negative", "🟡 Neutral"])
            
            with tabs[0]:
                display_review_samples(df, 'Positive')
            
            with tabs[1]:
                display_review_samples(df, 'Negative')
            
            with tabs[2]:
                display_review_samples(df, 'Neutral')
        
        # Top Keywords
        st.subheader("🔑 Top Keywords")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Positive Keywords**")
            positive_reviews = df[df['Sentiment'] == 'Positive']['Review'].tolist()
            positive_keywords = extract_keywords(positive_reviews)
            for word, count in positive_keywords[:5]:
                st.write(f"• {word}: {count} mentions")
        
        with col2:
            st.write("**Negative Keywords**")
            negative_reviews = df[df['Sentiment'] == 'Negative']['Review'].tolist()
            negative_keywords = extract_keywords(negative_reviews)
            for word, count in negative_keywords[:5]:
                st.write(f"• {word}: {count} mentions")
        
        # Download Results
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name=f"sentiment_analysis_{product_name.replace(' ', '_')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Summary report
            summary = f"""
            SENTIMENT ANALYSIS REPORT
            ============================
            Product: {product_name}
            Category: {product_category}
            Total Reviews: {len(df)}
            
            Sentiment Breakdown:
            - Positive: {positive_count} ({positive_count/len(df)*100:.1f}%)
            - Negative: {negative_count} ({negative_count/len(df)*100:.1f}%)
            - Neutral: {neutral_count} ({neutral_count/len(df)*100:.1f}%)
            
            Rating: {rating}/5.0
            Verdict: {verdict['verdict']}
            """
            
            st.download_button(
                label="📄 Download Summary Report",
                data=summary,
                file_name=f"summary_report_{product_name.replace(' ', '_')}.txt"
            )
        
        with col3:
            # Share button
            st.button("📤 Share Results", use_container_width=True)
        
        # Success message
        st.success("✅ Analysis complete! The sentiment analysis was performed 100% free using open-source models.")
        
        # Footer
        st.divider()
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            🚀 Built with Streamlit, Hugging Face Transformers & Plotly | 100% Free & Open Source
        </div>
        """, unsafe_allow_html=True)
        
        # Clear progress bar
        progress_bar.empty()
        status_text.empty()
    
    elif not data and analyze_clicked:
        st.warning("⚠️ Please select a data source or upload a CSV file")

# ============================================
# RUN THE APP
# ============================================
if __name__ == "__main__":
    main()
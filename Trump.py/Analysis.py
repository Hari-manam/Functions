# ✅ FINAL TRUMP PROJECT ANALYSIS with LDA and Hypothesis Visualizations ✅

import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import numpy as np
import seaborn as sns
import scipy.stats as stats

# Load datasets
trends = pd.read_csv(r'C:\Users\nanim\OneDrive\Desktop\Gen AI\Trump.py\Cleaned_Trump_Google_Trends.csv', parse_dates=['Week'])
youtube = pd.read_csv(r'C:\Users\nanim\OneDrive\Desktop\Gen AI\Trump.py\Cleaned_YouTube_Trump_Videos.csv')
cnn = pd.read_csv(r'C:\Users\nanim\OneDrive\Desktop\Gen AI\Trump.py\CNN_Trump_Politics2024_Cleaned.csv', engine='python')
fox = pd.read_csv(r'C:\Users\nanim\OneDrive\Desktop\Gen AI\Trump.py\FoxNews_Expert_Opinions.csv', engine='python')
truth = pd.read_csv(r'C:\Users\nanim\OneDrive\Desktop\Gen AI\Trump.py\trump_truths_dataset_cleaned.csv', engine='python', parse_dates=['post_date'])

# Sentiment Analysis on Truth Social Posts
analyzer = SentimentIntensityAnalyzer()
truth = truth.dropna(subset=['post_date', 'status_text'])
truth['compound'] = truth['status_text'].apply(lambda text: analyzer.polarity_scores(str(text))['compound'])
truth['week_end'] = truth['post_date'].apply(lambda dt: (dt + timedelta(days=(6 - dt.weekday()))).date())
weekly_sentiment = truth.groupby('week_end', as_index=False)['compound'].mean()
weekly_sentiment.rename(columns={'compound': 'avg_sentiment'}, inplace=True)
weekly_sentiment['week_end'] = pd.to_datetime(weekly_sentiment['week_end'])

# Merge for correlation
merged = pd.merge(weekly_sentiment, trends, left_on='week_end', right_on='Week', how='inner')

# ✅ Visualization - Truth Social Weekly Sentiment
plt.figure(figsize=(10, 5))
sns.lineplot(data=weekly_sentiment, x='week_end', y='avg_sentiment')
plt.title("Weekly Average Sentiment on Trump's Truth Social")
plt.xlabel('Week')
plt.ylabel('Average Compound Sentiment')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ✅ YouTube Title Sentiment with Better Visualization
youtube = youtube.dropna(subset=['Title'])
youtube['Sentiment'] = youtube['Title'].apply(lambda t: analyzer.polarity_scores(str(t))['compound'])
plt.figure(figsize=(14, 6))
colors = ['green' if x > 0 else 'red' for x in youtube['Sentiment']]
plt.bar(youtube['Title'], youtube['Sentiment'], color=colors)
plt.title('YouTube Video Title Sentiment')
plt.xlabel('Video Title')
plt.ylabel('Compound Sentiment')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# ✅ Google Trends Line Plot
trend_cols = [col for col in trends.columns if col != 'Week']
plt.figure(figsize=(15, 7))
for col in trend_cols:
    plt.plot(trends['Week'], trends[col], label=col)
plt.legend()
plt.title('Google Trends Over Time')
plt.xlabel('Week')
plt.ylabel('Trend Index')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ✅ LDA Topic Modeling - Visualize Top Words
pattern = re.compile(r'RELATED ARTICLE[^\n]*\n[^\n]*(\n|$)', flags=re.IGNORECASE)
cnn['Content'] = cnn['Content'].str.replace(pattern, '', regex=True).str.replace('\n', ' ', regex=True)
fox['Content'] = fox['Content'].str.replace('CLICK HERE FOR MORE FOX NEWS OPINION', '', case=False).str.replace('\n', ' ', regex=True)
cnn = cnn.dropna(subset=['Content'])
fox = fox.dropna(subset=['Content'])

for df, name, n_topics in zip([cnn, fox], ['CNN', 'FOX'], [3, 5]):
    vectorizer = CountVectorizer(stop_words='english', max_df=0.9, min_df=2)
    X = vectorizer.fit_transform(df['Content'])
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)
    feature_names = vectorizer.get_feature_names_out()

    # Visualize each topic as bar plot
    for topic_idx, topic in enumerate(lda.components_):
        top_indices = topic.argsort()[:-11:-1]
        top_words = [feature_names[i] for i in top_indices]
        top_values = topic[top_indices]

        plt.figure(figsize=(8, 4))
        sns.barplot(x=top_values, y=top_words)
        plt.title(f"{name} - Topic {topic_idx + 1}")
        plt.xlabel('Word Importance')
        plt.tight_layout()
        plt.show()

# ✅ Hypothesis Test - Sentiment Change Visualization
cutoff_date = pd.to_datetime('2024-08-01')
before = weekly_sentiment[weekly_sentiment['week_end'] < cutoff_date]['avg_sentiment']
after = weekly_sentiment[weekly_sentiment['week_end'] >= cutoff_date]['avg_sentiment']

plt.figure(figsize=(8, 5))
sns.boxplot(data=[before, after], palette=['orange', 'blue'])
plt.xticks([0, 1], ['Before Aug 2024', 'After Aug 2024'])
plt.title('Truth Social Sentiment Before vs After Aug 2024')
plt.ylabel('Average Sentiment')
plt.tight_layout()
plt.show()

if len(before) > 1 and len(after) > 1:
    t_stat, p_val = stats.ttest_ind(before, after)
    print(f"\nHypothesis Test - Sentiment Change Before/After Aug 2024")
    print(f"T-statistic: {round(t_stat, 3)}, P-value: {round(p_val, 4)}")
else:
    print("\nHypothesis Test skipped due to insufficient data before/after cutoff.")

# ✅ Correlation Calculation
print("\nCorrelation between Truth Social Sentiment and Google Trends:")
for col in trend_cols:
    corr = merged['avg_sentiment'].corr(merged[col])
    print(f"Correlation with {col}: {round(corr, 3)}")

print('\n✅ Project Complete: LDA and Hypothesis now visualized ✅')
# Task_03_Descriptive_Stats

This repository provides a comprehensive data analysis project focused on calculating descriptive statistics using various Python libraries and methodologies.

## Project Structure

The repository is organized as follows:

.  
├── README.md                
├── requirements.txt  
├── pure_python.py          
├── pandas_python.py       
├── polars_python.py       
└── visualizations.py     

## Setup and Installation

To get started with this project, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/Task_03_Descriptive_Stats.git
    cd Task_03_Descriptive_Stats
    ```

2.  **Create and activate a virtual environment** (recommended for managing dependencies):
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Each analysis script can be executed independently from the command line:

```bash
python <script_name.py>
```

For example, to run the Pandas analysis script:
```bash
python pure_python.py
```

## Data Analysis Approach

The analysis is performed using three different approaches:

1. **Pure Python**: Uses only the Python standard library for foundational statistical analysis.
2. **Pandas**: Leverages pandas DataFrames for streamlined data manipulation and summary.
3. **Polars**: Utilizes Polars for high-performance, efficient analysis on large-scale tabular data.

For each script and dataset, the following statistics are computed:
- **Count**: Number of observations.
- **Mean, Min, Max**: Central tendency and spread for numeric columns.
- **Standard Deviation**: Measure of dispersion.
- **Unique Value Counts & Most Frequent Values**: For categorical columns.

**Levels of analysis include:**
1. **Overall dataset**
2. **Grouped by page or account ID**
3. **Grouped by (page_id, ad_id) or (Facebook_Id, post_id) as applicable**

---

## Key Findings

### Facebook Ads Dataset (`2024_fb_ads_president_scored_anon_stats.txt`)

- **Ad Reach & Spending**
  - Average estimated audience size: ~556,463 people
  - Average impressions per ad: ~45,602
  - Mean ad spend: $1,061 (Max spend: $474,999)
- **Message Types**
  - 57% of ads contain calls to action (CTA)
  - 55% use advocacy messaging
  - 38% focus on issue-based topics; 27% are attack messages
  - 22% of ads are image-based
- **Campaign Topics**
  - Most discussed: Economy (12%), Health (11%), Social/Cultural (11%), Women’s issues (8%)
- **Content Integrity**
  - ~7% of ads flagged as potential scam; ~5% flagged for election integrity concerns
  - Incivility is generally rare

### Facebook Posts Dataset (`2024_fb_posts_president_scored_anon_stats.txt`)

- **Engagement Metrics**
  - Large variation in engagement (mean interactions: 4,190; mean shares: 320)
  - Strong correlation between comments, shares, and reactions
  - “Love” and “Angry” reactions are prominent indicators of audience sentiment
- **Content Types & Topics**
  - Advocacy (mean 0.55), CTA (0.13), attack (0.21), issue-focused (0.46)
  - Most common topics: Economy (9%), Health (4.8%), Social/Cultural (6%)
  - Fraud and scam content are present but not dominant (fraud mean ~0.86%, scam ~2%)
- **Audience & Administration**
  - The majority of posts are by pages categorized as "PERSON" and administered from the US
  - Post types include links, photos, videos, and text
  - High degree of unique content (many posts have unique timestamps or IDs)

### Twitter Posts Dataset (`2024_tw_posts_president_scored_anon_stats.txt`)

- **Engagement**
  - Very high average like count (6,913) and retweets (1,322), but with extreme variance
  - Average reply count: 1,063; average quote count: 128
- **Message & Topic Types**
  - Advocacy (mean 0.56), issue (0.50), attack (0.31), CTA (0.10)
  - Most common topics: Economy (16%), Health (5.5%), Social/Cultural (5%)
- **Content Integrity & Diversity**
  - Fraud, scam, incivility, and election integrity are rare but present (each <2% mean)
  - Wide language and source diversity, but English and Twitter Web App dominate

### Cross-Platform Insights

- **Topic Consistency**
  - Top topics (economy, health, social issues) are common across Facebook and Twitter.
- **Platform-Specific Trends**
  - Facebook ads are more likely to use direct advocacy and CTA messaging.
  - Twitter content is more volatile, with higher peaks in engagement metrics.
- **Audience Engagement**
  - Facebook’s paid reach (ads) is cost-intensive but delivers high impressions; organic posts vary widely.
  - Twitter posts can go viral, especially for political or advocacy content.

---

## Visualizations

All visualizations are saved in the `visualizations/` directory, organized by dataset for easy reference. The following types of plots are generated for each dataset:

- **Histograms with KDE curves**: Visualize the distribution of numeric variables, revealing skew, outliers, and modal patterns.
- **Boxplots**: Summarize the spread and highlight outliers for each numeric column.
- **Bar plots**: Display the frequency of top categorical values (e.g., most common topics, message types, sources).
- **Correlation heatmaps**: Show relationships between numeric variables, indicating which metrics move together.
- **Interactive scatterplot matrices (Plotly)**: Enable multivariate exploration of numeric variables in a browser.
- **Interactive bar charts (Plotly)**: Allow dynamic exploration of the most frequent categorical values.
- **Time series plots**: (If a date or time column is available) Visualize trends in numeric variables over time (e.g., daily engagement, ad spend).
- **Executive summary text files**: Each dataset directory includes an automatically generated narrative of key trends and findings.

---

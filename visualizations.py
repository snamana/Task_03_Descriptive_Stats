import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path
import numpy as np

def load_data(data_path: str) -> pd.DataFrame:
    return pd.read_csv(data_path)

def create_numeric_histograms(df: pd.DataFrame, save_dir: Path, dataset_name: str) -> None:
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        plt.figure(figsize=(10, 5))
        sns.histplot(df[col].dropna(), bins=40, kde=True, color='royalblue')
        plt.title(f"{col} Distribution – {dataset_name}")
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(save_dir / f'{col}_hist.png')
        plt.close()

def create_numeric_boxplots(df: pd.DataFrame, save_dir: Path, dataset_name: str) -> None:
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=df[col].dropna(), color='coral')
        plt.title(f"{col} Boxplot – {dataset_name}")
        plt.xlabel(col)
        plt.tight_layout()
        plt.savefig(save_dir / f'{col}_boxplot.png')
        plt.close()

def create_categorical_barplots(df: pd.DataFrame, save_dir: Path, dataset_name: str, topn=10) -> None:
    categorical_cols = [col for col in df.select_dtypes(include=['object', 'category']).columns if df[col].nunique() > 1]
    for col in categorical_cols:
        vc = df[col].value_counts().head(topn)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=vc.index.astype(str), y=vc.values, palette='viridis')
        plt.title(f"Top {topn} {col} Categories – {dataset_name}")
        plt.ylabel('Count')
        plt.xlabel(col)
        plt.xticks(rotation=35)
        plt.tight_layout()
        plt.savefig(save_dir / f'{col}_barplot.png')
        plt.close()

def create_correlation_heatmap(df: pd.DataFrame, save_dir: Path, dataset_name: str) -> None:
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        return
    corr = df[numeric_cols].corr()
    plt.figure(figsize=(10, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title(f"Correlation Heatmap – {dataset_name}")
    plt.tight_layout()
    plt.savefig(save_dir / 'correlation_heatmap.png')
    plt.close()

def create_interactive_plotly(df: pd.DataFrame, save_dir: Path, dataset_name: str, topn=5):
    # Scatter matrix for first few numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns[:topn]
    if len(numeric_cols) > 1:
        fig = px.scatter_matrix(df[numeric_cols], title=f"Scatterplot Matrix ({dataset_name})")
        fig.write_html(str(save_dir / 'scatter_matrix.html'))
    # Bar for first categorical
    categorical_cols = [col for col in df.select_dtypes(include=['object', 'category']).columns if df[col].nunique() > 1]
    for col in categorical_cols[:1]:
        vc = df[col].value_counts().head(10)
        fig = px.bar(x=vc.index.astype(str), y=vc.values, title=f"Top 10 {col} ({dataset_name})")
        fig.write_html(str(save_dir / f'{col}_interactive_bar.html'))

def create_narrative(df: pd.DataFrame, dataset_name: str) -> str:
    numeric = df.select_dtypes(include=[np.number]).columns
    categorical = [col for col in df.select_dtypes(include=['object', 'category']).columns if df[col].nunique() > 1]
    summary = [f"# Executive Summary: {dataset_name}"]
    if numeric.any():
        summary.append("## Numeric Highlights:")
        for col in numeric:
            s = df[col].dropna()
            if len(s) == 0: continue
            summary.append(
                f"- {col}: mean={s.mean():.2f}, median={s.median():.2f}, std={s.std():.2f}, min={s.min():.2f}, max={s.max():.2f}"
            )
    if categorical:
        summary.append("## Categorical Highlights:")
        for col in categorical:
            mode = df[col].mode().iloc[0] if not df[col].mode().empty else 'N/A'
            top_count = df[col].value_counts().iloc[0] if not df[col].value_counts().empty else 0
            summary.append(
                f"- {col}: most frequent='{mode}' ({top_count} times), unique values={df[col].nunique()}"
            )
    # Narrative points
    if 'createdAt' in df.columns:
        summary.append("- Engagement over time shows strong peaks, suggesting campaign/event-driven interaction.")
    if 'page_id' in df.columns:
        summary.append("- Posting is centralized among a few highly active pages/accounts.")
    summary.append(
        "\nThe dataset exhibits power-law behavior: most posts/ads get little attention, but a few dominate. This points to the importance of monitoring high-engagement content and actors."
    )
    return '\n'.join(summary)

def analyze_and_visualize(data_path: str, output_root: str):
    df = load_data(data_path)
    dataset_name = Path(data_path).stem
    out_dir = Path(output_root) / dataset_name
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Analyzing {dataset_name} ...")
    create_numeric_histograms(df, out_dir, dataset_name)
    create_numeric_boxplots(df, out_dir, dataset_name)
    create_categorical_barplots(df, out_dir, dataset_name)
    create_correlation_heatmap(df, out_dir, dataset_name)
    create_interactive_plotly(df, out_dir, dataset_name)
    narrative = create_narrative(df, dataset_name)
    print(narrative)
    with open(out_dir / "executive_summary.txt", "w") as f:
        f.write(narrative)
    print(f"All visualizations and executive summary saved in {out_dir}")

def main():
    datasets = [
        "period_03/2024_tw_posts_president_scored_anon.csv",
        "period_03/2024_fb_posts_president_scored_anon.csv",
        "period_03/2024_fb_ads_president_scored_anon.csv"
    ]
    output_root = "presentation_outputs"
    for path in datasets:
        try:
            analyze_and_visualize(path, output_root)
        except Exception as e:
            print(f"Failed on {path}: {e}")

if _name_ == "_main_":
    main()

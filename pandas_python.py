
import pandas as pd
from pathlib import Path

def infer_types(df):
    num_cols = df.select_dtypes('number').columns.tolist()
    cat_cols = [c for c in df.columns if c not in num_cols]
    return num_cols, cat_cols

def summarize(df, num_cols, cat_cols):
    stats = {}
    for col in num_cols:
        s = df[col].dropna()
        stats[col] = {
            'count': s.count(),
            'mean': s.mean(),
            'min': s.min(),
            'max': s.max(),
            'std': s.std()
        }
    for col in cat_cols:
        s = df[col].dropna()
        stats[col] = {
            'count': s.count(),
            'unique': s.nunique(),
            'mode': s.mode().iloc[0] if not s.mode().empty else None,
            'mode_count': s.value_counts().iloc[0] if not s.value_counts().empty else None
        }
    return stats

def auto_group_keys(df):
    columns = df.columns
    if 'page_id' in columns and 'ad_id' in columns:
        return [['page_id'], ['page_id', 'ad_id']]
    if 'Facebook_Id' in columns and 'post_id' in columns:
        return [['Facebook_Id'], ['Facebook_Id', 'post_id']]
    if 'id' in columns:
        keys = [['id']]
        if 'inReplyToId' in columns:
            keys.append(['inReplyToId'])
        return keys
    return []

def write_results(filepath, overall, group_stats):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("==== OVERALL ====\n")
        for col, stats in overall.items():
            f.write(f"{col}:\n")
            for k, v in stats.items():
                f.write(f"  {k}: {v}\n")
        for group, results in group_stats.items():
            f.write(f"\n==== GROUP: {group} ====\n")
            for col, stats in results.items():
                f.write(f"{col}:\n")
                for k, v in stats.items():
                    f.write(f"  {k}: {v}\n")

def main():
    data_files = [
        "2024_fb_ads_president_scored_anon.csv",
        "2024_fb_posts_president_scored_anon.csv",
        "2024_tw_posts_president_scored_anon.csv"
    ]
    output_dir = Path("pandas_results")
    output_dir.mkdir(exist_ok=True)
    for path in data_files:
        print(f"\nAnalyzing {path}")
        df = pd.read_csv(path)
        num_cols, cat_cols = infer_types(df)
        overall = summarize(df, num_cols, cat_cols)
        group_stats = {}
        for keys in auto_group_keys(df):
            grouped = df.groupby(keys)
            sample_key = next(iter(grouped.groups))
            group_df = grouped.get_group(sample_key)
            group_stats[str(keys) + " = " + str(sample_key)] = summarize(group_df, num_cols, cat_cols)
        result_file = output_dir / f"{Path(path).stem}_stats.txt"
        write_results(result_file, overall, group_stats)
        print(f"Results for {path} saved to {result_file}")

if _name_ == "_main_":
    main()

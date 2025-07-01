import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Dict, Any, Tuple

def try_float(s):
    try:
        return float(str(s).replace(',', '').strip())
    except (ValueError, AttributeError):
        return None

def infer_column_types(rows, sample_size=20):
    if not rows:
        return set(), set()
    cols = rows[0].keys()
    numeric, categorical = set(), set()
    for col in cols:
        floats = [try_float(row[col]) for row in rows[:sample_size]]
        n_floats = sum(v is not None for v in floats)
        if n_floats >= 0.8 * len(floats):
            numeric.add(col)
        else:
            categorical.add(col)
    return numeric, categorical

def compute_numeric_stats(values):
    vals = [try_float(v) for v in values if try_float(v) is not None]
    n = len(vals)
    if not n:
        return {}
    mean = sum(vals) / n
    minv, maxv = min(vals), max(vals)
    std = math.sqrt(sum((x - mean) ** 2 for x in vals) / (n - 1)) if n > 1 else 0
    return {'count': n, 'mean': mean, 'min': minv, 'max': maxv, 'std': std}

def compute_categorical_stats(values):
    vals = [v for v in values if v and v.strip().upper() not in ('NA', 'N/A', 'NULL')]
    counter = Counter(vals)
    n = len(vals)
    if not n:
        return {}
    most_common, most_count = counter.most_common(1)[0]
    return {'count': n, 'unique': len(counter), 'mode': most_common, 'mode_count': most_count}

def analyze_group(rows, num_cols, cat_cols):
    stats = {}
    for col in num_cols:
        stats[col] = compute_numeric_stats([row[col] for row in rows if col in row])
    for col in cat_cols:
        stats[col] = compute_categorical_stats([row[col] for row in rows if col in row])
    return stats

def aggregate_by_keys(rows, keys):
    agg = defaultdict(list)
    for row in rows:
        try:
            key = tuple(row[k] for k in keys)
            agg[key].append(row)
        except KeyError:
            continue
    return agg

def read_csv_rows(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def auto_group_keys(columns):
    if 'page_id' in columns and 'ad_id' in columns:
        return [('page_id',), ('page_id', 'ad_id')]
    if 'Facebook_Id' in columns and 'post_id' in columns:
        return [('Facebook_Id',), ('Facebook_Id', 'post_id')]
    if 'id' in columns:
        keys = [('id',)]
        if 'inReplyToId' in columns:
            keys.append(('inReplyToId',))
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
    output_dir = Path("pure_python_results")
    output_dir.mkdir(exist_ok=True)
    for path in data_files:
        print(f"\nAnalyzing {path}")
        rows = read_csv_rows(path)
        if not rows:
            print(f"{path} is empty or missing.")
            continue
        columns = rows[0].keys()
        num_cols, cat_cols = infer_column_types(rows)
        overall = analyze_group(rows, num_cols, cat_cols)
        group_stats = {}
        for keys in auto_group_keys(columns):
            grouped = aggregate_by_keys(rows, list(keys))
            sample_key = next(iter(grouped))
            group_stats[str(keys) + " = " + str(sample_key)] = analyze_group(grouped[sample_key], num_cols, cat_cols)
        result_file = output_dir / f"{Path(path).stem}_stats.txt"
        write_results(result_file, overall, group_stats)
        print(f"Results for {path} saved to {result_file}")

if _name_ == "_main_":
    main()

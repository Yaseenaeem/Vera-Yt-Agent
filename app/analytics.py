import pandas as pd
import isodate
from datetime import datetime, timezone
from typing import Dict, Any, Tuple

def process_youtube_dataset(raw_videos: list) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """
    Normalizes YouTube API JSON payloads into structured metrics using Pandas.
    Calculates Views-Per-Day, RPI, Shorts classification, and statistical quartiles.
    """
    if not raw_videos:
        return {}, pd.DataFrame()

    df = pd.DataFrame(raw_videos)

    # 1. Parse ISO 8601 duration (e.g. PT1M15S -> 75 seconds)
    def parse_duration_to_sec(duration_str):
        if not duration_str or not isinstance(duration_str, str):
            return 0
        try:
            return isodate.parse_duration(duration_str).total_seconds()
        except Exception:
            return 0

    df["duration_sec"] = df["duration"].apply(parse_duration_to_sec)
    
    # Flag YouTube Shorts (60 seconds or less)
    df["is_short"] = df["duration_sec"] <= 60

    # 2. Time-decay calculation (Days Active)
    now = datetime.now(timezone.utc)
    df["published_at_dt"] = pd.to_datetime(df["published_at"])
    df["days_old"] = (now - df["published_at_dt"]).dt.days.clip(lower=1)

    # 3. Views Per Day (VPD) Velocity Metric
    df["views_per_day"] = df["view_count"] / df["days_old"]

    # 4. Relative Performance Index (RPI) calculation
    median_views = df["view_count"].median()
    df["rpi"] = df["view_count"] / (median_views if median_views > 0 else 1)

    # 5. Quartile Splitting (Top 25% vs Bottom 25%)
    rpi_75th = df["rpi"].quantile(0.75)
    rpi_25th = df["rpi"].quantile(0.25)

    top_performers = df[df["rpi"] >= rpi_75th]
    weak_performers = df[df["rpi"] <= rpi_25th]

    # Clean statistical summary for LLM context injection
    summary = {
        "sample_size": int(len(df)),
        "median_views": int(median_views),
        "shorts_ratio": float(df["is_short"].sum() / len(df)),
        "avg_views_per_day": float(df["views_per_day"].mean()),
        "top_quartile_titles": top_performers["title"].tolist(),
        "bottom_quartile_titles": weak_performers["title"].tolist(),
        "top_quartile_avg_vpd": float(top_performers["views_per_day"].mean()) if not top_performers.empty else 0.0,
        "bottom_quartile_avg_vpd": float(weak_performers["views_per_day"].mean()) if not weak_performers.empty else 0.0
    }

    return summary, df
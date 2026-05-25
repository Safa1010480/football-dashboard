import pandas as pd

def load_data(filepath):
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['decade'] = (df['year'] // 10) * 10
    df['home_score'] = pd.to_numeric(df['home_score'], errors='coerce')
    df['away_score'] = pd.to_numeric(df['away_score'], errors='coerce')
    df = df.dropna(subset=['home_score', 'away_score'])
    df['total_goals'] = df['home_score'] + df['away_score']
    df['outcome'] = df.apply(
        lambda r: 'Home Win' if r['home_score'] > r['away_score']
        else ('Away Win' if r['away_score'] > r['home_score'] else 'Draw'), axis=1
    )
    return df

def apply_filters(df, year_range, tournaments, teams, score_range, search_text):
    df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    if tournaments:
        df = df[df['tournament'].isin(tournaments)]
    if teams:
        df = df[(df['home_team'].isin(teams)) | (df['away_team'].isin(teams))]
    df = df[(df['total_goals'] >= score_range[0]) & (df['total_goals'] <= score_range[1])]
    if search_text and search_text.strip():
        q = search_text.strip()
        mask = (
            df['home_team'].str.contains(q, case=False, na=False) |
            df['away_team'].str.contains(q, case=False, na=False) |
            df['city'].str.contains(q, case=False, na=False) |
            df['country'].str.contains(q, case=False, na=False)
        )
        df = df[mask]
    return df.reset_index(drop=True)

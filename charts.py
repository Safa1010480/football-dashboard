import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd

C1 = "#00d4ff"
C2 = "#00ff87"
C3 = "#ffffff"
BLUES = "cool"

def set_style():
    sns.set_theme(style="whitegrid", font_scale=1.05)
    matplotlib.rcParams.update({
        "figure.facecolor": "#0a0e1a",
        "axes.facecolor": "#0d1117",
        "axes.titleweight": "bold", "axes.titlecolor": "#00d4ff", "axes.labelcolor": "#ffffff", "xtick.color": "#aaaaaa", "ytick.color": "#aaaaaa", "text.color": "#ffffff",
        "axes.titlesize": 13,
        "axes.labelsize": 11,
    })

def pie_chart(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    counts = df['outcome'].value_counts()
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%',
           colors=[C1, C2, C3][:len(counts)], startangle=90,
           wedgeprops=dict(edgecolor='white', linewidth=1.5))
    ax.set_title('Match Outcome Distribution', pad=15)
    return fig

def histogram(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(df['total_goals'], bins=range(0, int(df['total_goals'].max()) + 2),
            color=C1, edgecolor='white', linewidth=0.6)
    ax.set_title('Goals Per Match Distribution')
    ax.set_xlabel('Total Goals')
    ax.set_ylabel('Number of Matches')
    ax.axvline(df['total_goals'].mean(), color=C3, linewidth=2,
               linestyle='--', label=f"Mean: {df['total_goals'].mean():.1f}")
    ax.legend()
    plt.tight_layout()
    return fig

def line_chart(df):
    fig, ax = plt.subplots(figsize=(9, 4))
    yearly = df.groupby('year').size().reset_index(name='matches')
    ax.plot(yearly['year'], yearly['matches'], color=C1, linewidth=2)
    ax.fill_between(yearly['year'], yearly['matches'], alpha=0.15, color=C1)
    ax.set_title('International Matches Played Per Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Matches')
    plt.tight_layout()
    return fig

def bar_chart(df):
    fig, ax = plt.subplots(figsize=(9, 5))
    home_wins = df[df['home_score'] > df['away_score']]['home_team'].value_counts()
    away_wins = df[df['away_score'] > df['home_score']]['away_team'].value_counts()
    total_wins = home_wins.add(away_wins, fill_value=0).nlargest(10)
    sns.barplot(x=total_wins.values, y=total_wins.index, palette=BLUES, ax=ax)
    ax.set_title('Top 10 Teams by Total Wins')
    ax.set_xlabel('Total Wins')
    ax.set_ylabel('Team')
    plt.tight_layout()
    return fig

def scatter_plot(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    sample = df.sample(min(3000, len(df)), random_state=42)
    ax.scatter(sample['home_score'], sample['away_score'],
               alpha=0.25, color=C1, s=15, edgecolors='none')
    ax.set_title('Home Goals vs Away Goals')
    ax.set_xlabel('Home Goals')
    ax.set_ylabel('Away Goals')
    mx = max(sample['home_score'].max(), sample['away_score'].max())
    ax.plot([0, mx], [0, mx], color=C3, linewidth=1.2, linestyle='--', label='Equal score')
    ax.legend(fontsize=9)
    plt.tight_layout()
    return fig

def box_plot(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    top_t = df['tournament'].value_counts().nlargest(6).index
    subset = df[df['tournament'].isin(top_t)]
    order = subset.groupby('tournament')['total_goals'].median().sort_values(ascending=False).index
    sns.boxplot(data=subset, x='tournament', y='total_goals', order=order, palette="Blues", ax=ax)
    ax.set_title('Goal Distribution by Top Tournaments')
    ax.set_xlabel('Tournament')
    ax.set_ylabel('Total Goals')
    ax.tick_params(axis='x', rotation=25)
    plt.tight_layout()
    return fig

def heatmap(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    corr = df[['home_score', 'away_score', 'total_goals', 'year']].corr()
    sns.heatmap(corr, annot=True, cmap='Blues', fmt='.2f', linewidths=0.5, ax=ax)
    ax.set_title('Feature Correlation Heatmap')
    plt.tight_layout()
    return fig

def area_chart(df):
    fig, ax = plt.subplots(figsize=(9, 4))
    avg = df.groupby('decade')['total_goals'].mean()
    ax.fill_between(avg.index, avg.values, alpha=0.4, color=C1)
    ax.plot(avg.index, avg.values, color=C1, linewidth=2.5, marker='o', markersize=5)
    ax.set_title('Average Goals Per Match by Decade')
    ax.set_xlabel('Decade')
    ax.set_ylabel('Average Goals')
    plt.tight_layout()
    return fig

def count_plot(df):
    fig, ax = plt.subplots(figsize=(9, 5))
    top_t = df['tournament'].value_counts().nlargest(8)
    sns.barplot(x=top_t.values, y=top_t.index, palette=BLUES, ax=ax)
    ax.set_title('Match Count by Tournament (Top 8)')
    ax.set_xlabel('Number of Matches')
    ax.set_ylabel('Tournament')
    plt.tight_layout()
    return fig

def violin_plot(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    melted = pd.melt(
        df[['home_score', 'away_score']].rename(
            columns={'home_score': 'Home', 'away_score': 'Away'}),
        var_name='Side', value_name='Goals')
    sns.violinplot(data=melted, x='Side', y='Goals',
                   palette={'Home': C1, 'Away': C2}, ax=ax, inner='box')
    ax.set_title('Goals Distribution: Home vs Away')
    ax.set_xlabel('Side')
    ax.set_ylabel('Goals Scored')
    plt.tight_layout()
    return fig

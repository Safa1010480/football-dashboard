import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
import io
import streamlit as st

C1 = "#2563eb"
C2 = "#3b82f6"
C3 = "#93c5fd"
BLUES = "Blues_d"

LIGHT = {
    "figure.facecolor": "#ffffff",
    "axes.facecolor":   "#ffffff",
    "axes.titleweight": "bold",
    "axes.titlesize":   13,
    "axes.titlecolor":  "#2563eb",
    "axes.labelsize":   11,
    "axes.labelcolor":  "#111827",
    "axes.edgecolor":   "#d1d5db",
    "xtick.color":      "#4b5563",
    "ytick.color":      "#4b5563",
    "text.color":       "#111827",
    "grid.color":       "#d1d5db",
    "grid.linewidth":   0.5,
}

def set_style():
    sns.set_theme(style="whitegrid", font_scale=1.05)
    matplotlib.rcParams.update(LIGHT)

def _apply(fig, ax=None):
    """Force light theme on a figure after creation."""
    fig.patch.set_facecolor("#ffffff")
    if ax is not None:
        axes = [ax] if not hasattr(ax, "__iter__") else ax
        for a in axes:
            a.set_facecolor("#ffffff")
            a.tick_params(colors="#4b5563")
            a.xaxis.label.set_color("#111827")
            a.yaxis.label.set_color("#111827")
            a.title.set_color("#2563eb")
            for spine in a.spines.values():
                spine.set_edgecolor("#d1d5db")

def download_button(fig, filename):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    st.download_button(
        label="Download Chart",
        data=buf,
        file_name=filename,
        mime="image/png",
        use_container_width=True
    )

def pie_chart(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    counts = df['outcome'].value_counts()
    colors = [C1, C2, C3][:len(counts)]
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%',
           colors=colors, startangle=90,
           wedgeprops=dict(edgecolor='#ffffff', linewidth=2))
    for t in ax.texts:
        t.set_color('#111827')
    ax.set_title('Match Outcome Distribution', pad=15)
    _apply(fig, ax)
    plt.tight_layout()
    return fig

def histogram(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(df['total_goals'], bins=range(0, int(df['total_goals'].max()) + 2),
            color=C1, edgecolor='#ffffff', linewidth=0.6)
    ax.set_title('Goals Per Match Distribution')
    ax.set_xlabel('Total Goals')
    ax.set_ylabel('Number of Matches')
    ax.axvline(df['total_goals'].mean(), color=C3, linewidth=2,
               linestyle='--', label=f"Mean: {df['total_goals'].mean():.1f}")
    ax.legend(facecolor='#f8fafc', labelcolor='#111827')
    _apply(fig, ax)
    plt.tight_layout()
    return fig

def line_chart(df):
    fig, ax = plt.subplots(figsize=(9, 4))
    yearly = df.groupby('year').size().reset_index(name='matches')
    ax.plot(yearly['year'], yearly['matches'], color=C1, linewidth=2)
    ax.fill_between(yearly['year'], yearly['matches'], alpha=0.15, color=C2)
    ax.set_title('International Matches Played Per Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Matches')
    _apply(fig, ax)
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
    _apply(fig, ax)
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
    ax.plot([0, mx], [0, mx], color=C3, linewidth=1.2,
            linestyle='--', label='Equal score')
    ax.legend(facecolor='#f8fafc', labelcolor='#111827', fontsize=9)
    _apply(fig, ax)
    plt.tight_layout()
    return fig

def box_plot(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    top_t = df['tournament'].value_counts().nlargest(6).index
    subset = df[df['tournament'].isin(top_t)]
    order = subset.groupby('tournament')['total_goals'].median().sort_values(ascending=False).index
    sns.boxplot(data=subset, x='tournament', y='total_goals',
                hue='tournament', order=order, palette=BLUES, ax=ax, legend=False)
    ax.set_title('Goal Distribution by Top Tournaments')
    ax.set_xlabel('Tournament')
    ax.set_ylabel('Total Goals')
    ax.tick_params(axis='x', rotation=25)
    _apply(fig, ax)
    plt.tight_layout()
    return fig

def heatmap(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    corr = df[['home_score', 'away_score', 'total_goals', 'year']].corr()
    sns.heatmap(corr, annot=True, cmap='Blues', fmt='.2f',
                linewidths=0.5, ax=ax, vmin=-1, vmax=1,
                annot_kws={"color": "#111827"})
    ax.set_title('Feature Correlation Heatmap')
    _apply(fig, ax)
    plt.tight_layout()
    return fig

def area_chart(df):
    fig, ax = plt.subplots(figsize=(9, 4))
    avg = df.groupby('decade')['total_goals'].mean()
    ax.fill_between(avg.index, avg.values, alpha=0.3, color=C1)
    ax.plot(avg.index, avg.values, color=C2, linewidth=2.5, marker='o', markersize=5)
    ax.set_title('Average Goals Per Match by Decade')
    ax.set_xlabel('Decade')
    ax.set_ylabel('Average Goals')
    _apply(fig, ax)
    plt.tight_layout()
    return fig

def count_plot(df):
    fig, ax = plt.subplots(figsize=(9, 5))
    top_t = df['tournament'].value_counts().nlargest(8)
    sns.barplot(x=top_t.values, y=top_t.index, palette=BLUES, ax=ax)
    ax.set_title('Match Count by Tournament (Top 8)')
    ax.set_xlabel('Number of Matches')
    ax.set_ylabel('Tournament')
    _apply(fig, ax)
    plt.tight_layout()
    return fig

def violin_plot(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    melted = pd.melt(
        df[['home_score', 'away_score']].rename(
            columns={'home_score': 'Home', 'away_score': 'Away'}),
        var_name='Side', value_name='Goals')
    sns.violinplot(data=melted, x='Side', y='Goals', hue='Side',
                   palette={'Home': C1, 'Away': C2}, ax=ax,
                   inner='box', legend=False)
    ax.set_title('Goals Distribution: Home vs Away')
    ax.set_xlabel('Side')
    ax.set_ylabel('Goals Scored')
    _apply(fig, ax)
    plt.tight_layout()
    return fig

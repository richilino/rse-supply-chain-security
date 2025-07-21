import json
import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os
from scipy.stats import gaussian_kde
import statistics
import numpy as np
import pandas as pd

RISK_LEVELS = {
    "Dangerous-Workflow": "Critical",
    "Binary-Artifacts": "High",
    "Branch-Protection": "High",
    "Code-Review": "High",
    "Dependency-Update-Tool": "High",
    "Signed-Releases": "High",
    "Token-Permissions": "High",
    "Vulnerabilities": "High",
    "Maintained": "High",
    "Security-Policy": "Medium",
    "SAST": "Medium",
    "Packaging": "Medium",
    "Pinned-Dependencies": "Medium",
    "Fuzzing": "Medium",
    "CI-Tests": "Low",
    "CII-Best-Practices": "Low",
    "Contributors": "Low",
    "License": "Low"
}

BINARY_CHECKS = ["Packaging", "Fuzzing", "Dependency-Update-Tool", "Dangerous-Workflow"]

BINARY_LABELS = {
    "Packaging": ["No Package", "Package Found"],
    "Fuzzing": ["Not Implemented", "Implemented"],
    "Dependency-Update-Tool": ["Not Used", "Used"],
    "Dangerous-Workflow": ["Dangerous Workflow", "Safe Workflow"]
}


def load_json_data(json_files):
    """Load and combine JSON data from multiple files."""
    combined_data = []
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                combined_data.extend(data)
            else:
                print(f"⚠️ Warning: {json_file} does not contain a list.")
    return combined_data


def extract_scores(data):
    """Extract general scores and individual check scores, treating -1 as NA."""
    general_scores = []
    check_scores = {}

    for entry in data:
        general_score = entry.get('score', 0)
        if general_score != -1:
            general_scores.append(general_score)

        for check in entry.get('checks', []):
            check_name = check.get('name', 'Unknown Check')
            check_score = check.get('score', 0)

            if check_score == -1: # Skip N/A scores
                continue
            else: check_scores.setdefault(check_name, []).append(check_score)

    return general_scores, check_scores


def create_stats_table(general_scores, check_scores, total_repositories):
    """
    Create a DataFrame with median and standard deviation for all Security Checks,
    sorted by median score from lowest to highest.
    """
    stats_list = []
    
    for check_name, scores in check_scores.items():
        if len(scores) > 0:
            stats_list.append({
                'Security Check': check_name,
                'Score 0–10 [%]':round((len(scores)/total_repositories)*100,2),
                'Mean': round(np.mean(scores),2),
                'Std Dev': round(np.std(scores), 2),
                'Risk Level': RISK_LEVELS.get(check_name, "Unknown")
            })
    
    stats_df = pd.DataFrame(stats_list)
    stats_df = stats_df.sort_values(by='Mean')
    stats_df = stats_df.reset_index(drop=True)

    if len(general_scores) > 0:
        general_df = pd.DataFrame([{
            'Security Check': 'GENERAL SCORE',
            'Score 0–10 [%]': round((len(scores)/total_repositories)*100,2),
            'Mean': round(np.mean(general_scores),2),
            'Std Dev': round(np.std(general_scores),2),
            'Risk Level': ""
        }])
        stats_df = pd.concat([stats_df, general_df], ignore_index=True)

    return stats_df


def plot_stats_table(stats_df, output_dir):
    """ Save Stats Tabelle containing Score 0–10 [%], std, median, risfactor of all check_names and generel_score as PNG """
    fig, ax = plt.subplots(figsize=(10, len(stats_df)*0.5 + 2))
    ax.axis('off')
    table = ax.table(cellText=stats_df.values,
                     colLabels=stats_df.columns,
                     cellLoc='center',
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)

    path = os.path.join(output_dir, 'stats_table.png')
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()


def save_general_scores_plot(general_scores, output_dir):
    """Save the distribution of general scores as a PNG image."""
    fig, ax = plt.subplots(figsize=(8, 4))

    # Barplots
    boxplots_colors = ['slategray']
    unique_vals, counts = np.unique(general_scores, return_counts=True)
    ax.bar(unique_vals, counts, width=0.08, color='steelblue', alpha=0.6, label='Histogramm')

    # KDE-curve
    xs = np.linspace(min(general_scores), max(general_scores), 200)
    kde = gaussian_kde(general_scores)
    ax.plot(xs, kde(xs) * len(general_scores) * 0.08, color='black', lw=1.5, label='KDE', alpha=0.5)  

    # Boxplot
    bp = ax.boxplot(general_scores, 
                    patch_artist=True, 
                    vert=False, 
                    widths=10, 
                    positions=[-10], 
                    boxprops=dict(facecolor='slategray', edgecolor='black', linewidth=1, alpha=0.4),
                    flierprops=dict(marker='o', markersize=2, markerfacecolor='white', markeredgecolor='black', alpha=0.2),
                    medianprops=dict(linewidth=1, color='black')
                    )

    # general plot settings
    ax.set_ylim(-25, max(counts)*1.1 +20)
    plt.xticks(ticks=range(11), labels=[str(i) for i in range(11)], fontsize=12)
    plt.xlabel('Security Score', fontsize=14)
    yticks= [0,50, 100, 150, 200]
    plt.yticks(ticks= yticks, labels=[str(i) for i in yticks], fontsize=12)
    plt.ylabel('Repositories [n]', fontsize=14)
    plt.tight_layout()

    path = os.path.join(output_dir, 'general_scores_distribution.png')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()




def save_individual_check_plots(check_scores,stats_df, output_dir):
    """Save the distribution of individual check scores as separate PNG images."""
    os.makedirs(output_dir, exist_ok=True)
    sns.set(style="whitegrid")
    filtered_stats_df = stats_df[stats_df['Security Check'] != 'GENERAL SCORE']

    for _, row in filtered_stats_df.iterrows():
        check_name = row['Security Check']
        scores = check_scores[check_name]
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 5))

        if check_name in BINARY_CHECKS:
            _plot_binaer_histogram_for_check(ax, row, check_scores)
        else:
            _plot_histogram_for_check(ax, row, check_scores)

        plt.tight_layout()
        filename = f"{check_name}_distribution.png".replace(" ", "_")
        path = os.path.join(output_dir, filename)
        plt.savefig(path)
        plt.close(fig)


def _plot_histogram_for_check(ax, row, check_scores):
    check_name = row['Security Check']
    scores = check_scores[check_name]
    counts, bins, patches = ax.hist(scores, bins=range(12), color='steelblue', edgecolor='none', width=0.85)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    total = counts.sum()

    ymin, ymax = ax.get_ylim()
    offset = (ymax - ymin) * 0.01 
    for count, x in zip(counts, bin_centers):
        percent = count / total * 100
        if count > 0:
            ax.text(x, count + offset, f'{percent:.1f}%', ha='center', va='bottom', fontsize=14, color='black')

    ax.grid(axis='x')
    ax.set_xticks(bin_centers)
    ax.set_xticklabels([str(i) for i in range(11)], fontsize=16)
    ax.set_xlabel('Security Score', fontsize=18)
    ax.set_ylabel('Repositories [n]', fontsize=18)
    ax.set_yscale('log', nonpositive='clip')
    ax.set_yticks([1,10, 100, 1000, 10000])
    ax.set_yticklabels([1, 10, 100, 1000, 10000], fontsize= 16)
    ax.text(0.5, 1.12, f"{check_name}", transform=ax.transAxes,
            fontsize=20, ha='center', va='bottom', fontweight='bold')
    ax.text(0.5, 1.10, f"$n$={len(scores)}    Mean={row['Mean']}    Risk: {row['Risk Level']}",
            transform=ax.transAxes, fontsize=18, ha='center', va='top')

    for spine in ax.spines.values():
        spine.set_edgecolor('black')

    ax.grid(axis='y')
    ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(1.0, 10.0), numticks=100))
    ax.yaxis.set_minor_formatter(ticker.NullFormatter()) 
    ax.yaxis.grid(True, which='major', linestyle='-', linewidth=1, color="#AAAAAA")
    ax.yaxis.grid(True, which='minor', linestyle=':', linewidth=0.8, color= '#AAAAAA')


def _plot_binaer_histogram_for_check(ax, row, check_scores):
    """Plottet binäre Checks mit check-spezifischen Labels."""
    check_name = row['Security Check']
    scores = check_scores[check_name]
    labels = BINARY_LABELS[check_name]

    count_0 = sum(s == 0 for s in scores)
    count_1 = sum(s == 10 for s in scores)
    df = pd.DataFrame({
        "Status": [labels[0], labels[1]],
        "Count": [count_0, count_1]
    })

    sns.barplot(x="Status", y="Count", data=df, ax=ax, color='steelblue', edgecolor='none', width=0.2)
    ax.set_xticklabels(BINARY_LABELS[check_name], fontsize=16)
    ax.set_xlabel('Security Status', fontsize=18)
    ax.set_ylabel('Repositories [n]', fontsize=18)
    ax.text(0.5, 1.13, f"{check_name}", transform=ax.transAxes,
            fontsize=20, ha='center', va='bottom', fontweight='bold')
    ax.text(0.5, 1.10, f"$n$={len(scores)}    Mean={row['Mean']}    Risk: {row['Risk Level']}",
            transform=ax.transAxes, fontsize=18, ha='center', va='top')

    total = count_0 + count_1
    ymin, ymax = ax.get_ylim()
    offset = (ymax - ymin) * 0.01 

    for i, count in enumerate([count_0, count_1]):
        percent = count / total * 100
        if count > 0:
            ax.text(i, count + offset , f'{percent:.1f}%', ha='center', va='bottom', fontsize=14, color='black')

    ax.set_yscale('log', nonpositive='clip')
    ax.grid(axis='y')
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
    ax.set_yticks([1, 10, 100, 1000, 10000])
    ax.set_yticklabels([1, 10, 100, 1000, 10000], fontsize= 16)
    ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(1.0, 10.0), numticks=100))
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())  
    ax.yaxis.grid(True, which='major', linestyle='-', linewidth=1, color='#AAAAAA')
    ax.yaxis.grid(True, which='minor', linestyle=':', linewidth=0.8,color='#AAAAAA' )


def save_all_checks_as_single_plots(check_scores, stats_df, output_dir):
    """"Save a plot containing all check score distributions."""
    sns.set(style="whitegrid")
    filtered_stats_df = stats_df[stats_df['Security Check'] != 'GENERAL SCORE']

    for _, row in filtered_stats_df.iterrows():
        check_name = row['Security Check']
        scores = check_scores[check_name]
        fig, ax = plt.subplots(figsize=(6, 8))

        if check_name in BINARY_CHECKS:
            _plot_binaer_histogram_for_check(ax, row, check_scores)
        else:
            _plot_histogram_for_check(ax, row, check_scores)

        plt.tight_layout()
        filename = f'{check_name}_distribution.png'.replace(" ", "_")
        path = os.path.join(output_dir, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path)
        plt.close(fig)

def save_all_checks_multiplot(check_scores, stats_df, output_dir):
    """Save a plot containing all check score distributions."""
    sns.set(style="whitegrid")

    filtered_stats_df = stats_df[stats_df['Security Check'] != 'GENERAL SCORE']
    num_checks = len(check_scores)
    num_columns = 3
    num_rows = (num_checks + num_columns - 1) // num_columns

    fig, axes = plt.subplots(num_rows, num_columns, figsize=(25, num_rows * 4))
    axes = axes.flatten()

    for i, (_, row) in enumerate(filtered_stats_df.iterrows()):
        ax = axes[i]
        check_name = row['Security Check']
        scores = check_scores[check_name]

        if check_name in BINARY_CHECKS:
            _plot_binaer_histogram_for_check(ax, row, check_scores)   
        else:
            _plot_histogram_for_check(ax, row, check_scores)


    for j in range(len(check_scores), len(axes)):
        fig.delaxes(axes[j])

    path = os.path.join(output_dir, 'all_checks_distribution.png')
    plt.tight_layout(h_pad=4, w_pad=9)
    plt.savefig(path)
    plt.close()


def plot_high_risk_checks(check_scores, stats_df, output_dir):
    """
    Save a plot with the high-risk checks (High or Critical).
    """
    sns.set(style="whitegrid")
    high_risk_df = stats_df[(stats_df['Risk Level'] == 'High') | (stats_df['Risk Level'] == 'Critical')]

    fig, axes = plt.subplots(3, 3, figsize=(25, 3 * 4))
    axes = axes.flatten()
    for i, (_, row) in enumerate(high_risk_df.iterrows()):
        ax = axes[i]
        check_name = row['Security Check']

        if check_name in BINARY_CHECKS:
            _plot_binaer_histogram_for_check(ax, row, check_scores)   
        else:
            _plot_histogram_for_check(ax, row, check_scores)
        
    
    for j in range(len(high_risk_df), 3):
        axes[j].set_visible(False)
    
    path = os.path.join(output_dir, 'high_risk_checks.png')
    plt.tight_layout(h_pad=2, w_pad=8)
    plt.savefig(path)
    plt.close()


def plot_top_high_risk_checks(check_scores, stats_df, output_dir):
    """
    Save a plot with the 3 high-risk checks (High or Critical) that have the highest mean score.
    Shows these three plots side by side.
    """
    
    sns.set(style="whitegrid")
    high_risk_df = stats_df[(stats_df['Risk Level'] == 'High') | (stats_df['Risk Level'] == 'Critical')]
    top_checks = high_risk_df.sort_values(by='Mean', ascending=False).head(3)
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 5))
    for i, (_, row) in enumerate(top_checks.iterrows()):
        ax = axes[i]
        check_name = row['Security Check']

        if check_name in BINARY_CHECKS:
            _plot_binaer_histogram_for_check(ax, row, check_scores)   
        else:
            _plot_histogram_for_check(ax, row, check_scores)
        
    for j in range(len(top_checks), 3):
        axes[j].set_visible(False)
    
    path = os.path.join(output_dir, 'top_high_risk_checks.png')
    plt.tight_layout(h_pad=2, w_pad=8)
    plt.savefig(path)
    plt.close()


def plot_lowest_high_risk_checks(check_scores, stats_df, output_dir):
    """
    Save a plot with the 3 high-risk checks (High or Critical) that have the lowest mean score.
    Shows these three plots side by side.
    """
    
    sns.set(style="whitegrid")
    high_risk_df = stats_df[(stats_df['Risk Level'] == 'High') | (stats_df['Risk Level'] == 'Critical')]
    lowest_checks = high_risk_df.sort_values(by='Mean', ascending=True).head(3)
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 5))
    for i, (_, row) in enumerate(lowest_checks.iterrows()):
        ax = axes[i]
        check_name = row['Security Check']
        if check_name in BINARY_CHECKS:
            _plot_binaer_histogram_for_check(ax, row, check_scores)   
        else:
            _plot_histogram_for_check(ax, row, check_scores)
    
    for j in range(len(lowest_checks), 3):
        axes[j].set_visible(False)
    
    path = os.path.join(output_dir, 'lowest_high_risk_checks.png')
    plt.tight_layout(h_pad=2, w_pad=8)
    plt.savefig(path)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Visualize distribution of Scorecard scores from multiple JSON files.")
    parser.add_argument("json_files", nargs='+', help="Paths to the input JSON files (multiple allowed)")
    parser.add_argument("output_dir", help="Directory to save output plots")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    data = load_json_data(args.json_files)
    total_repositories = len(data)

    print(f"Analyzing {len(data)} repositories...")

    general_scores, check_scores = extract_scores(data)

    print(f"Median Score: {statistics.fmean(general_scores)}")
    print(f"Quantiles Score: {statistics.quantiles(general_scores)}")

    stats_df = create_stats_table(general_scores, check_scores, total_repositories)
    plot_stats_table(stats_df, args.output_dir)

    save_general_scores_plot(general_scores, args.output_dir)

    
    save_all_checks_multiplot(check_scores, stats_df, args.output_dir)
    plot_top_high_risk_checks(check_scores, stats_df, args.output_dir)
    plot_lowest_high_risk_checks(check_scores, stats_df, args.output_dir)
    plot_high_risk_checks(check_scores, stats_df, args.output_dir)
    save_individual_check_plots(check_scores, stats_df, os.path.join(args.output_dir, "single_plots"))

    print(f"✅ Plots saved to {args.output_dir}")


if __name__ == "__main__":
    main()






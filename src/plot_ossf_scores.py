import json
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import os
import statistics
import numpy as np

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

            if check_name == "Packaging": # Für Packaging: -1 als 0 zählen, da -1 bedeutet kein Packaging gefunden
                if check_score == -1:
                    check_score = 0
                check_scores.setdefault(check_name, []).append(check_score)
            else:
                # Für alle anderen Checks: -1 überspringen
                if check_score == -1: # Skip N/A scores
                    continue
                check_scores.setdefault(check_name, []).append(check_score)

    return general_scores, check_scores



def save_general_scores_plot(general_scores, output_dir):
    """Save the distribution of general scores as a PNG image."""

    plt.figure(figsize=(8, 6))
    sns.violinplot(x=general_scores, linecolor="skyblue",color="skyblue" ,inner="box", inner_kws=dict(color="black", box_width=17, whis_width=2), linewidth=1)
    plt.xticks(ticks=range(11), labels=[str(i) for i in range(11)], fontsize=16)
    plt.xlabel('Security Score', fontsize=18)
    plt.yticks(fontsize=16)

    path = os.path.join(output_dir, 'general_scores_distribution.png')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

# def save_individual_check_plots(check_scores, output_dir):
#     """Save the distribution of individual check scores as separate PNG images."""
#     sns.set(style="whitegrid")
#     for check_name, scores in check_scores.items():
#         plt.figure(figsize=(8, 6))
#         sns.histplot(scores, kde=True, color="salmon", bins=10)
#         plt.title(f'Distribution for: {check_name}')
#         plt.xlabel('Score')
#         plt.ylabel('Frequency')

#         filename = f'{check_name.replace(" ", "_")}_distribution.png'
#         plt.tight_layout()
#         plt.savefig(os.path.join(output_dir, filename))
#         plt.close()

def save_all_checks_multiplot(check_scores, output_dir):
    """Save a large multiplot containing all check score distributions."""
    import numpy as np
    sns.set(style="whitegrid")
    num_checks = len(check_scores)
    num_columns = 3
    num_rows = (num_checks + num_columns - 1) // num_columns

    fig, axes = plt.subplots(num_rows, num_columns, figsize=(15, num_rows * 4))
    axes = axes.flatten()

    for i, (check_name, scores) in enumerate(check_scores.items()):
        ax = axes[i]
        counts, bins, patches = ax.hist(scores, bins=range(12), color='steelblue', edgecolor='black')  # bins=range(12) für 0-10
        bin_centers = 0.5 * (bins[:-1] + bins[1:])

        ax.grid(axis='x') 
        ax.set_xticks(bin_centers)
        ax.set_xticklabels([str(i) for i in range(11)], fontsize=12)
        ax.set_xlabel('Security Score', fontsize=14)
        if check_name == "Packaging":
            xticklabels = ["0*"] + [str(i) for i in range(1, 11)]
        else:
            xticklabels = [str(i) for i in range(11)]
        ax.set_xticklabels(xticklabels, fontsize=12)

        ax.set_ylabel('Number of Repositories', fontsize=14)
        ax.set_yscale('log')
        ax.set_yticks([1, 10, 100, 1000, 4000])
        ax.set_yticklabels([1,10, 100, 1000, 4000])   #ax.set_yticklabels(['0','1', '2', '3', '4'], fontsize=12)

        if check_name == "Packaging":
            patches[0].set_facecolor("skyblue")
        
        ax.set_title(f"{check_name} (n={len(scores)})", fontsize=18)


    for j in range(len(check_scores), len(axes)):
        fig.delaxes(axes[j])

    path = os.path.join(output_dir, 'all_checks_distribution.png')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def create_stats_table(general_scores, check_scores):
    """
    Create a DataFrame with median and standard deviation for all check names,
    sorted by median score from lowest to highest.
    """
    import pandas as pd
    
    stats_list = []
    
    # Calculate median and std for each check
    for check_name, scores in check_scores.items():
        if len(scores) > 0:
            stats_list.append({
                'Check Name': check_name,
                'n': len(scores),
                'Mean': round(np.mean(scores),2),
                'Median': round(np.median(scores), 2),
                'Std Dev': round(np.std(scores), 2),
                'Risk Level': RISK_LEVELS.get(check_name, "Unknown")
            })
    
    # Create DataFrame
    stats_df = pd.DataFrame(stats_list)
    stats_df = stats_df.sort_values(by='Mean')
    stats_df = stats_df.reset_index(drop=True)

    # General Scores berechnen und als separate Zeile hinzufügen
    if len(general_scores) > 0:
        general_df = pd.DataFrame([{
            'Check Name': 'GENERAL SCORE',
            'n': len(general_scores),
            'Median': round(np.median(general_scores),2),
            'Mean': round(np.mean(general_scores),2),
            'Std Dev': round(np.std(general_scores),2),
            'Risk Level': ""
        }])
        stats_df = pd.concat([stats_df, general_df], ignore_index=True)

    return stats_df


def plot_stats_table(stats_df, output_dir):
    """ Save Stats Tabelle containing mean, std, median, risfactor of all check_names and generel_score as PNG """
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


def plot_top_high_risk_checks(check_scores, stats_df, output_dir):
    """
    Save a plot with the 3 high-risk checks (High or Critical) that have the highest mean score.
    Shows these three plots side by side.
    """
    import numpy as np
    import seaborn as sns
    
    sns.set(style="whitegrid")
    high_risk_df = stats_df[(stats_df['Risk Level'] == 'High') | (stats_df['Risk Level'] == 'Critical')]
    top_checks = high_risk_df.sort_values(by='Mean', ascending=False).head(3)
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 5))
    for i, (_, row) in enumerate(top_checks.iterrows()):
        check_name = row['Check Name']
        scores = check_scores[check_name]
        
        ax = axes[i]
        counts, bins, patches = ax.hist(scores, bins=range(12), color='steelblue', edgecolor='black')
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        
        ax.grid(axis='x')
        ax.set_xticks(bin_centers)
        ax.set_xlabel('Security Score', fontsize=14)
        
        if check_name == "Packaging":
            xticklabels = ["0*"] + [str(i) for i in range(1, 11)]
            patches[0].set_facecolor("skyblue")
        else:
            xticklabels = [str(i) for i in range(11)]
        
        ax.set_xticklabels(xticklabels, fontsize=12)
        ax.set_ylabel('Number of Repositories', fontsize=14)
        ax.set_yscale('log')
        ax.set_yticks([1, 10, 100, 1000, 4000])
        ax.set_yticklabels([1, 10, 100, 1000, 4000])
        ax.set_title(f"{check_name} (n={len(scores)})\nMean: {row['Mean']}, Risk: {row['Risk Level']}", fontsize=16)
    
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
    import numpy as np
    import seaborn as sns
    
    sns.set(style="whitegrid")
    high_risk_df = stats_df[(stats_df['Risk Level'] == 'High') | (stats_df['Risk Level'] == 'Critical')]
    lowest_checks = high_risk_df.sort_values(by='Mean', ascending=True).head(3)
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 5))
    for i, (_, row) in enumerate(lowest_checks.iterrows()):
        check_name = row['Check Name']
        scores = check_scores[check_name]
        
        ax = axes[i]
        counts, bins, patches = ax.hist(scores, bins=range(12), color='steelblue', edgecolor='black')
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        
        ax.grid(axis='x')
        ax.set_xticks(bin_centers)
        ax.set_xlabel('Security Score', fontsize=14)
        
        if check_name == "Packaging":
            xticklabels = ["0*"] + [str(i) for i in range(1, 11)]
            patches[0].set_facecolor("skyblue")
        else:
            xticklabels = [str(i) for i in range(11)]
        
        ax.set_xticklabels(xticklabels, fontsize=12)
        ax.set_ylabel('Number of Repositories', fontsize=14)
        ax.set_yscale('log')
        ax.set_yticks([1, 10, 100, 1000, 4000])
        ax.set_yticklabels([1, 10, 100, 1000, 4000])
        ax.set_title(f"{check_name} (n={len(scores)})\nMean: {row['Mean']}, Risk: {row['Risk Level']}", fontsize=16)
    
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

    print(f"Analyzing {len(data)} repositories...")

    general_scores, check_scores = extract_scores(data)

    print(f"Median Score: {statistics.fmean(general_scores)}")
    print(f"Quantiles Score: {statistics.quantiles(general_scores)}")

    save_general_scores_plot(general_scores, args.output_dir)
    #save_individual_check_plots(check_scores, args.output_dir)
    save_all_checks_multiplot(check_scores, args.output_dir)

    stats_df = create_stats_table(general_scores, check_scores)
    plot_stats_table(stats_df, args.output_dir)

    plot_top_high_risk_checks(check_scores, stats_df, args.output_dir)
    plot_lowest_high_risk_checks(check_scores, stats_df, args.output_dir)

    print(f"✅ Plots saved to {args.output_dir}")




if __name__ == "__main__":
    main()






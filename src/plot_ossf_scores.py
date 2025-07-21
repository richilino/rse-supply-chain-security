import json
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import os
import statistics

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
            if check_score == -1:
                continue  # Skip N/A scores
            check_scores.setdefault(check_name, []).append(check_score)

    return general_scores, check_scores

def save_general_scores_plot(general_scores, output_dir):
    """Save the distribution of general scores as a PNG image."""
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 6))
    sns.histplot(general_scores, kde=True, color="skyblue", bins=10, binrange=[0,10])
    plt.title('Distribution of General Scores')
    plt.xlabel('General Score')
    plt.ylabel('Frequency')

    path = os.path.join(output_dir, 'general_scores_distribution.png')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def save_individual_check_plots(check_scores, output_dir):
    """Save the distribution of individual check scores as separate PNG images."""
    sns.set(style="whitegrid")
    for check_name, scores in check_scores.items():
        plt.figure(figsize=(8, 6))
        sns.histplot(scores, kde=True, color="salmon", bins=10, binrange=[0,10])
        plt.title(f'Distribution for: {check_name}')
        plt.xlabel('Score')
        plt.ylabel('Frequency')

        filename = f'{check_name.replace(" ", "_")}_distribution.png'
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, filename))
        plt.close()

def save_all_checks_multiplot(check_scores, output_dir):
    """Save a large multiplot containing all check score distributions."""
    sns.set(style="whitegrid")
    num_checks = len(check_scores)
    num_columns = 3
    num_rows = (num_checks + num_columns - 1) // num_columns

    fig, axes = plt.subplots(num_rows, num_columns, figsize=(15, num_rows * 4))
    axes = axes.flatten()

    for i, (check_name, scores) in enumerate(check_scores.items()):
        ax = axes[i]
        sns.histplot(scores, kde=True, ax=ax, color="salmon", bins=10, binrange=[0,10])
        ax.set_title(check_name)
        ax.set_xlabel('Score')
        ax.set_ylabel('Frequency')

    for j in range(len(check_scores), len(axes)):
        fig.delaxes(axes[j])

    path = os.path.join(output_dir, 'all_checks_distribution.png')
    plt.tight_layout()
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
    save_individual_check_plots(check_scores, args.output_dir)
    save_all_checks_multiplot(check_scores, args.output_dir)

    print(f"✅ Plots saved to {args.output_dir}")

if __name__ == "__main__":
    main()

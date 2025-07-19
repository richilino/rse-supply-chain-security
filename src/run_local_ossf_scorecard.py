import subprocess
import json
import argparse
import os

def run_scorecard(scorecard_dir, repo_url):
    """Runs scorecard for a single repository and returns parsed JSON output."""
    try:
        result = subprocess.run(
            [os.path.join(scorecard_dir, 'scorecard'), f'--repo={repo_url}', '--format=json'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Scorecard failed for {repo_url}: {e.stderr.strip()}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Failed to parse JSON output for {repo_url}")
        return None

def load_existing_urls(output_json):
    existing_urls = set()
    if os.path.exists(output_json):
        with open(output_json, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                for entry in data:
                    repo_name = entry['repo']['name']
                    existing_urls.add(f"https://{repo_name}")
            except json.JSONDecodeError:
                pass  # If the file is empty or not valid JSON, just ignore it
    return existing_urls

def main(scorecard_dir, input_txt, exclude_urls, output_json):
    # Read TXT and extract exclude URLs
    with open(exclude_urls, 'r', encoding='utf-8') as file:
        exclude_repos = [line.strip() for line in file if line.strip()]

    print(f"Excluding {len(exclude_repos)} repositories from local scan...")

    # Load existing URLs from the output JSON
    existing_urls = load_existing_urls(output_json)

    print(f"Excluding {len(existing_urls)} already scanned repositories...")

    # Read input TXT and get list of URLs
    with open(input_txt, 'r', encoding='utf-8') as f:
        repo_urls = [line.strip() for line in f if line.strip() and line.strip() not in exclude_repos and line.strip() not in existing_urls]

    print(f"🚀 Running scorecard on {len(repo_urls)} repositories...")

    batch_size = 1  # Define the batch size
    results_batch = []

    for i, repo in enumerate(repo_urls, start=1):
        print(f"[{i}/{len(repo_urls)}] Running scorecard on {repo}...")
        result = run_scorecard(scorecard_dir, repo)
        if result:
            results_batch.append(result)

            # Check if the batch is full or if it's the last repository
            if len(results_batch) >= batch_size or i == len(repo_urls):
                # Load existing data from the file
                if os.path.exists(output_json):
                    with open(output_json, 'r', encoding='utf-8') as out_f:
                        existing_data = json.load(out_f)
                else:
                    existing_data = []

                # Append the batch results to the existing data
                existing_data.extend(results_batch)

                # Write the updated data back to the file
                with open(output_json, 'w', encoding='utf-8') as out_f:
                    json.dump(existing_data, out_f, indent=4)

                # Clear the batch for the next set of results
                results_batch = []

    print(f"✅ Completed. Results saved to {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OSSF Scorecard on repositories from a TXT file and save results.")
    parser.add_argument("scorecard_dir", help="Path to the directory containing the scorecard binary")
    parser.add_argument("input_txt", help="Path to the input TXT file (one repo URL per line)")
    parser.add_argument("exclude_urls", help="Path to the input TXT file of URLs that should not be scanned")
    parser.add_argument("output_json", help="Path to the output JSON file for scorecard results")
    args = parser.parse_args()

    main(args.scorecard_dir, args.input_txt, args.exclude_urls, args.output_json)

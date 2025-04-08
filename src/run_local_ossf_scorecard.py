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

def main(scorecard_dir, input_txt, exclude_urls, output_json):
    # Read TXT and extract exclude URLs
    with open(exclude_urls, 'r', encoding='utf-8') as file:
        exclude_repos = [line.strip() for line in file if line.strip()]

    print(f"Excluding {len(exclude_repos)} repositories from local scan...")

    # Read input TXT and get list of URLs
    with open(input_txt, 'r', encoding='utf-8') as f:
        repo_urls = [line.strip() for line in f if line.strip() and line.strip() not in exclude_repos]

    all_results = []

    print(f"🚀 Running scorecard on {len(repo_urls)} repositories...")

    for i, repo in enumerate(repo_urls[:10], start=1):
        print(f"[{i}/{len(repo_urls)}] Running scorecard on {repo}...")
        result = run_scorecard(scorecard_dir, repo)
        if result:
            all_results.append(result)
            # Write results to output JSON after each run (optional but keeps progress)
            with open(output_json, 'w', encoding='utf-8') as out_f:
                json.dump(all_results, out_f, indent=2)

    print(f"✅ Completed. {len(all_results)} results saved to {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OSSF Scorecard on repositories from a TXT file and save results.")
    parser.add_argument("scorecard_dir", help="Path to the directory containing the scorecard binary")
    parser.add_argument("input_txt", help="Path to the input TXT file (one repo URL per line)")
    parser.add_argument("exclude_urls", help="Path to the input TXT file of URLs that should not be scanned")
    parser.add_argument("output_json", help="Path to the output JSON file for scorecard results")
    args = parser.parse_args()

    main(args.scorecard_dir, args.input_txt, args.exclude_urls, args.output_json)

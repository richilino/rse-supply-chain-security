import requests
import argparse
import time
import json

OSSF_API_BASE = "https://api.securityscorecards.dev/projects/"

def fetch_scorecard_data(repo_url):
    """Queries the OSSF Scorecard API for a given repository URL."""
    try:
        repo_path = repo_url.replace("https://", "")  # Remove 'https://' for API format
        api_url = f"{OSSF_API_BASE}{repo_path}"
        
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Failed to fetch data for {repo_url} (Status Code: {response.status_code})")
            return {"repo": repo_url, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        print(f"❌ Error fetching data for {repo_url}: {e}")
        return {"repo": repo_url, "error": str(e)}

def query_ossf_scorecard(tracked_repos_file, output_json_file):
    """Reads the tracked repositories, queries the OSSF Scorecard API, and writes results to JSON."""
    results = []

    try:
        with open(tracked_repos_file, 'r', encoding='utf-8') as file:
            repos = [line.strip() for line in file.readlines() if line.strip()]

        print(f"🔍 Querying OSSF Scorecard for {len(repos)} repositories...\n")

        for repo in repos:
            data = fetch_scorecard_data(repo)
            results.append(data)

            # Print to console
            if "error" not in data:
                print(f"📌 Repository: {repo}")
                print(f"🔹 Score: {data.get('score', 'N/A')}")
                print(f"📅 Date: {data.get('date', 'N/A')}")
            else:
                print(f"⚠️ {repo}: {data['error']}")

            time.sleep(0.5)  # Respect API rate limits

        # Write results to JSON file
        with open(output_json_file, 'w', encoding='utf-8') as json_file:
            json.dump(results, json_file, indent=4)

        print(f"\n✅ Results saved to {output_json_file}")

    except Exception as e:
        print(f"❌ Error processing repositories: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query OSSF Scorecard API for tracked repositories and save results to JSON.")
    parser.add_argument("tracked_repos_file", help="Path to the text file containing tracked repositories")
    parser.add_argument("output_json_file", help="Path to the JSON file for storing results")

    args = parser.parse_args()

    query_ossf_scorecard(args.tracked_repos_file, args.output_json_file)

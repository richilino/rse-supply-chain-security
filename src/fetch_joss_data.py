import os
import requests
import argparse
import json

GITHUB_ISSUE_API_BASE = "https://api.github.com/repos/openjournals/joss-reviews/issues"

def fetch_issues(api_url, output_dir):
    page = 1
    per_page = 100
    while True:
        # Construct the URL with pagination parameters
        params = [("state", "all"),("labels", "accepted"),("per_page", per_page), ("page", page)]
        response = requests.get(api_url, params=params, headers={"Authorization": f"Bearer {os.environ["GITHUB_AUTH_TOKEN"]}"})

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            break

        data = response.json()

        # If the data is empty, we've reached the end of pagination
        if not data:
            break

        # Write the data to a file
        output_file = os.path.join(output_dir, f"joss_repository_data.{page}.json")
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Saved page {page} to {output_file}")
        page += 1

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch GitHub issues with pagination and save to a specified directory.")
    parser.add_argument("output_dir", help="The directory to save the output files.")

    # Parse the command-line arguments
    args = parser.parse_args()
    output_dir = args.output_dir

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fetch_issues(GITHUB_ISSUE_API_BASE, output_dir)

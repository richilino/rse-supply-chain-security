import csv
import argparse

def filter_matching_urls(txt_file, csv_file, output_file):
    try:
        # Load URLs from the TXT file
        with open(txt_file, 'r', encoding='utf-8') as tf:
            txt_urls = [line.strip() for line in tf if line.strip()]

        # Read CSV and store OSSF-tracked repos in a set (with https:// prepended)
        ossf_repos = set()
        with open(csv_file, 'r', encoding='utf-8') as cf:
            csv_reader = csv.DictReader(cf)
            for row in csv_reader:
                repo_url = "https://" + row["repo"].strip()
                ossf_repos.add(repo_url)

        total_tracked = len(ossf_repos)  # Total OSSF-tracked repos

        # Find matching and untracked URLs
        matching_urls = [url for url in txt_urls if url in ossf_repos]
        untracked_urls = [url for url in txt_urls if url not in ossf_repos]

        # Write matching URLs to the output text file
        with open(output_file, 'w', encoding='utf-8') as of:
            for url in matching_urls:
                of.write(url + "\n")

        # Print summary
        print(f"Total URLs tracked by OSSF: {total_tracked}")
        print(f"Total URLs checked from TXT: {len(txt_urls)}")
        print(f"Total repos matched: {len(matching_urls)}")
        print(f"Matching URLs saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter URLs in TXT file based on OSSF-tracked repos in CSV.")
    parser.add_argument("txt_file", help="Path to the input TXT file (one URL per line)")
    parser.add_argument("csv_file", help="Path to the CSV file (OSSF-tracked repos)")
    parser.add_argument("output_file", help="Path to the output text file")

    args = parser.parse_args()

    filter_matching_urls(args.txt_file, args.csv_file, args.output_file)

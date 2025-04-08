envvars:
    "GITHUB_AUTH_TOKEN"

rule all:
    input: 
        "data/api/rsd_repository_data.json"
        "data/api/joss_repository_data.json",
        "data/urls/rsd_repository_urls.txt",
        "data/urls/joss_repository_urls.txt",
        "data/urls/tracked_repository_urls.txt",
        "data/urls/merged_urls.txt",
        "data/scores/tracked.repository_scores.json",
        "data/scores/local.repository_scores.json",

# RSD

rule download_rsd_repository_data:
    output: "data/api/rsd_repository_data.json"
    shell: 
        """curl https://research-software-directory.org/api/v1/repository_url -o {output}"""

rule filter_rsd_repository_data:
    input: "data/api/rsd_repository_data.json"
    output: "data/urls/rsd_repository_urls.txt"
    shell:
        """cat {input} |  jq '[.[] | select(.code_platform == "github") | {{url: .url}}]' | grep -Eo \"(http|https)://github.com/[a-zA-Z0-9_-]*/[a-zA-Z0-9_-]*\" | sort -u > {output}"""

# JOSS

rule download_joss_repository_data:
    output: "data/api/joss_repository_data.json"
    shell:
        """curl "https://api.github.com/repos/openjournals/joss-reviews/issues?state=all&labels=accepted" -o {output}"""

rule filter_joss_repository_data:
    input: "data/api/joss_repository_data.json"
    output: "data/urls/joss_repository_urls.txt"
    shell:
        "cat {input} | jq '[.[] | {{url: .body}}]' | grep -Eo \"(http|https)://github.com/[a-zA-Z0-9_-]*/[a-zA-Z0-9_-]*\" | sort -u > {output}"

rule merge_repository_urls:
    input: 
        "data/urls/rsd_repository_urls.txt",
        "data/urls/joss_repository_urls.txt",
    output: "data/urls/merged_urls.txt"
    shell:
        "cat {input} | sort -u > {output}"


# OSSF Tracked Repos

rule download_ossf_tracked_repositories:
    output: "data/ossf_tracked.csv"
    shell:
        """curl https://raw.githubusercontent.com/ossf/scorecard/refs/heads/main/cron/internal/data/projects.csv -o {output}"""

rule find_tracked_repositories:
    input: 
        urls_repos="data/urls/merged_urls.txt",
        ossf_tracked="data/ossf_tracked.csv"
    output:
        "data/urls/tracked_repository_urls.txt"
    shell:
        """python3 src/filter_tracked_repositories.py {input.urls_repos} {input.ossf_tracked} {output}"""

rule query_tracked_repositories:
    input: "data/urls/tracked_repository_urls.txt"
    output: "data/scores/tracked.repository_scores.json"
    shell: 
        """python3 src/query_ossf_scorecard.py {input} {output}"""

rule run_local_ossf_scorecard:
    input: 
        repo_urls="data/urls/merged_urls.txt",
        exclude_urls="data/urls/tracked_repository_urls.txt"
    output: "data/scores/local.repository_scores.json"
    shell:
        """python3 src/run_local_ossf_scorecard.py ~/go/bin {input.repo_urls} {input.exclude_urls} {output}"""

rule analyze_repositories:
    input: 
        "data/scores/tracked.repository_scores.json", 
        "data/scores/local.repository_scores.json" 
    shell: 
        """python3 src/plot_ossf_scores.py {input} plots"""

rule clean:
    shell:
        """find data -type f ! -path "data/raw/*" -delete"""

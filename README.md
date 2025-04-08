# Supply Chain Security Analysis of Research Software

## Setting Up the Environment

### Python Environment

To make it easy for you to get started with contributing / reproducing our results, we recommend to setup a virtual environment (venv). You can create a new venv using the command:

```sh
python -m venv ./venv
```

Then activate it using:

```sh
source /pathToVenv/bin/activate
```

and install the dependencies using the following command:

```sh
pip install -r requirements.txt
```

### Scorecard

Additionally, you need to have setup a local installation of the OSSF Scorecard with Go. To install Scorecard as a standalone:

Visit the [release page](https://github.com/ossf/scorecard/releases/tag/v5.1.1) and download the correct zip file for your operating system.

Add the binary to your GOPATH/bin directory (use go env GOPATH to identify your directory if necessary).

## Starting an Analysis Run

Create a GitHub PAT with public repositories permission so you don't run into API request limits.

```sh
export GITHUB_AUTH_TOKEN=<your_github_token>

snakemake
```

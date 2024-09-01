import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter


def read_csv_to_dict(file_name: str):
    csv_objects = []
    if os.path.exists(file_name):
        with open(file_name, mode='r', newline='') as file:
            csv_reader = csv.DictReader(file)
            csv_objects = [row for row in csv_reader]
    return csv_objects


# RQ 05
def plot_language_distribution(data, output_image='language_distribution.png'):
    language_counts = Counter(row['language'] for row in data)

    top_10_languages = language_counts.most_common(10)

    languages, counts = zip(*top_10_languages) if top_10_languages else ([], [])

    plt.figure(figsize=(10, 6))
    plt.barh(languages, counts, color='skyblue')
    plt.xlabel('Number of Repositories')
    plt.ylabel('Programming Languages')
    plt.title('Top 10 Most Common Programming Languages')

    plt.savefig(output_image)
    print(f"Plot saved as {output_image}")


# RQ 01
def analyze_creation_dates(data, output_image='creation_dates_distribution.png'):
    creation_years = [datetime.strptime(row['created_at'], '%Y-%m-%dT%H:%M:%SZ').year for row in data]

    year_counts = Counter(creation_years)

    sorted_years = sorted(year_counts.items())
    years, counts = zip(*sorted_years) if sorted_years else ([], [])

    plt.figure(figsize=(10, 6))
    plt.bar(years, counts, color='green')
    plt.xlabel('Year')
    plt.ylabel('Number of Repositories Created')
    plt.title('Repositories Created per Year')

    plt.savefig(output_image)
    print(f"Creation date analysis saved as {output_image}")


# RQ 02
def analyze_pull_requests(data, output_image='pull_requests_distribution.png'):
    pull_requests = [int(row['total_pulls']) for row in data]

    plt.figure(figsize=(10, 6))
    plt.hist(pull_requests, bins=20, color='orange')
    plt.xlabel('Number of Pull Requests')
    plt.ylabel('Number of Repositories')
    plt.title('Distribution of Pull Requests Across Repositories')
    plt.savefig(output_image)
    print(f"Pull requests analysis saved as {output_image}")


# RQ 03
def analyze_releases(data, output_image='releases_distribution.png'):
    releases = [int(row['total_releases']) for row in data]

    plt.figure(figsize=(10, 6))
    plt.hist(releases, bins=20, color='purple')
    plt.xlabel('Number of Releases')
    plt.ylabel('Number of Repositories')
    plt.title('Distribution of Releases Across Repositories')
    plt.savefig(output_image)
    print(f"Releases analysis saved as {output_image}")


# RQ 04
def analyze_last_update(data, output_image='last_update_distribution.png'):
    current_date = datetime.now()
    last_update_days = [
        (current_date - datetime.strptime(row['updated_at'], '%Y-%m-%dT%H:%M:%SZ')).days
        for row in data
    ]

    plt.figure(figsize=(10, 6))
    plt.hist(last_update_days, bins=20, color='red')
    plt.xlabel('Days Since Last Update')
    plt.ylabel('Number of Repositories')
    plt.title('Distribution of Time Since Last Update Across Repositories')
    plt.savefig(output_image)
    print(f"Last update analysis saved as {output_image}")


# RQ 06
def analyze_closed_issues(data, output_image='closed_issues_distribution.png'):
    closed_issues_ratios = [float(row['closed_issues_ratio']) for row in data]

    plt.figure(figsize=(10, 6))
    plt.hist(closed_issues_ratios, bins=20, color='blue')
    plt.xlabel('Closed Issues Ratio')
    plt.ylabel('Number of Repositories')
    plt.title('Distribution of Closed Issues Ratios Across Repositories')
    plt.savefig(output_image)
    print(f"Closed issues ratio analysis saved as {output_image}")


if __name__ == "__main__":
    size = 1000
    file_name = "repos_details.csv"
    data = read_csv_to_dict(file_name)

    # RQ 01
    plot_language_distribution(data)

    # RQ 02
    analyze_pull_requests(data)

    # RQ 03
    analyze_releases(data)

    # RQ 04
    analyze_last_update(data)

    # RQ 06
    analyze_closed_issues(data)

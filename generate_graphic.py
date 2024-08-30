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


def analyze_creation_dates(data, output_image='creation_dates_distribution.png'):
    """
    Analyzes the created_at column to show the distribution of repositories created per year.
    """
    # Extracting the years from the 'created_at' column
    creation_years = [datetime.strptime(row['created_at'], '%Y-%m-%dT%H:%M:%SZ').year for row in data]

    # Counting the occurrences of each year
    year_counts = Counter(creation_years)

    # Sorting the years for proper chronological order in the plot
    sorted_years = sorted(year_counts.items())
    years, counts = zip(*sorted_years) if sorted_years else ([], [])

    # Plotting the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(years, counts, color='green')
    plt.xlabel('Year')
    plt.ylabel('Number of Repositories Created')
    plt.title('Repositories Created per Year')

    plt.savefig(output_image)
    print(f"Creation date analysis saved as {output_image}")


if __name__ == "__main__":
    size = 1000
    file_name = "repos_details.csv"
    data = read_csv_to_dict(file_name)

    analyze_creation_dates(data)
    plot_language_distribution(data)

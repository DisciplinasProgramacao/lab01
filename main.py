import requests

token = ""

def get_popular_repos(size, headers):
    url = f"https://api.github.com/search/repositories"
    params = {
        "q": "stars:>0",
        "sort": "stars",
        "order": "desc",
        "per_page": size
    }
    response = requests.get(url,  params=params, headers=headers)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        raise Exception(f"Failed to fetch repositories: {response.status_code}")

def get_repos_details(repos, headers):
    repos_detail = []
    for repo in repos:
        # RQ01: Creation Date
        created_at = repo["created_at"]

        owner = repo["owner"]["login"]
        repo_name = repo["name"]

        # RQ02: Total accepted pull requests
        total_pulls = get_accepted_pull_requests(headers, owner, repo_name)

        # RQ03: Total releases
        total_releases = get_total_releases(headers, owner, repo_name)

        # RQ04: Last updated date
        updated_at = repo["updated_at"]

        # RQ05: Primary language
        language = repo["language"]

        # RQ06: Closed issues ratio
        closed_issues_ratio = get_closed_issues_ratio(headers, owner, repo_name)

        repos_detail.append({
            'name': repo["name"],
            'created_at': created_at,
            'total_pulls': total_pulls,
            'total_releases': total_releases,
            'updated_at': updated_at,
            'language': language,
            'closed_issues_ratio': closed_issues_ratio,
        })
    print(repos_detail)


def get_closed_issues_ratio(headers, owner, repo_name):
    issues_url = f"https://api.github.com/repos/{owner}/{repo_name}/issues"
    issues_params = {"state": "all", "per_page": 100}
    total_issues = []
    closed_issues = []

    while True:
        issues_response = requests.get(issues_url, params=issues_params, headers=headers)
        if issues_response.status_code != 200:
            break

        page_issues = issues_response.json()
        total_issues.extend(page_issues)
        closed_issues.extend(issue for issue in page_issues if issue['state'] == 'closed')

        if 'next' in issues_response.links:
            issues_url = issues_response.links['next']['url']
        else:
            break

    if len(total_issues) == 0:
        return 0

    closed_issues_ratio = round(len(closed_issues) / len(total_issues), 2)
    return closed_issues_ratio


def get_total_releases(headers, owner, repo_name):
    releases_url = f"https://api.github.com/repos/{owner}/{repo_name}/releases"
    releases_params = {"per_page": 100}
    total_releases = []

    while True:
        releases_response = requests.get(releases_url, params=releases_params, headers=headers)
        if releases_response.status_code != 200:
            break

        page_releases = releases_response.json()
        total_releases.extend(page_releases)

        if 'next' in releases_response.links:
            releases_url = releases_response.links['next']['url']
        else:
            break

    return len(total_releases)


def get_accepted_pull_requests(headers, owner, repo_name):
    pulls_url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
    pulls_params = {"state": "closed", "per_page": 100}
    total_pulls = []

    while True:
        pulls_response = requests.get(pulls_url, params=pulls_params, headers=headers)
        if pulls_response.status_code != 200:
            break

        pulls = pulls_response.json()
        total_pulls.extend(pulls)

        if 'next' in pulls_response.links:
            pulls_url = pulls_response.links['next']['url']
        else:
            break
    merged_count = sum(1 for pr in total_pulls if pr.get('merged_at') is not None)
    return merged_count


# Main
if __name__ == "__main__":

    size = 100
    headers = {"Authorization": f"token {token}"}
    try:
        popular_repos = get_popular_repos(size, headers)
        get_repos_details(popular_repos, headers)
    except Exception as e:
        print(e)

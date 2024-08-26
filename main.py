import csv
import requests

token = ""
headers = {"Authorization": f"Bearer {token}"}


def get_popular_repos(total_repos, headers):
    url = "https://api.github.com/graphql"
    repos = []
    after_cursor = None

    while len(repos) < total_repos:
        query = """
        query ($after: String) {
          search(query: "stars:>0", type: REPOSITORY, first: 100, after: $after) {
            pageInfo {
              endCursor
              hasNextPage
            }
            nodes {
              ... on Repository {
                name
                createdAt
                updatedAt
                primaryLanguage {
                  name
                }
                owner {
                  login
                }
                stargazerCount
              }
            }
          }
        }
        """
        variables = {"after": after_cursor}
        response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
        if response.status_code == 200:
            data = response.json()["data"]["search"]
            repos.extend(data["nodes"])
            after_cursor = data["pageInfo"]["endCursor"]
            if not data["pageInfo"]["hasNextPage"]:
                break
        else:
            raise Exception(f"Failed to fetch repositories: {response.status_code}")

    return repos[:total_repos]


def get_repo_details(repos, headers):
    repo_details = []
    url = "https://api.github.com/graphql"

    for repo in repos:
        print(f"Processing repository: {repo['name']}")
        owner = repo["owner"]["login"]
        repo_name = repo["name"]

        query = """
        query ($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            name
            createdAt
            updatedAt
            primaryLanguage {
              name
            }
            pullRequests(states: MERGED) {
              totalCount
            }
            releases {
              totalCount
            }
            issues(states: CLOSED) {
              totalCount
            }
            openIssues: issues(states: OPEN) {
              totalCount
            }
          }
        }
        """
        variables = {"owner": owner, "name": repo_name}
        response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)

        if response.status_code == 200:
            data = response.json()["data"]["repository"]
            closed_issues_ratio = (
                    data["issues"]["totalCount"] / (data["issues"]["totalCount"] + data["openIssues"]["totalCount"])
            ) if (data["issues"]["totalCount"] + data["openIssues"]["totalCount"]) > 0 else 0

            repo_details.append({
                'name': data["name"],
                'created_at': data["createdAt"],
                'total_pulls': data["pullRequests"]["totalCount"],
                'total_releases': data["releases"]["totalCount"],
                'updated_at': data["updatedAt"],
                'language': data["primaryLanguage"]["name"] if data["primaryLanguage"] else None,
                'closed_issues_ratio': round(closed_issues_ratio, 2),
            })
        else:
            raise Exception(f"Failed to fetch repository details: {response.status_code}")

    keys = repo_details[0].keys() if repo_details else []
    with open('repos_details.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(repo_details)

    print("Saved repository details to repos_details.csv")
    return repo_details


if __name__ == "__main__":
    size = 1000
    try:
        popular_repos = get_popular_repos(size, headers)
        repo_details = get_repo_details(popular_repos, headers)
        print(repo_details)
    except Exception as e:
        print(e)

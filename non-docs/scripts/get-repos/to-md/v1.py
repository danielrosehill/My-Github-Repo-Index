import requests

# Constants
GITHUB_API_URL = "https://api.github.com/users/danielrosehill/repos"
MARKDOWN_OUTPUT_FILE = "index.md"

def get_repositories():
    """Fetches repositories from the GitHub API and returns them."""
    repos = []
    page = 1
    per_page = 100  # GitHub allows up to 100 items per page

    while True:
        # Make a request to get the repositories, paginated
        response = requests.get(GITHUB_API_URL, params={'page': page, 'per_page': per_page})

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve repositories. Status code: {response.status_code}")
            break

        # Parse JSON response
        data = response.json()

        # If no more repositories, break the loop
        if not data:
            break

        # Add repos from this page to the list
        repos.extend(data)

        # Move to the next page
        page += 1

    return repos

def get_last_commit_date(repo_name):
    """Fetches the date of the last commit for a given repository."""
    commits_url = f"https://api.github.com/repos/danielrosehill/{repo_name}/commits"
    response = requests.get(commits_url)

    if response.status_code == 200:
        commits_data = response.json()
        if commits_data:
            return commits_data[0]['commit']['committer']['date']
    
    return "No commits found"

def write_repos_to_markdown(repos):
    """Writes repository information into a markdown table and saves it as index.md."""
    
    # Sort repositories by name alphabetically
    sorted_repos = sorted(repos, key=lambda x: x['name'])

    # Prepare markdown content
    with open(MARKDOWN_OUTPUT_FILE, mode='w', encoding='utf-8') as file:
        file.write("# GitHub Repositories\n\n")
        file.write("| Repository Name | Description | Creation Date | Last Commit Date | URL |\n")
        file.write("|-----------------|-------------|---------------|------------------|-----|\n")

        # Write repository data rows in markdown format
        for repo in sorted_repos:
            repo_name = repo['name']
            description = repo['description'] or "No description"
            creation_date = repo['created_at']
            last_commit_date = get_last_commit_date(repo_name)
            repo_url = repo['html_url']

            # Write each row in markdown table format
            file.write(f"| {repo_name} | {description} | {creation_date} | {last_commit_date} | [Link]({repo_url}) |\n")

def main():
    """Main function to fetch repositories and write them into a markdown file."""
    print("Fetching repositories...")
    repos = get_repositories()

    if repos:
        print(f"Fetched {len(repos)} repositories.")
        print("Writing to Markdown...")
        write_repos_to_markdown(repos)
        print(f"Repositories written to {MARKDOWN_OUTPUT_FILE}.")
    else:
        print("No repositories found.")

if __name__ == "__main__":
    main()
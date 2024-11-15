import requests
import csv

# Constants
GITHUB_API_URL = "https://api.github.com/users/danielrosehill/repos"
CSV_OUTPUT_FILE = "repos.csv"

def get_repositories():
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

def write_repos_to_csv(repos):
    # Sort repositories by name alphabetically
    sorted_repos = sorted(repos, key=lambda x: x['name'])
    
    # Write the sorted repositories to a CSV file
    with open(CSV_OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header row
        writer.writerow(['repo_name', 'repo_url'])
        
        # Write repository data rows
        for repo in sorted_repos:
            writer.writerow([repo['name'], repo['html_url']])

def main():
    print("Fetching repositories...")
    repos = get_repositories()
    
    if repos:
        print(f"Fetched {len(repos)} repositories.")
        print("Writing to CSV...")
        write_repos_to_csv(repos)
        print(f"Repositories written to {CSV_OUTPUT_FILE}.")
    else:
        print("No repositories found.")

if __name__ == "__main__":
    main()
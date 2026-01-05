import requests
import os
from dotenv import load_dotenv

load_dotenv()

github_token = os.getenv("github_token")

def get_github_contributions(gh_handle, token):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {token}"}

    query = """
    query($user: String!) {
      user(login: $user) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
                color
              }
            }
          }
        }
      }
    }
    """
    
    variables = {"user": gh_handle}
    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        calendar = data['data']['user']['contributionsCollection']['contributionCalendar']
        return calendar
    else:
        raise Exception(f"Query failed: {response.status_code}")

print(get_github_contributions("obayM", github_token))

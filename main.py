import requests
import os
from dotenv import load_dotenv

from PIL import Image, ImageDraw, ImageFont

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



def generate_wallpaper(gh_data, headline="Consistency is the key to mastery", out="bg.png", style="dark-silver"):
    cell_size = 15
    cell_margin =3
    text_height = 30


    num_weeks = len(gh_data['weeks'])
    img_width = 1920
    img_height = 1080

    grid_width = (num_weeks* (cell_size + cell_margin)) - cell_margin
    grid_height = (7 * (cell_size + cell_margin)) - cell_margin

    total_content_height = grid_height + text_height

    start_x = (img_width - grid_width) // 2
    start_y = (img_height - total_content_height) // 2
    

    img = Image.new("RGB", (img_width, img_height), color="white")
    draw = ImageDraw.Draw(img)
    
    try:

        draw.text((start_x, start_y), f"{gh_data['totalContributions']} contributions in the last year", fill="black")
    except:
        draw.text((start_x, start_y), f"Total: {gh_data['totalContributions']}", fill="black")

    for x, week in enumerate(gh_data['weeks']):
        for y, day in enumerate(week['contributionDays']):

            x0 = start_x + x * (cell_size + cell_margin) + cell_margin
            y0 = start_y + y * (cell_size + cell_margin) + cell_margin + text_height
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            
            draw.rectangle([x0, y0, x1, y1], fill=day['color'], outline="#eeeeee", width=1)

    img.save(out)
    print(f"Image saved as {out}")

generate_wallpaper(get_github_contributions("obayM",github_token))
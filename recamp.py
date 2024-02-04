import requests
from bs4 import BeautifulSoup
import csv
import time

def login(session, username, password):
    login_url = "https://ork.amtgard.com/orkui/index.php?Route=Login/login"
    try:
        response = session.post(login_url, data={"username": username, "password": password})
        if response.status_code == 200:
            print("Logged in successfully.")
        else:
            print(f"Login failed with status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Error during login: {e}")
        return False
    return True

def fetch_players(session, url):
    try:
        response = session.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch players from {url}. Status code: {response.status_code}")
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        players = {}
        for row in soup.select("table.information-table tbody tr"):
            cells = row.find_all('td')
            if len(cells) >= 3:  # Ensure there are enough cells
                player_link = cells[2].find('a')  # The player link is in the third cell
                if player_link and 'href' in player_link.attrs:
                    player_id = player_link['href'].split('/')[-1]
                    full_url = 'https://ork.amtgard.com' + player_link['href']
                    players[player_id] = {'url': full_url, 'name': player_link.get_text()}
        if not players:
            print(f"No players found at {url}")
        return players
    except requests.RequestException as e:
        print(f"Error fetching players from {url}: {e}")
        return None

def get_email(session, player_id):
    admin_url = f"https://ork.amtgard.com/orkui/index.php?Route=Admin/player/{player_id}"
    try:
        response = session.get(admin_url)
        if response.status_code != 200:
            print(f"Failed to fetch email for player {player_id}. Status code: {response.status_code}")
            return "EMAIL_NOT_FOUND"
        soup = BeautifulSoup(response.text, 'html.parser')
        email_field = soup.find('input', {'class': 'most-emails-field'})

        # Additional logging to understand what is being found
        if email_field:
            print(f"Found email field for player {player_id}: {email_field}")
            if 'value' in email_field.attrs:
                return email_field['value']
            else:
                print(f"Email field for player {player_id} does not have a value attribute.")
        else:
            print(f"No email field found for player {player_id}.")
            print(f"Page content: {soup.prettify()}[:1000]")  # Print first 1000 characters of the page

        return "EMAIL_NOT_FOUND"
    except requests.RequestException as e:
        print(f"Error fetching email for player {player_id}: {e}")
        return "EMAIL_NOT_FOUND"

# Main workflow
session = requests.Session()
if not login(session, 'your_username', 'your_password'):
    exit("Login failed, exiting script.")

active_players = fetch_players(session, "https://ork.amtgard.com/orkui/index.php?Route=Reports/active/Kingdom&id=11")
time.sleep(2)  # Rate limiting
dues_players = fetch_players(session, "https://ork.amtgard.com/orkui/index.php?Route=Reports/dues/Kingdom&id=11")

if active_players is None or dues_players is None:
    exit("Failed to fetch player data, exiting script.")

matched_players = {pid: active_players[pid] for pid in active_players if pid in dues_players}

if not matched_players:
    print("No matching players found.")
else:
    print(f"Found {len(matched_players)} matching players.")

for player_id, player_info in matched_players.items():
    email = get_email(session, player_id)
    player_info['email'] = email
    time.sleep(2)  # Rate limiting

# Save to CSV
with open('matched_players.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Player ID', 'URL', 'Name', 'Email'])
    for player_id, player_info in matched_players.items():
        writer.writerow([player_id, player_info['url'], player_info['name'], player_info['email']])

print("Data saved to matched_players.csv")

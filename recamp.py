import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime
import sys

def login(session, username, password):
    login_url = "https://ork.amtgard.com/orkui/index.php?Route=Login/login"
    try:
        response = session.post(login_url, data={"username": username, "password": password})
        if response.status_code == 200:
            print()
            print("Logged in successfully.")
            time.sleep(2)  # Rate limiting
        else:
            print()
            print(f"Login failed with status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print()
        print(f"Error during login: {e}")
        return False
    return True

def fetch_players(session, url):
    try:
        response = session.get(url)
        if response.status_code != 200:
            print()
            print(f"Failed to fetch players from {url}. Status code: {response.status_code}")
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        players = {}
        base_url = 'https://ork.amtgard.com'
        for row in soup.select("table.information-table tbody tr"):
            cells = row.find_all('td')
            if len(cells) >= 3:
                player_link = cells[2].find('a')
                if player_link and 'href' in player_link.attrs:
                    href = player_link['href']
                    full_url = href if href.startswith(base_url) else base_url + href
                    player_id = href.split('/')[-1]
                    players[player_id] = {'ork_id': player_id, 'ork_url': full_url, 'personaName': player_link.get_text()}
        if not players:
            print()
            print(f"No players found at {url}")
        return players
    except requests.RequestException as e:
        print()
        print(f"Error fetching players from {url}: {e}")
        return None

def get_player_details(session, player_id):
    admin_url = f"https://ork.amtgard.com/orkui/index.php?Route=Admin/player/{player_id}"
    try:
        response = session.get(admin_url)
        if response.status_code != 200:
            print()
            print(f"Failed to fetch details for player {player_id}. Status code: {response.status_code}")
            print()
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        email_field = soup.find('input', {'class': 'most-emails-field'})
        given_name_field = soup.find('input', {'id': 'GivenName'})
        surname_field = soup.find('input', {'id': 'Surname'})

        email = email_field['value'] if email_field and 'value' in email_field.attrs else "EMAIL_NOT_FOUND"
        firstname = given_name_field['value'] if given_name_field and 'value' in given_name_field.attrs else ""
        lastname = surname_field['value'] if surname_field and 'value' in surname_field.attrs else ""

        return {'email': email, 'firstname': firstname, 'lastname': lastname}
    except requests.RequestException as e:
        print()
        print(f"Error fetching details for player {player_id}: {e}")
        return None

# Progress bar function. Shamelessly stolen from Stack Exchange. Keeping the parameters comment for future reference.
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

session = requests.Session()
if not login(session, 'your_username', 'your_password'):
    print()
    exit("Login failed, exiting script.")

print("Comparing active and dues paid players...")
print()

active_players = fetch_players(session, "https://ork.amtgard.com/orkui/index.php?Route=Reports/active/Kingdom&id=11")
time.sleep(2)  # Rate limiting
dues_players = fetch_players(session, "https://ork.amtgard.com/orkui/index.php?Route=Reports/dues/Kingdom&id=11")

if active_players is None or dues_players is None:
    print()
    exit("Failed to fetch player data, exiting script.")

matched_players = {pid: active_players[pid] for pid in active_players if pid in dues_players}

total_players = len(matched_players)
print(f"{total_players} eligible players found.")
print()
time.sleep(.5)
print(f"Gathering details for {total_players} players. Please wait...")
print()

# Initial call to print 0% progress
print_progress_bar(0, total_players, prefix='Progress:', suffix='Complete', length=50)

# Iterate through matches and gather data.
for i, (player_id, player_info) in enumerate(matched_players.items(), 1):
    details = get_player_details(session, player_id)
    if details:
        player_info.update(details)
    time.sleep(2)  # Rate limiting
    print_progress_bar(i, total_players, prefix='Progress:', suffix='Complete', length=50)

time.sleep(.5)
print()
print("Detail collection complete.")

current_time = datetime.now().strftime('%Y%m%d%H%M')

filename = f'eligible_voters_{current_time}.csv'

# Save to CSV
with open(filename, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['ork_id', 'personaName', 'firstname', 'lastname', 'email', 'ork_url']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for player_info in matched_players.values():
        writer.writerow(player_info)

time.sleep(.5)
print()
print(f"Details saved to {filename}")

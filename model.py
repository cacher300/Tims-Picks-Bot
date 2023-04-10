def main():
  '''
  Known issue is that names like Jani Hakanpää with funky letters dont work but they irrelivant
  Player id to name is broken also because some names are diffrent in the api and the html
  it can also find players from another team if they have the same name
  '''
  import numpy as np
  from sklearn.linear_model import LogisticRegression
  from sklearn.model_selection import train_test_split
  from sklearn.preprocessing import StandardScaler
  import json
  import csv
  import requests
  import pandas as pd
  import os
  from bs4 import BeautifulSoup
  from unidecode import unidecode
  import random
  
  number = 0
  
  html_path = os.path.join(os.getcwd(), 'data.html')
  
  # Read the contents of the HTML file
  with open(html_path, 'r') as f:
      html_content = f.read()
  
  # Parse the HTML content with BeautifulSoup
  soup = BeautifulSoup(html_content, 'html.parser')
  
  # Find all the table tags in the HTML content
  tables = soup.find_all('table')
  
  base1 = []
  base2 = []
  base3 = []
  
  # Loop over each table and extract the info from the first column
  for index, table in enumerate(tables):
      # Skip the first table
      if index == 0:
          continue
      elif index == 1:
          # Extract results from second table
          rows = table.find_all('tr')
          for row in rows:
              cells = row.find_all('td')
              if len(cells) > 1:
                  name = cells[1].text.replace('\n', '')
                  base1.append(name)
      elif index == 2:
          # Extract results from third table
          rows = table.find_all('tr')
          for row in rows:
              cells = row.find_all('td')
              if len(cells) > 1:
                  name = cells[1].text.replace('\n', '')
                  base2.append(name)
      elif index == 3:
          # Extract results from fourth table
          rows = table.find_all('tr')
          for row in rows:
              cells = row.find_all('td')
              if len(cells) > 1:
                  name = cells[1].text.replace('\n', '')
                  base3.append(name)
  
  print(base1)
  print(base2)
  print(base3)
  
  print(len(base1))
  print(len(base2))
  print(len(base3))
  
  
  base3 = [unidecode(word) for word in base3]
  base2 = [unidecode(word) for word in base2]
  base1 = [unidecode(word) for word in base1]
  
  
  broken_names = ['Alexander Wennberg', 'Mitch Marner','T.J. Brodie']
  
  for i, item in enumerate(broken_names):
      for x in [base1, base2, base3]:
          if item in x:
              if item == 'Alexander Wennberg':
                  idx = x.index(item)
                  x.pop(idx)
                  x.insert(idx, 'Alex Wennberg')
              if item == 'Mitch Marner':
                  idx = x.index(item)
                  x.pop(idx)
                  x.insert(idx, 'Mitchell Marner')
              if item == 'T.J. Brodie':
                  idx = x.index(item)
                  x.pop(idx)
                  x.insert(idx, 'TJ Brodie')
  
  
  # Set the base URL for the NHL API
  base_url = "https://statsapi.web.nhl.com/api/v1"
  
  # Send a GET request to the teams endpoint of the NHL API and load the response into a JSON object
  response = requests.get(f"{base_url}/teams")
  teams = json.loads(response.text)
  
  # Initialize an empty list to store player information
  player_info = []
  
  part1 = []
  part2 = []
  part3 = []
  
  
  # Iterate through each team in the response from the NHL API
  for team in teams["teams"]:
      # Get the team ID and name from the team object
      team_id = team["id"]
      team_name = team["name"]
  
      # Set the endpoint for retrieving the roster for this team
      roster_endpoint = f"/teams/{team_id}/roster"
  
      # Send a GET request to the roster endpoint of this team and load the response into a JSON object
      response = requests.get(base_url + roster_endpoint)
      roster = json.loads(response.text)
  
      # Iterate through each player on this team's roster
      for player in roster["roster"]:
          # Get the player ID and name from the player object
          player_id = player["person"]["id"]
          player_name = player["person"]["fullName"]
  
  
          # Check if the player's name is in base1
          if player_name in base1:
              # Append the player's ID to part1
              part1.append(player_id)
  
          # Check if the player's name is in base2
          elif player_name in base2:
              # Append the player's ID to part2
              part2.append(player_id)
  
          # Check if the player's name is in base3
          elif player_name in base3:
              # Append the player's ID to part3
              part3.append(player_id)
  
  
  
  print("Part 1:", part1)
  print("Part 2:", part2)
  print("Part 3:", part3)
  
  lists = [part1, part2, part3]
  
  #lists = [part3] ################################################################################################
  
  
  # Initialize an empty list to store the results
  all_player_info = []
  
  # Loop through each list
  for player_list in lists:
  
      number = number + 1
  
      # Initialize an empty list to store player information
      player_info = []
  
      # Loop through each player in the list
      for i in player_list:
  
  
          api_url = f'https://statsapi.web.nhl.com/api/v1/people/{i}/stats?season=20222023&stats=gameLog'
  
          # Send request to API and extract JSON data
          response = requests.get(api_url)
          json_data = response.json()
  
          # Extract relevant data and create a DataFrame
          rows = []
          for split in json_data['stats'][0]['splits']:
              try:
                  shooting_pct = split['stat']['shotPct']
              except KeyError:
                  shooting_pct = 0.0
              opp_id = split['opponent']['id']
              opp_url = f'https://statsapi.web.nhl.com/api/v1/teams/{opp_id}?expand=team.stats&season=20222023'
              opp_response = requests.get(opp_url)
              opp_data = opp_response.json()
              opp_ga_per_gp = opp_data['teams'][0]['teamStats'][0]['splits'][0]['stat']['goalsAgainstPerGame']
              row = {
                  'date': split['date'],
                  'goals': split['stat']['goals'],
                  'shots': split['stat']['shots'],
                  'shooting_pct': shooting_pct,
                  'opp_id': opp_id,
                  'opp_name': split['opponent']['name'],
                  'opp_ga_per_gp': opp_ga_per_gp,
                  'scored': 1 if split['stat']['goals'] > 0 else 0,
              }
              rows.append(row)
  
          mcDavid_data = pd.DataFrame(rows)
  
          # Save DataFrame to CSV
          mcDavid_data.to_csv('mcdavid_2019_data.csv', index=False)
  
          gpg = f'https://statsapi.web.nhl.com/api/v1/people/{i}/stats?stats=statsSingleSeason&season=20222023'
          question = requests.get(gpg)
          json_data = question.json()
          games = json_data["stats"][0]["splits"][0]["stat"]["games"]
          shtpct = json_data["stats"][0]["splits"][0]["stat"]["shotPct"]
  
          # Set up the data
          goals = json_data["stats"][0]["splits"][0]["stat"]["goals"]
          gp = json_data["stats"][0]["splits"][0]["stat"]["games"]
          shooting_pct = float(json_data["stats"][0]["splits"][0]["stat"]["shotPct"])
          shots = float(json_data["stats"][0]["splits"][0]["stat"]["shots"]/gp)
          gpg = int(goals)/gp
  
          url = f"https://statsapi.web.nhl.com/api/v1/people/{i}/stats?stats=gameLog"
          nuggets = requests.get(url)
          team_id = nuggets.json()["stats"][0]["splits"][0]["team"]["id"]
          urml = f'https://statsapi.web.nhl.com/api/v1/teams/{team_id}/?expand=team.schedule.next'
          resfponse = requests.get(urml)
          data = resfponse.json()
          next_opponent_id = data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']['team']['id']
          url = f"https://statsapi.web.nhl.com/api/v1/teams/{next_opponent_id}/stats?stats=gameLog&season=20222023"
  
          response = requests.get(url)
          data = response.json()
  
          goalsAgainstPerGame = data["stats"][0]["splits"][0]["stat"]["goalsAgainstPerGame"]
          opp_gaa = goalsAgainstPerGame  # hypothetical opponent goals against average per game
          mcDavid_data = pd.read_csv('mcdavid_2019_data.csv')
  
  
          # Preprocess the data
          mcDavid_data['opp_strength'] = mcDavid_data['opp_ga_per_gp']
          X = mcDavid_data[['goals', 'shots', 'shooting_pct', 'opp_strength']]
          y = mcDavid_data['scored']
          with open("mcdavid_2019_data.csv") as csvfile:
              reader = csv.reader(csvfile)
              next(reader)  # Skip the header row
              total = 0
              for row in reader:
                  total += int(row[7])
  
              if total < 2:
                  player_fullnames = f'https://statsapi.web.nhl.com/api/v1/people/{i}'
                  response = requests.get(player_fullnames)
                  json_data = response.json()
                  full_name = json_data['people'][0]['fullName']
  
                  print(f"The predicted odds of {str(full_name)} scoring in a today's game is {0:.2%}")
                  player_info.append({'name': full_name, 'odds': 0})
                  continue
          average = 0
          average_odds = []
          percent = 0
  
          while average <= 30:
  
              # Split data into training and testing sets
              max_retry = 100  # Maximum number of retries
              retry_count = 0  # Counter for retries
              random_states = []  # List to store tried random_state values
  
              while retry_count < max_retry:
                  try:
                      random_state = random.randint(1, 100)  # Generate a random random_state value
                      if random_state in random_states:
                          continue  # Skip if random_state has already been tried
                      random_states.append(random_state)
                      random_states = []
                      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)
                      scaler = StandardScaler(with_mean=False)
                      X_train = scaler.fit_transform(X_train, y_train)
                      X_test = scaler.transform(X_test)
  
                      # Fit a logistic regression model
                      model = LogisticRegression()
                      model.fit(X_train, y_train)
  
                      # Evaluate the model
                      train_score = model.score(X_train, y_train)
                      test_score = model.score(X_test, y_test)
                      print(f'Train accuracy: {train_score:.4f}')
                      print(f'Test accuracy: {test_score:.4f}')
  
                      # Make predictions for a hypothetical game
  
                      opp_strength = opp_gaa
                      X_new = np.array([[gpg, shots, shooting_pct, opp_strength]])
                      X_new_scaled = scaler.transform(X_new)
                      odds = model.predict_proba(X_new_scaled)[0][1]
                      player_fullnames = f'https://statsapi.web.nhl.com/api/v1/people/{i}'
                      response = requests.get(player_fullnames)
                      json_data = response.json()
                      full_name = json_data['people'][0]['fullName']
  
                      print(f"The predicted odds of {str(full_name)} scoring in a today's game is {odds:.2%}")
                      average_odds.append(odds)
                      average = average + 1
                      break
                  except ValueError as e:
                      if "This solver needs samples of at least 2 classes in the data, but the data contains only one class" in str(
                              e):
                          print("Error: The data contains only one class. Retrying...")
                      else:
                          # Print the original error message and retry
                          print(f"Error: {e}. Retrying...")
                      retry_count += 1
                      continue
  
              if retry_count == max_retry:
                  print("Maximum retries reached. Could not generate suitable random_state value.")
              percent = sum(average_odds) / len(average_odds)
          player_info.append({'name': full_name, 'odds': percent})
          print(percent)
  
      player_info = sorted(player_info, key=lambda x: x['odds'], reverse=True)
  
      # Print the chart
      print('Player\t\tPredicted Odds')
      print('--------------------------------')
      for info in player_info:
          print(f'{info["name"]}\t{info["odds"]:.2%}')
      with open(f'pick{number}.csv', 'w', newline='') as f:
          writer = csv.writer(f)
          for info in player_info[:len(player_list)]:
              writer.writerow([info['name'], info['odds']])


  
  
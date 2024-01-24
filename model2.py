def main2():
  import requests
  import csv
  # Function to calculate scoring likelihood
  def calculate_scoring_likelihood(player):
      # Use the shooting percentage value if it's already a float
      shooting_percentage = player['shootingPercentage']
      power_play_minutes, power_play_seconds = map(int, player['powerPlayTimeOnIcePerGame'].split(':'))
      power_play_time = power_play_minutes + power_play_seconds / 60
      gpg = player['goalsPerGame']
      spg = player['shotsPerGame']
      pptoi_factor = power_play_time * 0.1
      opponent_gaa_factor = player['opponentGAA'] * 0.1
      scoring_index = (gpg * shooting_percentage) + spg + pptoi_factor - opponent_gaa_factor
      return scoring_index
  
  # Function to calculate percentage chance
  def calculate_percentage_chance(category):
      for player in category:
          player['Scoring Likelihood Index'] = calculate_scoring_likelihood(player)
      total_index = sum(player['Scoring Likelihood Index'] for player in category)
      for player in category:
          player['Percentage Chance'] = (player['Scoring Likelihood Index'] / total_index) * 100
  
  # Fetching the JSON data from the URL
  url = "https://api.hockeychallengehelper.com/api/picks"
  response = requests.get(url)
  json_data = response.json()
  
  # Extracting player data
  players = [player for player_list in json_data["playerLists"] for player in player_list["players"]]
  
  # Divide players into three categories
  category_1 = players[:15]
  category_2 = players[15:30]
  category_3 = players[30:45]
  
  # Apply the calculation to each category
  calculate_percentage_chance(category_1)
  calculate_percentage_chance(category_2)
  calculate_percentage_chance(category_3)
  
  # Function to write player data to a text file
  def write_to_file_decimal(category, filename):
      # Sorting players in descending order of their percentage chance
      sorted_category = sorted(category, key=lambda x: x['Percentage Chance'], reverse=True)
      with open(filename, 'w') as file:
          for player in sorted_category:
              # Converting percentage to decimal (e.g., 75.0% to 0.75)
              decimal_chance = player['Percentage Chance'] / 100
              file.write(f"{player['fullName']}, {decimal_chance:.2f}\n")
  
  
  # Writing each sorted category to a separate CSV file
  write_to_file_decimal(category_1, 'pick1.csv')
  write_to_file_decimal(category_2, 'pick2.csv')
  write_to_file_decimal(category_3, 'pick3.csv')
  
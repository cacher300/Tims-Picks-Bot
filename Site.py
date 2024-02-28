from datetime import datetime, timedelta
import time
import requests
from model import main

def get_upcoming_games(api_url):
    response = requests.get(api_url)
    schedule_data = response.json()
    current_utc = datetime.utcnow()
    current_date = current_utc.date()
    upcoming_games = []

    for game_week in schedule_data['gameWeek']:
        for game in game_week['games']:
            start_time_utc = game['startTimeUTC']
            game_time = datetime.strptime(start_time_utc, "%Y-%m-%dT%H:%M:%SZ")

            # Check if the game is today and in the future
            if game_time.date() == current_date and game_time > current_utc:
                upcoming_games.append(game_time)

    print(len(upcoming_games))
    return upcoming_games
def schedule_games_run():
    api_url = "https://api-web.nhle.com/v1/schedule/now"
    upcoming_games = get_upcoming_games(api_url)

    for game_time in upcoming_games:
        run_time = game_time + timedelta(minutes=20)
        wait_seconds = (run_time - datetime.utcnow()).total_seconds()

        if wait_seconds > 0:
            print(f"Scheduling 'main' to run in {wait_seconds} seconds.")
            time.sleep(wait_seconds)
            main()

def timer():
    while True:
        schedule_games_run()
        now = datetime.now()
        next_run = (now + timedelta(days=1)).replace(hour=5, minute=0, second=0, microsecond=0)
        sleep_seconds = (next_run - now).total_seconds()

        print(f"Sleeping for {sleep_seconds}")
        time.sleep(sleep_seconds)

        schedule_games_run()



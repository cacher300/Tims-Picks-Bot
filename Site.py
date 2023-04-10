
def timer():
  import datetime
  import time
  import requests
  from Text import texts
  from model import main

  while True:
      # Get the current time
      now = datetime.datetime.now()
  
      # Check if it's 3:00am
      if now.hour == 4 and now.minute == 5 and now.second == 40:
  
          url = "http://www.hockeychallengepicks.ca/"
          response = requests.get(url)
          
  
          source_code = response.text
          with open("data.html", "w") as f:
              f.write(source_code)
          print("Website source code extracted")
          main()
          texts()
  
          # Add any other code you want to run at this time
  
      # Wait for one second before checking the time again
      time.sleep(1)
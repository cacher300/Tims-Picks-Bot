def texts():
  import csv
  from twilio.rest import Client
  # Replace with your Twilio account SID, auth token, and phone numbers
  account_sid = 'AC0eb057fb44d08943f92000230268f4ae'
  auth_token = '4e289897f3141444e6cca6690dd4761f'
  from_number = '+19295564501'
  to_number = '+19053598346'
  
  def send_message_for_csv(csv_file):
      # Read the CSV file and extract the top 3 items
      with open(csv_file, 'r') as csvfile:
          reader = csv.reader(csvfile)
          top_items = sorted(reader, key=lambda row: float(row[1]), reverse=True)[:3]  # Sort by odds and get top 3
  
      # Prepare the message body
      message_body = f'{csv_file} choices:\n'
      for item in top_items:
          name = item[0]
          odds = float(item[1]) * 100  # Convert odds to percentage
          message_body += f'{name}: {odds:.2f}%\n'
  
      # Send the text message using Twilio API
      client = Client(account_sid, auth_token)
      message = client.messages.create(
          body=message_body,
          from_=from_number,
          to=to_number
      )
  
      print(f'Sent message SID: {message.sid}')
  
  
  # Call the function for each CSV file
  csv_files = ['pick1.csv', 'pick2.csv', 'pick3.csv']  # Update with your actual file names
  for csv_file in csv_files:
      send_message_for_csv(csv_file)
  
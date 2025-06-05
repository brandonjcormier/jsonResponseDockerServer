from flask import Flask
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Initialize global variables
lastSuccessfulCheck = None
response = None
jsonResponse = None

#################### CONFIGURATION ####################

# The URL to check
urlToCheck = 'https://web-api.nordvpn.com/v1/ips/info'

# How long before we check the URL again after a sucessful check
refreshTime = 30

#################### CONFIGURATION ####################

# How many times the app has tried to get a response
runCount = 0

startTime = datetime.now(timezone('MST'))

def fetchUrlRequest():
    global lastSuccessfulCheck, runCount, response, jsonResponse  # Indicates modification of global variables
    while True:
        try:
            response = requests.get(urlToCheck, timeout=10).text
            jsonResponse = json.loads(response)

            lastSuccessfulCheck = datetime.now(timezone('MST'))

            # Increment the counter for each fetch attempt
            runCount += 1  
            
            # Logging
            print(f'Request successfully completted at {lastSuccessfulCheck.strftime("%I:%M:%S %p %Z")}')
            print(f'Run count: {runCount}')

            # Exit the loop on success
            break
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch request: {e}. Retrying in 5 seconds...")
            time.sleep(5)

@app.route('/')
def web_page():
    # Get current time
    currentTime = datetime.now(timezone('MST'))

    # Calculate how long the script has been running
    uptime = currentTime - startTime

    # Format the uptime into a more readable string format
    uptime_str = str(timedelta(seconds=int(uptime.total_seconds())))
    
    # Provide different responses based on whether the request has been fetched successfully
    if lastSuccessfulCheck and response:
        return jsonResponse
    else:
        return f'<h2>The request has not been sent yet. Please wait {refreshTime} seconds.</h2>'

if __name__ == '__main__':
    # Get the background schedular set up
    scheduler = BackgroundScheduler()

    # Set the schedule for how often to check the URL
    scheduler.add_job(fetchUrlRequest, 'interval', seconds=refreshTime)

    scheduler.start()

    # Run the app over the network on port 1237
    app.run(host='0.0.0.0', port=1237, use_reloader=False)
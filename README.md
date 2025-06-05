This is a simple Python app that creates a web server which pings a URL and displays the response in the app. I use this primararily to monitor the public IP of the Gluetun container I am running through NordVPN. I can use this to display the IP and some details in my Glance homescreen.


To build the code into a Docker image, navigate to the root directory in a terminal and run (without quotes):

"sudo docker build -t ipmonitoring ."

Then you can start up the docker container:

"sudo docker compose up -d"

This code is preconfigured to run the container through a Gluetun container I have running. If you just want to run the web server without it you can uncomment the ports in the docker-compose.yml and remove this line:

network_mode: container:gluetun

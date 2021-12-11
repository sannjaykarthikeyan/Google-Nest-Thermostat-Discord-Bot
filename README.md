# Google-Nest-Thermostat-Discord-Bot (V2.0.0)
Discord bot that controls temperature and thermostat mode of your Google Nest Thermostat. Uses Pycord and Google Device Access API to access and change thermostat settings. 

**IMPORTANT: READ README.MD BEFORE ATTEMPTING TO USE PROGRAM.**

Instructions: 

1. Create a Discord Bot using the Discord Developer portal. The Developer Portal can be found Here: https://discord.com/developers/applications

A tutorial to create a discord bot can be found here. Follow steps 1-4.
https://www.digitaltrends.com/gaming/how-to-make-a-discord-bot/

Take note of your bot token. DO NOT SHARE THIS TOKEN.

2. Follow the steps in this guide to create a Google Cloud Console Project:
https://www.wouternieuwerth.nl/controlling-a-google-nest-thermostat-with-python/
(P.S A non-refundable $5 USD fee paid to Google is required to create a Google Cloud Console Project)

This is a requirement in order to access your project ID, your client ID and your client secret. DO NOT SHARE
ANY OF THESE VALUES.

3. Using a Python IDE (Preferably Visual Studio Code), copy the code from discordbot.py in this repository
and replace the project id, client id and client secret with your own values.

4. Deploy/run the bot in your discord server and use the commands ?verify, ?code and ?setTemp to interact with the bot
and control your thermostat.







Commands:

?verify -> Grabs user access token from their URL. Necessary for Google Device Access API.

      Example:

      "?verify"

      "The following is used for verification purposes:

      Go to this URL to log in:

      (you would paste your url here)

      After that, use ?code to paste your URL as a message."
      
?code -> Receives user's access token from URL. 

(?verify has to be used to get URL before using this command.)

      Example:
      
      "?code (url you received from the previous command here)"
      
      "Code received. Please wait...
       Current Humidity:
       58
       Current Temperature:
       23.329987"
       
 ?setTemp(userPref_ThermostatMode, set_temp_to) -> Changes the thermostat mode and temperature.
 
      Example:
      
      "?setTemp HEAT 22"
      
      "Temperature set. Please check your thermostat to confirm."
      
?cmds -> Displays commands

?currentTemp -> Displays current temperature.

?currentHumidity -> Displays current humidity.

Credits: 

Wouter Nieuwerth: "Controlling a Google Nest Thermostat with Python".
The code from their tutorial has been used in this repository.
Their website: https://www.wouternieuwerth.nl/
 
      

*/ 
IMPORTANT: THERE ARE MULTIPLE
STEPS TO FOLLOW BEFORE USING THIS DISCORD BOT.
REFER TO THE GUIDE IN README BEFORE USING THIS BOT. THIS BOT WILL NOT FUNCTION
WITHOUT THE SETUP OF YOUR GOOGLE DEVICE ACCESS PROJECT. 
*/

import discord
import requests
from discord.ext import commands
import random
import re
verified = False
global url_set_mode

// Replace these variables with your own values. Refer to README to setup Device Access Project and create values.
project_id = 'your-project-id-here'
client_id = 'your-client-id-here'
client_secret = 'your-client-secret-here'

// Do not change this. The redirect url will contain your access token to control your thermostat.
redirect_uri = 'https://www.google.com'

description = """Discord bot that controls temperature and thermostat mode of your Google
Nest Thermostat. Uses Pycord and Google Device Acceess API."""

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="?", description=description, intents=intents)

// Event that confirms that the bot has logged in successfully.
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

// Bot command that grabs user access token from their URL. Assumes that you have already setup Google Device Access Project (React to README)
@bot.command()
async def verify(ctx):
    await ctx.send("The following is used for verification purposes: ")
    url = 'https://nestservices.google.com/partnerconnections/' + project_id + '/auth?redirect_uri=' + redirect_uri + '&access_type=offline&prompt=consent&client_id=' + client_id + '&response_type=code&scope=https://www.googleapis.com/auth/sdm.service'
    await ctx.send("Go to this URL to log in: ")
    await ctx.send(url)
    await ctx.send("\nAfter that, use ?code to paste your URL as a message.\n")

// Bot command that receives user's access token from URL
@bot.command()
async def code(ctx, code: str):
    code = code.replace('&scope=https://www.googleapis.com/auth/sdm.service', '')
    code = code.replace('https://www.google.com/?code=', '')
    await ctx.send("\nCode received. Please wait...")
    # await ctx.send("Your code is\n" + code)
    # verified = True
    await ctx.send(verified)
    import requests

    params = (
        ('client_id', client_id),
        ('client_secret', client_secret),
        ('code', code),
        ('grant_type', 'authorization_code'),
        ('redirect_uri', redirect_uri),
    )

    response = requests.post('https://www.googleapis.com/oauth2/v4/token', params=params)

    response_json = response.json()
    access_token = response_json['token_type'] + ' ' + str(response_json['access_token'])
    refresh_token = response_json['refresh_token']

    params = (
        ('client_id', client_id),
        ('client_secret', client_secret),
        ('refresh_token', refresh_token),
        ('grant_type', 'refresh_token'),
    )

    response = requests.post('https://www.googleapis.com/oauth2/v4/token', params=params)

    response_json = response.json()
    access_token = response_json['token_type'] + ' ' + response_json['access_token']

    url_structures = 'https://smartdevicemanagement.googleapis.com/v1/enterprises/' + project_id + '/structures'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': access_token,
    }

    response = requests.get(url_structures, headers=headers)


    url_get_devices = 'https://smartdevicemanagement.googleapis.com/v1/enterprises/' + project_id + '/devices'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': access_token,
    }

    response = requests.get(url_get_devices, headers=headers)

    response_json = response.json()
    device_0_name = response_json['devices'][0]['name']
    url_get_device = 'https://smartdevicemanagement.googleapis.com/v1/' + device_0_name

    headers = {
        'Content-Type': 'application/json',
        'Authorization': access_token,
    }

    response = requests.get(url_get_device, headers=headers)

    response_json = response.json()

    humidity = response_json['traits']['sdm.devices.traits.Humidity']['ambientHumidityPercent']

    await ctx.send("Current Humidity: " + humidity)

    temperature = response_json['traits']['sdm.devices.traits.Temperature']['ambientTemperatureCelsius']

    await ctx.send("Current Temp: " + temperature)

    url_set_mode = 'https://smartdevicemanagement.googleapis.com/v1/' + device_0_name + ':executeCommand'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': access_token,
    }

    // Bot command for user to set thermostat mode and temp. Example: ?setTemp HEAT 23.0
    // Only accepts the values "HEAT" or "COOL" for thermostat mode
    // Temperature has to be a decimal value.
    @bot.command()
    async def setTemp(ctx, userPref_ThermostatMode: str, set_temp_to: float):

        await ctx.send("Temperature")

        if userPref_ThermostatMode == "HEAT":
            data = '{ "command" : "sdm.devices.commands.ThermostatMode.SetMode", "params" : { "mode" : "HEAT" } }'
            data = '{"command" : "sdm.devices.commands.ThermostatTemperatureSetpoint.SetHeat", "params" : {"heatCelsius" : ' + str(
                        set_temp_to) + '} }'
            print("Temperature set to HEAT" + "\nSuccess.")

        if userPref_ThermostatMode == "COOL":

            data = '{ "command" : "sdm.devices.commands.ThermostatMode.SetMode", "params" : { "mode" : "COOL" } }'
            data = '{"command" : "sdm.devices.commands.ThermostatTemperatureSetpoint.SetCool", "params" : {"coolCelsius" : ' + str(
                    set_temp_to) + '} }'
            print("Temperature set to COOL" + "\nSuccess.")
            
        url_set_mode = 'https://smartdevicemanagement.googleapis.com/v1/' + device_0_name + ':executeCommand'

        headers = {
                'Content-Type': 'application/json',
                'Authorization': access_token,
            }

        response = requests.post(url_set_mode, headers=headers, data=data)

        print(response.json())

       
// Insert the token for your bot.
bot.run("your-token")

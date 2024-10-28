import requests
from bs4 import BeautifulSoup
from discord.ext import commands


class WeatherInfo(commands.Cog):
        def __init__(self, bot):
            self.bot = bot


        @commands.command(name="tiempo", help="Responde con los datos meteorológicos de la ciudad que le digas.")
        async def get_weather_info(self, ctx, city=None):
            if city:
                url = "https://www.google.com/search?q=weather " + city
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/123.0.2420.97"}
                html = requests.get(url, headers=headers).content
                soup = BeautifulSoup(html, 'html.parser')
                try:
                    response = format_weather_response(soup, city)
                    await ctx.send(response)
                except:
                    await ctx.send(f"No se han podido encontrar datos meteorológicos de '{city}'.")
            else:
                await ctx.send("El formato del comando es: '!tiempo <<nombre_ciudad>>'.")


def format_weather_response(soup, city):
    time = soup.find("div", attrs={'id': 'wob_dts'}).text
    sky = soup.find("span", attrs={'id': 'wob_dc'}).text
    temperature = soup.find("span", attrs={'id': 'wob_tm'}).text
    rain_chance = soup.find("span", attrs={'id': 'wob_pp'}).text
    humidity = soup.find("span", attrs={'id': 'wob_hm'}).text
    wind = soup.find("span", attrs={'id': 'wob_ws'}).text

    formatted_response = f"Ciudad: {city.capitalize()}\nHora: {time.capitalize()}\nCielo: {sky.capitalize()}\nTemperatura: {temperature} °C\nPrecipitaciones: {rain_chance}\nHumedad: {humidity}\nViento: {wind}"

    return formatted_response
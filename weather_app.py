from datetime import datetime
import pyowm
import streamlit as st
from matplotlib import dates
from matplotlib import pyplot as plt

# Use Streamlit secrets to fetch the secret API key.
api_key = st.secrets["API_KEY"]

sign = u"\N{DEGREE SIGN}"
owm = pyowm.OWM(api_key)
mgr = owm.weather_manager()

st.title("Weather Forecaster")
st.write("## *Made by Shubham with* :heart:")
st.write("### Enter the city name, choose a Temperature unit and a graph type from below:")

location = st.text_input("Name of The City :", "")
units = st.selectbox("Select Temperature Unit:", ('celsius', 'fahrenheit'))
graph = st.selectbox("Select Graph Type:", ('Bar Graph', 'Line Graph'))

degree = 'C' if units == 'celsius' else 'F'


# ---------- Helper Functions ---------- #

def get_temperature():
    """Get the max and min temperature for the next 5 days."""
    forecaster = mgr.forecast_at_place(location, '3h')
    forecast = forecaster.forecast

    days, dates_list, temp_min, temp_max = [], [], [], []

    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date = day.date()
        if date not in dates_list:
            dates_list.append(date)
            temp_min.append(None)
            temp_max.append(None)
            days.append(date)

        temp = weather.temperature(unit=units)['temp']
        if not temp_min[-1] or temp < temp_min[-1]:
            temp_min[-1] = temp
        if not temp_max[-1] or temp > temp_max[-1]:
            temp_max[-1] = temp
    return days, temp_min, temp_max


def plot_bar_graph_temp():
    """Plot the 5-day bar graph of min and max temperatures."""
    st.write("_____________________________________")
    st.title("5 Day Min and Max Temperature")

    days, temp_min, temp_max = get_temperature()
    days = dates.date2num(days)

    fig, ax = plt.subplots()
    plt.style.use('ggplot')
    ax.bar(days - 0.25, temp_min, width=0.5, color='#42bff4', label='Min')
    ax.bar(days + 0.25, temp_max, width=0.5, color='#ff5349', label='Max')

    ax.set_xlabel('Day')
    ax.set_ylabel(f'Temperature ({sign}{degree})')
    ax.set_title("Weekly Forecast")
    ax.legend(fontsize='x-small')

    xaxis_format = dates.DateFormatter('%m/%d')
    ax.xaxis.set_major_formatter(xaxis_format)

    # Annotate bars with values
    for bars in [ax.patches]:
        for bar in ax.patches:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                    f"{int(height)}{sign}", ha='center', va='bottom', color='white')

    st.pyplot(fig)


def plot_line_graph_temp():
    """Plot line graph for min and max temperature."""
    st.write("_____________________________________")
    st.title("5 Day Min and Max Temperature")

    days, temp_min, temp_max = get_temperature()
    days = dates.date2num(days)

    fig, ax = plt.subplots()
    plt.style.use('ggplot')
    ax.plot(days, temp_min, label='Min', color='#42bff4', marker='o')
    ax.plot(days, temp_max, label='Max', color='#ff5349', marker='o')

    ax.set_xlabel('Day')
    ax.set_ylabel(f'Temperature ({sign}{degree})')
    ax.set_title("Weekly Forecast")
    ax.legend(fontsize='x-small')

    xaxis_format = dates.DateFormatter('%m/%d')
    ax.xaxis.set_major_formatter(xaxis_format)

    st.pyplot(fig)


def weather_forcast():
    """Display current weather."""
    obs = mgr.weather_at_place(location)
    weather = obs.weather
    icon = weather.weather_icon_url(size='4x')

    temp = weather.temperature(unit=units)['temp']
    temp_felt = weather.temperature(unit=units)['feels_like']
    st.image(icon, caption=(weather.detailed_status).title())
    st.markdown(f"## 🌡️ Temperature: **{round(temp)}{sign}{degree}**")
    st.write(f"### Feels Like: {round(temp_felt)}{sign}{degree}")
    st.write(f"### ☁️ Clouds Coverage: {weather.clouds}%")
    st.write(f"### 💨 Wind Speed: {weather.wind()['speed']} m/s")
    st.write(f"### 💧 Humidity: {weather.humidity}%")
    st.write(f"### ⏲️ Pressure: {weather.pressure['press']} mBar")
    st.write(f"### 🛣️ Visibility: {weather.visibility(unit='kilometers')} km")


def upcoming_weather_alert():
    """Show upcoming weather alerts."""
    forecaster = mgr.forecast_at_place(location, '3h')
    st.write("_____________________________________")
    st.title("Upcoming Weather Alerts")

    alerts = []
    if forecaster.will_have_clouds():
        alerts.append("Cloud Alert ⛅")
    if forecaster.will_have_rain():
        alerts.append("Rain Alert 🌧️")
    if forecaster.will_have_snow():
        alerts.append("Snow Alert ❄️")
    if forecaster.will_have_hurricane():
        alerts.append("Hurricane Alert 🌀")
    if forecaster.will_have_tornado():
        alerts.append("Tornado Alert 🌪️")
    if forecaster.will_have_fog():
        alerts.append("Fog Alert 🌫️")
    if forecaster.will_have_storm():
        alerts.append("Storm Alert 🌩️")

    if alerts:
        for alert in alerts:
            st.write(f"### - {alert}")
    else:
        st.write("### No Upcoming Alerts!")


def sunrise_sunset():
    """Show sunrise and sunset times."""
    st.write("_____________________________________")
    st.title("Sunrise and Sunset")
    obs = mgr.weather_at_place(location)
    weather = obs.weather

    sunrise_unix = datetime.utcfromtimestamp(int(weather.sunrise_time()))
    sunset_unix = datetime.utcfromtimestamp(int(weather.sunset_time()))

    st.write(f"#### 🌅 Sunrise: {sunrise_unix.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    st.write(f"#### 🌇 Sunset: {sunset_unix.strftime('%Y-%m-%d %H:%M:%S UTC')}")


def get_humidity():
    """Get humidity data for 5 days."""
    days, dates_list, humidity_max = [], [], []
    forecaster = mgr.forecast_at_place(location, '3h')
    forecast = forecaster.forecast

    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date = day.date()
        if date not in dates_list:
            dates_list.append(date)
            humidity_max.append(None)
            days.append(date)

        humidity = weather.humidity
        if not humidity_max[-1] or humidity > humidity_max[-1]:
            humidity_max[-1] = humidity

    return days, humidity_max


def plot_humidity_graph():
    """Plot humidity levels for 5 days."""
    st.write("_____________________________________")
    st.title("Humidity Index of 5 Days")

    days, humidity = get_humidity()
    days = dates.date2num(days)

    fig, ax = plt.subplots()
    plt.style.use('ggplot')
    ax.bar(days, humidity, color='#42bff4')

    ax.set_xlabel('Day')
    ax.set_ylabel('Humidity (%)')
    ax.set_title('Humidity Forecast')

    xaxis_format = dates.DateFormatter('%m/%d')
    ax.xaxis.set_major_formatter(xaxis_format)

    for bar in ax.patches:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height,
                f"{height}%", ha='center', va='bottom', color='white')

    st.pyplot(fig)


# ---------- Main ---------- #
if __name__ == '__main__':
    if st.button('Submit'):
        if location == '':
            st.warning('Provide a city name!!')
        else:
            try:
                weather_forcast()
                if graph == 'Bar Graph':
                    plot_bar_graph_temp()
                elif graph == 'Line Graph':
                    plot_line_graph_temp()

                upcoming_weather_alert()
                sunrise_sunset()
                plot_humidity_graph()
            except Exception as e:
                st.exception(e)

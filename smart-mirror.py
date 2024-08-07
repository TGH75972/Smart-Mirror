import tkinter as tk
from tkinter import Label
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

CITY = 'London'
NEWS_SOURCE = 'bbc-news'
NEWS_API_KEY = 'newws_api_heree!'

def get_weather():
    url = f'https://wttr.in/{CITY}?format=%t'
    response = requests.get(url)
    temp = response.text.strip()
    
    weather_desc_url = f'https://wttr.in/{CITY}?format=%C'
    response = requests.get(weather_desc_url)
    weather = response.text.strip()
    
    return temp, weather

def get_news():
    url = f'https://newsapi.org/v2/top-headlines?sources={NEWS_SOURCE}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    
    try:
        data = response.json()
        if 'articles' not in data:
            raise ValueError("Unexpected response structure")
        
        headlines = [article['title'] for article in data['articles'][:5]]
        return headlines
    
    except requests.RequestException:
        return ["Unable to fetch news"]
    
    except ValueError:
        return ["Unexpected response"]

def get_quote():
    response = requests.get('https://api.quotable.io/random')
    data = response.json()
    quote = f"{data['content']} — {data['author']}"
    return quote

def update_info():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    
    temp, weather = get_weather()
    headlines = get_news()
    quote = get_quote()

    time_label.config(text=f"Time: {current_time}")
    date_label.config(text=f"Date: {current_date}")
    weather_label.config(text=f"Weather: {temp}, {weather}")
    
    news_text = "\n".join([f"- {headline}" for headline in headlines])
    news_label.config(text=f"Headlines:\n{news_text}")

    quote_label.config(text=f"Quote of the Day:\n{quote}")

    root.after(60000, update_info)

def generate_temperature_graph():
    times = [datetime.now() - timedelta(minutes=i) for i in range(60)]
    temps = [float(get_weather()[0].replace('°C', '')) + (i % 5 - 2) for i in range(60)]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(times, temps, label='Temperature')
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Temperature Trend')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

root = tk.Tk()
root.title("Smart Mirror")

root.attributes('-fullscreen', True)
root.configure(bg='black')

time_label = Label(root, font=('Arial', 30), fg='white', bg='black')
time_label.pack(pady=10)

date_label = Label(root, font=('Arial', 24), fg='white', bg='black')
date_label.pack(pady=5)

weather_label = Label(root, font=('Arial', 24), fg='white', bg='black')
weather_label.pack(pady=5)

news_label = Label(root, font=('Arial', 16), fg='white', bg='black', justify='left')
news_label.pack(pady=10)

quote_label = Label(root, font=('Arial', 16), fg='white', bg='black', justify='left')
quote_label.pack(pady=10)

greeting_label = Label(root, font=('Arial', 20), fg='white', bg='black')
greeting_label.pack(pady=10)

graph_frame = tk.Frame(root, bg='black')
graph_frame.pack(fill='both', expand=True, padx=10, pady=10)

def set_greeting():
    now = datetime.now()
    hour = now.hour
    if hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    greeting_label.config(text=greeting)

set_greeting()
update_info()
generate_temperature_graph()

root.mainloop()

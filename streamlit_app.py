import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

title = "<h3 style='text-align: center; font-family: Arial, sans-serif; color: pink;'>PowerBall & Mega Millions Checker</h1>"
st.markdown(title, unsafe_allow_html=True)

input[type=range]::-webkit-slider-runnable-track {
  background-color: blue;
}

input[type=range]::-webkit-slider-thumb {
  background-color: blue;
}

input[type=range]::-moz-range-track {
  background-color: blue;
}

input[type=range]::-moz-range-thumb {
  background-color: blue;
}

def get_megamillions_data():
    url = "https://www.lotteryusa.com/mega-millions/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.select('.c-result-card')
    
    winning_numbers = []
    drawing_dates = []

    for row in rows:
        date = row.select_one('.c-result-card__title').text.strip()
        megaball = [int(n.text) for n in row.select('.c-result__item.c-result__bonus-ball .c-ball.c-ball--yellow')]
        numbers = [int(num.text.strip()) for num in row.select('.c-ball.c-ball--default.c-result__item')]

        drawing_dates.append(date)
        winning_numbers.append(numbers + megaball)
    
    return winning_numbers, drawing_dates

    
# Function to get Powerball numbers and dates
def get_powerball_data():
    url = 'https://www.powerball.com/previous-results?gc=powerball'
    params = {
        'game': 'powerball',
        'p': '',
        'pn': '',
        'pp': ''
    }

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    winning_data = soup.select('#searchNumbersResults > div.d-flex.gap-3.flex-column > a')

    winning_numbers = []
    drawing_dates = []
    for data in winning_data:
        date = data.select_one('div > div > div:nth-child(1) > div > h5').text.strip()
        numbers = data.select('div.white-balls.item-powerball')
        powerball = data.select('div.powerball.item-powerball')
        winning_numbers.append([int(n.text) for n in numbers] + [int(p.text) for p in powerball])
        drawing_dates.append(date)

    return winning_numbers, drawing_dates

def create_html_table(dataframe, lottery_game):
    table_html = '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">'
    table_html += "<tr><th>Date</th><th>Winning Numbers</th></tr>"
    
    for index, row in dataframe.iterrows():
        table_html += "<tr>"
        table_html += f"<td style='text-align: center;'>{row['Date']}</td>"
        table_html += "<td style='text-align: center;'>"
        
        for num in row['Winning Numbers'][:-1]:  # Main numbers
            table_html += f"<span style='padding: 5px; display: inline-block; margin-right: 3px;'>{num}</span>"
        
        # Set the bonus ball color based on the selected game
        bonus_ball_color = "red" if lottery_game == "Powerball" else "yellow"

        # Bonus ball with the appropriate color
        table_html += f"<span style='padding: 5px; display: inline-block; margin-right: 3px; color: {bonus_ball_color};'>{row['Winning Numbers'][-1]}</span>"
        
        table_html += "</td></tr>"
    
    table_html += "</table><br><br>"
    return table_html

# Set default numbers
default_numbers = [9, 36, 41, 44, 59]
default_bonus_number = 4

# Create input sliders for user to enter numbers
number_inputs = []

# Create columns
cols = st.sidebar.columns(3)

# Place sliders in columns
for i, default_num in enumerate(default_numbers, start=1):
    col = cols[(i - 1) % 3]
    number_inputs.append(col.slider(f"Enter number {i}", min_value=1, max_value=69, value=default_num, step=1))

# Place bonus number slider in the last column
bonus_number = cols[2].slider("Enter bonus number", min_value=1, max_value=26, value=default_bonus_number, step=1)

# Choose the game: Powerball or Mega Millions
lottery_game = st.sidebar.selectbox("Choose the game", options=["Powerball", "Mega Millions"])

# Set the bonus ball color based on the selected game
bonus_ball_color = "red" if lottery_game == "Powerball" else "yellow"

def display_lottery_numbers(numbers, bonus_ball_color):
    html_code = f"""
    <style>
        .ball {{
            width: 50px;
            height: 50px;
            line-height: 50px;
            text-align: center;
            border-radius: 50%;
            display: inline-block;
            margin: 5px;
        }}
        .white-ball {{
            background-color: white;
            color: black;
            border: 1px solid black;
        }}
        .yellow-ball {{
            background-color: yellow;
            color: black;
            border: 1px solid black;
        }}
        .red-ball {{
            background-color: red;
            color: black;
            border: 1px solid black;
        }}
    </style>
    <div class="ball white-ball">{numbers[0]}</div>
    <div class="ball white-ball">{numbers[1]}</div>
    <div class="ball white-ball">{numbers[2]}</div>
    <div class="ball white-ball">{numbers[3]}</div>
    <div class="ball white-ball">{numbers[4]}</div>
    <div class="ball {bonus_ball_color}-ball">{numbers[5]}</div>
    """
    return html_code

# Display the lottery numbers in the sidebar
st.sidebar.markdown(display_lottery_numbers(number_inputs + [bonus_number], bonus_ball_color) + "<br><br><br>", unsafe_allow_html=True)

# Add three carriage returns at the bottom of the sidebar
st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)

# Get the winning numbers and dates based on the user's selection
if lottery_game == "Powerball":
    winning_numbers, drawing_dates = get_powerball_data()
else:
    winning_numbers, drawing_dates = get_megamillions_data()
   
# Create a DataFrame with the winning numbers and dates
winning_df = pd.DataFrame({'Date': drawing_dates, 'Winning Numbers': winning_numbers})

# Display the winning numbers in an HTML table
st.write(f"The winning {lottery_game} numbers are:")
st.markdown(create_html_table(winning_df, lottery_game), unsafe_allow_html=True)

title = "<h3 style='text-align: left; font-family: Arial, sans-serif; color: Black;'>You Picked the Magic Numbers</h1>"
st.markdown(title, unsafe_allow_html=True)

# Display user's selected numbers with CSS
st.write(display_lottery_numbers(number_inputs + [bonus_number], bonus_ball_color), unsafe_allow_html=True)

# Define user_numbers
user_numbers = number_inputs

def calculate_prize(lottery_game, matched_numbers, matched_bonus):
    if lottery_game == "Powerball":
        prize_structure = {
            (5, True): "Jackpot",
            (5, False): "$1,000,000",
            (4, True): "$50,000",
            (4, False): "$100",
            (3, True): "$100",
            (3, False): "$7",
            (2, True): "$7",
            (1, True): "$4",
            (0, True): "$4"
        }
    else:  # Mega Millions
        prize_structure = {
            (5, True): "Jackpot",
            (5, False): "$1,000,000",
            (4, True): "$10,000",
            (4, False): "$500",
            (3, True): "$200",
            (3, False): "$10",
            (2, True): "$10",
            (1, True): "$4",
            (0, True): "$2"
        }
    return prize_structure.get((matched_numbers, matched_bonus), "No prize")

winning_dates = []
for i, numbers in enumerate(winning_numbers):
    # Check if the user matched the winning numbers
    matches = set(user_numbers).intersection(numbers[:-1])  # Exclude the last number (bonus)
    matched_bonus = bonus_number == numbers[-1]  # Check if the bonus number matches

    # If the user has matched any numbers or the bonus number, add the drawing date to the winning_dates list
    if len(matches) > 0 or matched_bonus:
        prize = calculate_prize(lottery_game, len(matches), matched_bonus)
        winning_dates.append((drawing_dates[i], prize))

if len(winning_dates) == 0:
    st.write("No winners.")
else:
    st.write(f"You got at least one number on the following {lottery_game} drawing dates:")
    for date, prize in winning_dates:
        st.write(f"{date}: {prize}")


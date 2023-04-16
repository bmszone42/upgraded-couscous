import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

title = "<h2 style='text-align: center; font-family: Arial, sans-serif; color: blue;'>PowerBall & Mega Millions Checker -- Let's Check Our Numbers</h1>"
st.markdown(title, unsafe_allow_html=True)

def get_megamillions_data():
    url = "https://www.lotteryusa.com/mega-millions/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.select('.c-result-card')
    
    winning_numbers = []
    drawing_dates = []

    for row in rows:
        date = row.select_one('.c-result-card__title').text.strip()
        #numbers = [int(n.text) for n in row.select(' .c-ball__label')]
        #numbers = [int(n.text) for n in row.select('.c-ball .c-result__item .c-ball--default .c-ball__label')]
        numbers = [int(n.text) for n in row.select('.c-ball.c-result__item.c-ball--default .c-ball__label')]
        st.write(numbers)
        megaball = [int(n.text) for n in row.select('.c-result__item.c-result__bonus-ball .c-ball.c-ball--yellow')]
        st.write(megaball)
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

def create_html_table(dataframe):
    table_html = '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">'
    table_html += "<tr><th>Date</th><th>Winning Numbers</th></tr>"
    
    for index, row in dataframe.iterrows():
        table_html += "<tr>"
        table_html += f"<td style='text-align: center;'>{row['Date']}</td>"
        table_html += "<td style='text-align: center;'>"
        
        for num in row['Winning Numbers'][:-1]:  # Main numbers
            table_html += f"<span style='padding: 5px; display: inline-block; margin-right: 3px;'>{num}</span>"
        
        # Powerball number in red
        table_html += f"<span style='padding: 5px; display: inline-block; margin-right: 3px; color: red;'>{row['Winning Numbers'][-1]}</span>"
        
        table_html += "</td></tr>"
    
    table_html += "</table><br><br>"
    return table_html

# Set default numbers
default_numbers = [9, 36, 41, 44, 59]
default_bonus_number = 4

# Create inputs for user to enter numbers
number1 = st.sidebar.number_input("Enter first number", min_value=1, max_value=69, value=default_numbers[0])
number2 = st.sidebar.number_input("Enter second number", min_value=1, max_value=69, value=default_numbers[1])
number3 = st.sidebar.number_input("Enter third number", min_value=1, max_value=69, value=default_numbers[2])
number4 = st.sidebar.number_input("Enter fourth number", min_value=1, max_value=69, value=default_numbers[3])
number5 = st.sidebar.number_input("Enter fifth number", min_value=1, max_value=69, value=default_numbers[4])
bonus_number = st.sidebar.number_input("Enter bonus number", min_value=1, max_value=26, value=default_bonus_number)

# Selector for Powerball or Mega Millions
lottery_game = st.sidebar.selectbox("Select the lottery game", ["Powerball", "Mega Millions"])

# Get the winning numbers and dates based on the user's selection
if lottery_game == "Powerball":
    winning_numbers, drawing_dates = get_powerball_data()
else:
    winning_numbers, drawing_dates = get_megamillions_data()
   
st.write("Length of drawing_dates:", len(drawing_dates))
st.write("Length of winning_numbers:", len(winning_numbers))

# Create a DataFrame with the winning numbers and dates
winning_df = pd.DataFrame({'Date': drawing_dates, 'Winning Numbers': winning_numbers})

# Display the winning numbers in an HTML table
st.write(f"The winning {lottery_game} numbers are:")
st.markdown(create_html_table(winning_df), unsafe_allow_html=True)

# Define user_numbers
user_numbers = [number1, number2, number3, number4, number5]
# Display results
entered_numbers = f"You entered the numbers <strong>{number1}</strong>, <strong>{number2}</strong>, <strong>{number3}</strong>, <strong>{number4}</strong>, <strong>{number5}</strong>, and <span style='color: red;'><strong>{bonus_number}</strong></span>"
st.markdown(entered_numbers, unsafe_allow_html=True)

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


import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime

def get_powerball_data(start_date, end_date):
    url = f"https://www.powerball.com/api/v1/numbers/powerball?_format=json&min=1&max=5&startDate={start_date}&endDate={end_date}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find_all("div", class_="winning-numbers")

    results = []
    for draw in data:
        numbers = [int(n.text) for n in draw.find_all("span", class_="ball")]
        powerball = int(draw.find("span", class_="powerball").text)
        results.append({"winning_numbers": set(numbers), "bonus_number": powerball})
    return results

def get_mega_millions_data(start_date, end_date):
    url = f"https://www.megamillions.com/api/v1/numbers/megamillions?_format=json&min=1&max=5&startDate={start_date}&endDate={end_date}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find_all("div", class_="winning-numbers")

    results = []
    for draw in data:
        numbers = [int(n.text) for n in draw.find_all("span", class_="ball")]
        mega_ball = int(draw.find("span", class_="mega-ball").text)
        results.append({"winning_numbers": set(numbers), "bonus_number": mega_ball})
    return results

def check_winning_numbers(lottery_data, user_numbers, bonus_number):
    for draw in lottery_data:
        winning_numbers = draw["winning_numbers"]
        draw_bonus_number = draw["bonus_number"]
        
        if winning_numbers == user_numbers and draw_bonus_number == bonus_number:
            return True
    return False

st.title("Lottery Number Checker")
st.subheader("Check your Powerball and Mega Millions numbers")

lottery_type = st.selectbox("Select Lottery Type", ["Powerball", "Mega Millions"])

st.write("Enter your numbers (comma separated):")
default_powerball_numbers = "18, 29, 35, 44, 60"
default_mega_millions_numbers = "8, 33, 38, 50, 53"

if lottery_type == "Powerball":
    user_numbers_input = st.text_input("", value=default_powerball_numbers, label_visibility='collapsed')
else:
    user_numbers_input = st.text_input("", value=default_mega_millions_numbers, label_visibility='collapsed')
user_numbers = set(map(int, user_numbers_input.split(",")))

if lottery_type == "Powerball":
    bonus_number = st.number_input("Enter your Powerball bonus number:", value=26, min_value=1, max_value=50)
else:
    bonus_number = st.number_input("Enter your Mega Millions bonus number:", value=25, min_value=1, max_value=50)

start_date = st.date_input("Select start date:")
end_date = st.date_input("Select end date:")

if st.button("Check Numbers"):
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    if lottery_type == "Powerball":
        lottery_data = get_powerball_data(start_date_str, end_date_str)
    else:
        lottery_data = get_mega_millions_data(start_date_str, end_date_str)

    won = check_winning_numbers(lottery_data, user_numbers, bonus_number)

    if won:
        st.success("Congratulations! You won!")
    else:
        st.warning("Sorry, you did not win.")

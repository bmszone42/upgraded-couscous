import streamlit as st
import requests
import datetime
import json

def get_powerball_data(start_date, end_date):
    url = f"https://api.powerball.net/v1/results?start={start_date}&end={end_date}"
    response = requests.get(url)
    return response.json()

def get_mega_millions_data(start_date, end_date):
    url = f"https://api.megamillions.net/v1/results?start={start_date}&end={end_date}"
    response = requests.get(url)
    return response.json()

def check_winning_numbers(lottery_data, user_numbers, bonus_number):
    for draw in lottery_data:
        winning_numbers = set(draw["winning_numbers"].split(","))
        draw_bonus_number = draw["bonus_number"]
        
        if winning_numbers == user_numbers and draw_bonus_number == bonus_number:
            return True
    return False

st.title("Lottery Number Checker")
st.subheader("Check your Powerball and Mega Millions numbers")

lottery_type = st.selectbox("Select Lottery Type", ["Powerball", "Mega Millions"])
st.write("Enter your numbers (comma separated):")
user_numbers = set(map(int, st.text_input("").split(",")))
bonus_number = st.number_input("Enter your bonus number:", min_value=1, max_value=50)

start_date = st.date_input("Select start date:")
end_date = st.date_input("Select end date:")

if st.button("Check Numbers"):
    if lottery_type == "Powerball":
        lottery_data = get_powerball_data(start_date, end_date)
    else:
        lottery_data = get_mega_millions_data(start_date, end_date)

    won = check_winning_numbers(lottery_data, user_numbers, bonus_number)

    if won:
        st.success("Congratulations! You won!")
    else:
        st.warning("Sorry, you did not win.")

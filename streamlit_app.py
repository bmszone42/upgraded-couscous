import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from requests_html import HTMLSession

import requests
from bs4 import BeautifulSoup
import datetime


import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from requests_html import HTMLSession

import requests
from bs4 import BeautifulSoup
import datetime


# Scrape Powerball data from official website for the last 50 draws
def get_powerball_data():
    url = "https://www.powerball.com/previous-results"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.select(".result-item")[:50]
    results = []

    for draw in data:
        draw_date = draw.select_one(".result-heading").text.strip()
        draw_date = datetime.datetime.strptime(draw_date, "%m/%d/%Y").strftime("%Y-%m-%d")

        numbers = [int(num.text) for num in draw.select(".result-ball")]
        powerball = int(draw.select_one(".result-powerball").text)

        results.append({"date": draw_date, "winning_numbers": set(numbers), "bonus_number": powerball})

    return results


# Scrape Mega Millions data from official website for the last 50 draws
def get_mega_millions_data():
    url = "https://www.megamillions.com/Winning-Numbers/Previous-Drawings.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.select(".row.pb-4.pt-4.border-bottom.border-secondary")[:50]
    results = []

    for draw in data:
        draw_date = draw.select_one(".col-sm-6.col-lg-4.pb-2.pb-md-0").text.strip()
        draw_date = datetime.datetime.strptime(draw_date, "%m/%d/%Y").strftime("%Y-%m-%d")

        numbers_list = draw.select_one(".list-unstyled.winning_numbers")
        numbers = [int(num.text) for num in numbers_list.select(".ball")] + \
                  [int(num.text) for num in numbers_list.select(".ball.gold")]
        mega_ball = int(draw.select_one(".ball.megaball").text)

        results.append({"date": draw_date, "winning_numbers": set(numbers), "bonus_number": mega_ball})

    return results


def get_winning_combination(lottery_data, user_numbers, bonus_number):
    for draw in lottery_data:
        winning_numbers = draw["winning_numbers"]
        draw_bonus_number = draw["bonus_number"]

        matched_numbers = winning_numbers.intersection(user_numbers)
        matched_count = len(matched_numbers)
        bonus_matched = bonus_number == draw_bonus_number

        if matched_count == 5 and bonus_matched:
            return "Jackpot"
        elif matched_count == 5:
            return "Match 5"
        elif matched_count == 4 and bonus_matched:
            return "Match 4 + Bonus"
        elif matched_count == 4:
            return "Match 4"
        elif matched_count == 3 and bonus_matched:
            return "Match 3 + Bonus"
        elif matched_count == 3:
            return "Match 3"
        elif matched_count == 2 and bonus_matched:
            return "Match 2 + Bonus"
        elif matched_count == 1 and bonus_matched:
            return "Match 1 + Bonus"
        elif bonus_matched:
            return "Bonus Only"
    return "No Win"


def app():
    st.set_page_config(page_title="Lottery Number Checker", page_icon=":money_with_wings:")

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

    if st.button("Check Numbers"):
        if lottery_type == "Powerball":
            lottery_data = get_powerball_data()
        else:
            lottery_data = get_mega_millions_data()

        winning_combination = get_winning_combination(lottery_data, user_numbers, bonus_number)

        if winning_combination != "No Win":
            st.success(f"Congratulations! You got a {winning_combination}!")
        else:
            st.warning("Sorry, you did not win.")

        st.subheader("Numbers drawn for the latest drawing:")

        latest_draw = lottery_data[0]

        data = {
            "Date": [latest_draw["date"]],
            "Numbers Drawn": [", ".join(str(num) for num in sorted(latest_draw["winning_numbers"]))],
            "Bonus Number": [latest_draw["bonus_number"]],
        }
        df = pd.DataFrame(data)
        st.write(df)
        
    st.subheader("Disclaimer")
    st.write("This tool is for informational purposes only. While we strive to ensure the accuracy of the information provided, we make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or availability with respect to the website or the information, products, services, or related graphics contained on the website for any purpose. Any reliance you place on such information is therefore strictly at your own risk.")    
 
if __name__ == "__main__":
    app()

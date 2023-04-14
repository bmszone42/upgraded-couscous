import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from requests_html import HTMLSession


def get_powerball_data(start_date, end_date):
    base_url = 'https://www.powerball.com'
    url = f'{base_url}/draw-games/powerball'
    headers = {'user-agent': 'Mozilla/5.0'}
    with requests.Session() as session:
        session.headers.update(headers)
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extracting data for the provided date range
        datepicker_input = soup.find('input', {'id': 'datepicker-input'})
        datepicker_input['value'] = start_date
        datepicker_input2 = soup.find('input', {'id': 'datepicker-input2'})
        datepicker_input2['value'] = end_date
        search_btn = soup.find('button', {'id': 'submit-date'})
        response = session.post(base_url + search_btn['formaction'], data=search_btn.form)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select('tr')
        results = []

        for draw in data:
            draw_date = draw.select_one(".date-value").text.strip()
            draw_date = datetime.datetime.strptime(draw_date, "%m/%d/%Y").strftime("%Y-%m-%d")

            if start_date <= draw_date <= end_date:
                numbers = [int(num.text) for num in draw.select(".white-ball")]
                powerball = int(draw.select_one(".red-ball").text)

                results.append({"date": draw_date, "winning_numbers": set(numbers), "bonus_number": powerball})

    return results


def get_mega_millions_data(start_date, end_date):
    base_url = 'https://www.megamillions.com'
    url = f'{base_url}/Winning-Numbers/Previous-Drawings.aspx'
    headers = {'user-agent': 'Mozilla/5.0'}
    with requests.Session() as session:
        session.headers.update(headers)
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extracting data for the provided date range
        datepicker_input = soup.find('input', {'id': 'from-date'})
        datepicker_input['value'] = start_date
        datepicker_input2 = soup.find('input', {'id': 'to-date'})
        datepicker_input2['value'] = end_date
        search_btn = soup.find('button', {'id': 'btnSearch'})
        response = session.post(base_url + search_btn['formaction'], data=search_btn.form)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select('.past-draw-body .table-row')
        results = []

        for draw in data:
            draw_date = draw.select_one(".date").text.strip()
            draw_date = datetime.datetime.strptime(draw_date, "%A, %B %d, %Y").strftime("%Y-%m-%d")

            if start_date <= draw_date <= end_date:
                numbers_list = draw.select_one(".numbers .table-row").select(".number")
                numbers = [int(num.text) for num in numbers_list]
                mega_ball = int(draw.select_one(".mega-ball").text)

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

    winning_combination = get_winning_combination(lottery_data, user_numbers, bonus_number)

    if winning_combination != "No Win":
        st.success(f"Congratulations! You got a {winning_combination}!")
    else:
        st.warning("Sorry, you did not win.")
        
    st.subheader("Numbers drawn for the queried date range:")
        
    data = {
        "Date": [draw["date"] for draw in lottery_data],
        "Numbers Drawn": [", ".join(str(num) for num in sorted(draw["winning_numbers"])) for draw in lottery_data],
        "Bonus Number": [draw["bonus_number"] for draw in lottery_data],
    }
    df = pd.DataFrame(data)
    st.write(df)

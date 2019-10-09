from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
import requests
import re
import time
import os


# number of arzigogoli by weeks
def weeks_from_first():
    f_date = date(2019, 9, 30)
    l_date = date.today()
    delta = l_date - f_date
    return int(delta.days / 7) + 1


# number of arzigogoli by website count
def scraper():
    page = requests.get("https://weblab.ing.unimore.it/people/andreoli/didattica/sistemi-operativi/index.html").text
    soup = BeautifulSoup(page, "html.parser")
    array = []
    for title in soup.find_all('h4'):
        x = re.search(r"Arzigogolo [0-9]+", title.text)
        if x is not None:
            array.append(x)
    return len(array)  # number of Arzigogoli


# send and pin message Telegram
def send_telegram(num_arz):
    bot_token = os.environ["TG_TOKEN"]
    unimore_group = os.environ["UNIMORE_GROUP_ID"]
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + \
                unimore_group + '&parse_mode=Markdown&text=' + "Arzigogolo " + str(num_arz) + \
                " uscito: " \
                "https://weblab.ing.unimore.it/people/andreolini/didattica/sistemi-operativi/2019-20/arzigogolo-" + \
                str(num_arz) + "/A" + str(num_arz) + "-testo.pdf"
    message_id = requests.get(send_text)
    pin_message = 'https://api.telegram.org/bot' + bot_token + '/pinChatMessage?chat_id=' + \
                  unimore_group + '&message_id=' + \
                  str(message_id.json()["result"]["message_id"])
    requests.get(pin_message)


def main():
    while True:
        arz_by_week = weeks_from_first()
        arz_by_website = scraper()

        print("Arzigogolo settimana: " + str(arz_by_week))
        print("Arzigogoli sul sito attualmente: " + str(arz_by_website))

        if arz_by_week == arz_by_website:
            send_telegram(arz_by_website)

            # days to next week
            days_to_sunday = 6 - date.today().weekday()

            # difference hours
            diff_hours = abs(datetime.now().replace(microsecond=0) -
                             datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

            # sleep to monday 8:00
            time.sleep(days_to_sunday * 86400 + (115200 - diff_hours))  # days_to_sunday + (24h - current time + 8h)
        else:
            print("sleep for 15 minutes")
            time.sleep(900)


if __name__ == "__main__":
    main()

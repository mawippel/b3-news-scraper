import schedule
import time
import scraper_exame
import scraper_google_finance
import scraper_info_money


def scrap():
    scraper_exame.scrap()
    scraper_google_finance.scrap()
    scraper_info_money.scrap()


schedule.every(15).minutes.do(scrap)

while True:
    schedule.run_pending()
    time.sleep(1)

import schedule
import time
import scraper_exame
import scraper_suno
import scraper_info_money

first_time = True

def scrap():
    scraper_exame.scrap()
    scraper_suno.scrap()
    scraper_info_money.scrap()


schedule.every(30).minutes.do(scrap)

while True:
    if first_time:
        scrap()
        first_time = False
    schedule.run_pending()
    time.sleep(1)

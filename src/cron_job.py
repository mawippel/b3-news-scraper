import schedule
import time
import scraper_exame
import scraper_suno
import scraper_info_money


def main():
    schedule.every(30).minutes.do(scrap)
    first_time = True
    while True:
        if first_time:
            scrap()
            first_time = False
        schedule.run_pending()
        time.sleep(1)


def scrap():
    scraper_exame.scrap()
    scraper_suno.scrap()
    scraper_info_money.scrap()


if __name__ == "__main__":
    main()

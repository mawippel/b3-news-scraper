import datetime


class LogUtils:
    @staticmethod
    def start(website_name):
        print('[{}] Starting {} scraper...'.format(
            datetime.datetime.now().isoformat(), website_name))

    @staticmethod
    def end(website_name, saved_news):
        print('[{}] Ending {} scraper... {} news were saved. {}'.format(
            datetime.datetime.now().isoformat(), website_name, len(saved_news), saved_news))

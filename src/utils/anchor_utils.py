class AnchorUtils:

    @staticmethod
    def is_valid(href):
        return href and href[:1] != '/'

    @staticmethod
    def is_not_fetched(href, fetched_links):
        return href not in fetched_links

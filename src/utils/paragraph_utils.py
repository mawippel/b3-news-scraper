class ParagraphUtils:

    @staticmethod
    def split(text):
        texts = text.split('.')
        return [x for x in texts if x]

    @staticmethod
    def sanitize(paragraph):
        paragraph = paragraph.replace(u'\xa0', u' ')
        paragraph = paragraph.replace('"', '')
        paragraph = paragraph.strip()
        return paragraph

    @staticmethod
    def is_valid(text):
        return ParagraphUtils.is_not_tag(text) and ParagraphUtils.is_not_script_tag(text) and not ParagraphUtils.is_useless_paragraph(text)

    @staticmethod
    def is_not_script_tag(text):
        return text and "<script>" not in text

    @staticmethod
    def is_useless_paragraph(paragraph):
        return paragraph.strip() == '' or paragraph.lower() == 'adiciona categoria materia'

    @staticmethod
    def is_not_tag(text):
        return text and text[:1] != '<'

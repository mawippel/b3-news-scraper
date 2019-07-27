import os
import requests
import yaml

# Load the config file into memory
config = yaml.safe_load(open("config.yml"))


def analyze(text):
    payload = {'key': config['API_KEY'], 'lang': 'pt',
               'txt': text}
    r = requests.post(
        "https://api.meaningcloud.com/sentiment-2.1", data=payload)
    print(r.text)


if __name__ == "__main__":
    analyze(
        'Neste ano, supomos que tenhamos uma melhora na economia, porém, não temos total certeza')

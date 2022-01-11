import config, requests

r = requests.get(config.BARS_URL, headers= config.Headers)

print(r.content)
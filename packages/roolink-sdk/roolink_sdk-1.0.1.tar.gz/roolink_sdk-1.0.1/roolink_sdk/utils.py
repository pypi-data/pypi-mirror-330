import re


bazadebezolkohpepadr_pattern = re.compile(r'bazadebezolkohpepadr="([^"]+)"')
script_url_pattern = re.compile(r'<script type="text/javascript"\s+(?:nonce=".*?")?\s+src="([a-z\d/\-_]+)"></script>', re.IGNORECASE)

def get_bazadebezolkohpepadr(html):
	match = re.search(bazadebezolkohpepadr_pattern, html)
	if not match:
		raise Exception("Failed to parse bazadebezolkohpepadr")
	return match.group(1)


def parse_script_url(html):
	match = re.search(script_url_pattern, html)
	if not match:
		raise Exception("Failed to parse script url")
	return match.group(1)
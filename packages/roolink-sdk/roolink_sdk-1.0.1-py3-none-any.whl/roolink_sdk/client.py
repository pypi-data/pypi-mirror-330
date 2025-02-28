import requests
import json

class RooLink:
	"""
	RooLink SDK for interacting with the RooLink API.

	This SDK provides methods for fetching usage limits, parsing scripts, generating sensor data, and more.
	"""

	BASE_URL = "https://www.roolink.io/api/v1"

	def __init__(self, api_key, protected_url, user_agent):
		"""
		Initialize the RooLink SDK.

		:param api_key: Your RooLink API key.
		:param protected_url: The URL you want to protect.
		:param user_agent: The User-Agent string for your session. Most recent version of Chrome on Windows.
		"""
		self.api_key = api_key
		self.protected_url = protected_url
		self.user_agent = user_agent
		self.client = requests.Session()

	def request_limit(self) -> dict:
		"""
		Fetch the API request limit for your key.

		:return: A dictionary containing the current request limit information.
		"""
		url = f"{self.BASE_URL}/limit?key={self.api_key}"
		return self._request("GET", url)

	def parse_script_data(self, script_body) -> dict:
		"""
		Parse script data to extract relevant information. Used for generating sensor data 3.0.

		:param script_body: The script content as plain text.
		:return: Parsed script data as a dictionary.
		"""
		headers = self._default_headers(content_type="text/plain")
		url = f"{self.BASE_URL}/parse"
		return self._request("POST", url, headers=headers, data=script_body)

	def generate_sensor_data(self, abck, bm_sz, script_data=None, sec_cpt=False, stepper=False, index=2, flags="", keyboard=False) -> str:
		"""
		Generate sensor data.

		:param abck: The "_abck" cookie response can be found either in the response from the GET request to the script endpoint or in the response from the most recent POST request to the script endpoint.
		:param bm_sz: The response containing the "bm_sz" cookie can be obtained from the initial GET request made to the script endpoint.
		:param script_data: (Optional - required for sensor data 3.0) used for generating sensor data 3.0.
		:param sec_cpt: (Optional) Enable sec_cpt mode.
		:param stepper: (Optional) Enable stepper mode. Use this only if you are having issues generating a valid cookie
		:param index: (Optional - required if using stepper mode) Index parameter for generation. Works with Stepper mode to get a specific sensor index.
		:param flags: (Optional) Additional flags as a string.
		:param keyboard: (Optional) Enables Keyboard events
		:return: Generated sensor data as a JSON string.
		"""
		headers = self._default_headers()
		payload = {
			"url": self.protected_url,
			"userAgent": self.user_agent,
			"_abck": abck,
			"bm_sz": bm_sz,
			"sec_cpt": sec_cpt,
			"stepper": stepper,
			"index": index,
			"flags": flags,
			"keyboard": keyboard
		}
		if script_data:
			payload["scriptData"] = script_data

		url = f"{self.BASE_URL}/sensor"
		response = self._request("POST", url, headers=headers, json=payload)
		return json.dumps({"sensor_data": response.get("sensor")})

	def generate_sbsd_body(self, url, vid, cookie) -> dict:
		"""
		Generate the SBSD body.

		:param url: Url of the original page you were trying to get (the referrer)
		:param vid: The vid parameter.
		:param cookie: The bm_o, sbsd_o, or bm_so cookie value.
		:return: Generated SBSD body as a dictionary.
		"""
		headers = self._default_headers()
		payload = {
			"url": url,
			"userAgent": self.user_agent,
			"vid": vid,
			"bm_o": cookie
		}
		url = f"{self.BASE_URL}/sbsd"
		return self._request("POST", url, headers=headers, json=payload)

	def generate_pixel_data(self, bazadebezolkohpepadr, hash_value) -> str:
		"""
		Generate pixel data.

		:param bazadebezolkohpepadr: the "window.Bazadebezolkohpepadr" value from the html
		:param hash_value: the "u" value from the pixel post data
		:return: Generated pixel data as a string.
		"""
		headers = self._default_headers()
		payload = {
			"userAgent": self.user_agent,
			"bazadebezolkohpepadr": int(bazadebezolkohpepadr),
			"hash": hash_value
		}
		url = f"{self.BASE_URL}/pixel"
		response = self._request("POST", url, headers=headers, json=payload)
		return response.get("sensor")

	def generate_sec_cpt_answers(self, token, timestamp, nonce, difficulty, cookie) -> dict:
		"""
		Generate sec-cpt answers for challenge resolution. All parameters will be provided by the challenge response.

		:param token: Security token.
		:param timestamp: Timestamp of the request.
		:param nonce: Nonce value.
		:param difficulty: Challenge difficulty level.
		:param cookie: Associated cookie.
		:return: Generated sec-cpt answers as a dictionary.
		"""
		headers = self._default_headers()
		payload = {
			"token": token,
			"timestamp": timestamp,
			"nonce": nonce,
			"difficulty": difficulty,
			"cookie": cookie
		}
		url = f"{self.BASE_URL}/sec-cpt"
		return self._request("POST", url, headers=headers, json=payload)

	def _default_headers(self, content_type="application/json"):
		"""
		Generate default headers for API requests.

		:param content_type: Content-Type header value.
		:return: Dictionary of default headers.
		"""
		return {
			"x-api-key": self.api_key,
			"content-type": content_type
		}

	def _request(self, method, url, headers=None, data=None, json=None):
		"""
		Internal method to handle HTTP requests.

		:param method: HTTP method (GET, POST, etc.).
		:param url: URL for the request.
		:param headers: Request headers.
		:param data: Raw data to send in the request body.
		:param json: JSON payload to send in the request body.
		:return: Parsed JSON response from the API.
		"""
		response = self.client.request(method, url, headers=headers, data=data, json=json)
		
		if not response.ok:
			raise Exception(f"Error {response.status_code}: {response.text}")

		try:
			return response.json()
		except json.JSONDecodeError:
			raise Exception("Invalid JSON response from server")

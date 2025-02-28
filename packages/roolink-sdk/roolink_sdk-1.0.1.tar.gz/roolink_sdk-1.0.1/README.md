# RooLink SDK

RooLink SDK is a Python library designed for seamless interaction with the RooLink API. It provides utilities for API request limits, parsing scripts, generating sensor data, and more.

## Features

- Fetch API request limits
- Parse script data
- Generate sensor data for validation
- Create SBSD body
- Generate pixel data
- Solve sec-cpt challenges

## Usage

Install the SDK via pip:

```bash
pip install roolink-sdk
```
Quick Start
Here's how to use the SDK in your Python project:

### Import the SDK and Initialize
```python
from roolink_sdk.client import RooLink
from roolink_sdk.utils import get_bazadebezolkohpepadr, parse_script_url

# Initialize the RooLink SDK
api_key = "your_api_key"
protected_url = "https://example.com"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

session = RooLink(api_key, protected_url, user_agent)
```
### Fetch API Request Limit
```python
limit = session.request_limit()
print("Request Limit:", limit)
```
### Parse Script Data
```python
script_body = "function example() { return 'sample'; }"
parsed_data = session.parse_script_data(script_body)
print("Parsed Data:", parsed_data)
```
### Generate Sensor Data
```python
abck = "sample_abck"
bm_sz = "sample_bm_sz"
sensor_data = session.generate_sensor_data(abck, bm_sz)
print("Sensor Data:", sensor_data)
```
### Generate SBSD Body
```python
url = "https://example.com/"
vid = "sample_vid"
cookie = "sample_cookie"
sbsd_body = session.generate_sbsd_body(url, vid, cookie)
print("SBSD Body:", sbsd_body)
```
### Generate Pixel Data
```python
bazadebezolkohpepadr = 12345
hash_value = "sample_hash"
pixel_data = session.generate_pixel_data(bazadebezolkohpepadr, hash_value)
print("Pixel Data:", pixel_data)
```
### Solve sec-cpt Challenges
```python
token = "sample_token"
timestamp = 1234567890
nonce = "sample_nonce"
difficulty = 3
cookie = "sample_cookie"
sec_cpt_answers = session.generate_sec_cpt_answers(token, timestamp, nonce, difficulty, cookie)
print("Sec-CPT Answers:", sec_cpt_answers)
```

## License
```markdown
This project is licensed under the MIT License. See the LICENSE file for details.
```

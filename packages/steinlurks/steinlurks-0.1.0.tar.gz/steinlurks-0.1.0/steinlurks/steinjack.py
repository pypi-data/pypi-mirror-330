import Topython
import random
import requests
import json
import uuid
import hashlib
from fake_useragent import UserAgent
from fake_useragent import UserAgent
import threading
import sys
import time
import pycountry
from secrets import token_hex
from ms4 import InfoIG, RestInsta
import os
import string
from queue import Queue


def check_email(email):
	if email.endswith('@aol.com'):return Topython.Email.aol(email)
	elif email.endswith('@gmail.com'):return Topython.Email.gmail(email)
	else:return False
    

class Variable:
    country = [country.numeric for country in pycountry.countries]
    num = random.choice(country)
    sgin = hashlib.sha256(uuid.uuid4().hex.encode()).hexdigest()
    csr = str(token_hex(8) * 2)
    android = f"android-{uuid.uuid4().hex[:16]}"
variable_instance = Variable()

def generate_user_agent():
    """Generate a random user agent string."""
    ii = ["165.1.0.29.119", "166.0.0.30.120", "167.0.0.31.121", "168.0.0.32.122"]
    aa = {
        "28/9": ["720dpi", "1080dpi", "1440dpi"],
        "29/10": ["720dpi", "1080dpi", "1440dpi", "2160dpi"],
        "30/11": ["1080dpi", "1440dpi", "2160dpi"],
        "31/12": ["1440dpi", "2160dpi"]
    }
    ss = {
        "720dpi": ["1280x720", "1920x1080"],
        "1080dpi": ["1920x1080", "2560x1440", "3840x2160"],
        "1440dpi": ["2560x1440", "3840x2160"],
        "2160dpi": ["3840x2160", "7680x4320"]
    }
    dd = {
        "samsung": ["SM-T292", "SM-G973F", "SM-A515F"],
        "google": ["Pixel 4", "Pixel 5"],
        "huawei": ["P30 Pro", "Mate 40 Pro"],
        "xiaomi": ["Mi 10", "Redmi Note 10"],
        "oneplus": ["8T", "9 Pro"],
        "sony": ["XZ2", "Xperia 1"]
    }
    cc = ["qcom", "exynos", "kirin", "mediatek", "apple"]
    lan = ["en_US", "es_ES", "fr_FR", "de_DE", "zh_CN", "ja_JP", "ko_KR"]
    dp = ["phone", "tablet", "watch", "tv", "car"]
    arm = ["arm64_v8a", "armeabi-v7a", "x86", "x86_64"]
    comb = ["samsung", "google", "huawei", "xiaomi", "oneplus", "sony"]

    sos = random.choice(list(aa.keys()))
    vlo = random.choice(aa[sos])
    lop = random.choice(ss[vlo])
    ki = random.choice(comb)
    mo = random.choice(dd.get(ki, ["Unknown"]))

    user_agent = (
        f"Instagram {random.choice(ii)} Android "
        f"({sos}; {vlo}; {lop}; {ki}; {mo}; "
        f"{random.choice(arm)}; {random.choice(dp)}; "
        f"{random.choice(lan)}; {random.choice(cc)})"
    )

    return user_agent

def stein1(email):
    """Check if the email corresponds to a 'Good' password and return True or False."""
    
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.caa.ar.search.async/"
    
    # The payload to be sent with the request
    payload = f"params=%7B%22client_input_params%22%3A%7B%22text_input_id%22%3A%22616z6k%3A71%22%2C%22was_headers_prefill_available%22%3A0%2C%22sfdid%22%3A%22%22%2C%22fetched_email_token_list%22%3A%7B%7D%2C%22search_query%22%3A%22{email}%22%2C%22android_build_type%22%3A%22release%22%2C%22accounts_list%22%3A%5B%5D%2C%22ig_android_qe_device_id%22%3A%228745a4a2-a663-4bc7-9b3b-16d5b8ea20b9%22%2C%22ig_oauth_token%22%3A%5B%5D%2C%22is_whatsapp_installed%22%3A1%2C%22lois_settings%22%3A%7B%22lois_token%22%3A%22%22%2C%22lara_override%22%3A%22%22%7D%2C%22was_headers_prefill_used%22%3A0%2C%22headers_infra_flow_id%22%3A%22%22%2C%22fetched_email_list%22%3A%5B%5D%2C%22sso_accounts_auth_data%22%3A%5B%5D%2C%22encrypted_msisdn%22%3A%22%22%7D%2C%22server_params%22%3A%7B%22event_request_id%22%3A%22b8a5a2be-1abe-40da-b476-3d893c871e21%22%2C%22is_from_logged_out%22%3A0%2C%22layered_homepage_experiment_group%22%3Anull%2C%22device_id%22%3A%22android-bf1b282ab2b0b445%22%2C%22waterfall_id%22%3A%22017145b8-cb79-439a-9036-2fb580f40ca0%22%2C%22INTERNAL__latency_qpl_instance_id%22%3A3.6480220400074E13%2C%22is_platform_login%22%3A0%2C%22context_data%22%3A%22AR2rfU7knJNQCBz3hzsomH487qVyGu0HOVx3jgM-6G69fIwxA73vDmSlV7vY-W2aR4sv08iPPcsbdDt7RQF0ijGeqPudYXN0zlEZMvLeGOEvM_HHTtEJuv8dHDd4c8AIk4VpoaEASAIC9T_OS4yHwzupVtJKe7ghZ7k0y3kHeS7OGhaAIm4QvqfWW5JendkDb0mWJ31hcpuhEp8qcbdjJ27ABYmh7-MltY9OrlgAoBsSZuz8_MD3S1XQFV0I52liYk8fK_tSI9x4Ok0lTmIWJ4aN8pjQvxGhAWLJ73ONhBVfpIXE2xuutHN4eMrjKARC2-XcGRmg7pf3xLfGu_Z7zKiKrVmR8LQz91dwiKHFaND6DeHwVcARkBjYm0YLjaGdT-0FIeGYFs1x%7Carm%22%2C%22INTERNAL__latency_qpl_marker_id%22%3A36707139%2C%22family_device_id%22%3A%222586e714-fdb4-4741-ba7b-0b84b13e2a97%22%2C%22offline_experiment_group%22%3A%22caa_launch_ig4a_combined_60_percent%22%2C%22INTERNAL_INFRA_THEME%22%3A%22default%2Cdefault%22%2C%22access_flow_version%22%3A%22F2_FLOW%22%2C%22is_from_logged_in_switcher%22%3A0%2C%22qe_device_id%22%3A%228745a4a2-a663-4bc7-9b3b-16d5b8ea20b9%22%7D%7D&bk_client_context=%7B%22bloks_version%22%3A%228ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb%22%2C%22styles_id%22%3A%22instagram%22%7D&bloks_versioning_id=8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb"
    
    headers = {
        'User-Agent': generate_user_agent(),  # Randomly generated user agent
        'x-ig-app-locale': "en-US",
        'x-ig-device-locale': "en-US",
        'x-ig-mapped-locale': "en-US",
        'x-pigeon-session-id': "UFS-42175dfd-8675-4443-8f8d-7f09fa7ea9da-0",
        'x-pigeon-rawclienttime': "1725835735.847",
        'x-ig-bandwidth-speed-kbps': "-1.000",
        'x-ig-bandwidth-totalbytes-b': "0",
        'x-ig-bandwidth-totaltime-ms': "0",
        'x-bloks-version-id': "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb",
        'x-ig-www-claim': "0",
        'x-bloks-is-layout-rtl': "true",
        'x-ig-device-id': "8745a4a2-a663-4bc7-9b3b-16d5b8ea20b9",
        'x-ig-family-device-id': "2586e714-fdb4-4741-ba7b-0b84b13e2a97",
        'x-ig-android-id': "android-bf1b282ab2b0b445",
        'x-ig-timezone-offset': "10800",
        'x-fb-connection-type': "MOBILE.LTE",
        'x-ig-connection-type': "MOBILE(LTE)",
        'x-ig-capabilities': "3brTv10=",
        'x-ig-app-id': "567067343352427",
        'priority': "u=3",
        'accept-language': "en-US",
        'x-mid': "Zt4loQABAAFzGR1YLL2M9XOkL9El",
        'ig-intended-user-id': "0",
        'content-type': "application/x-www-form-urlencoded"
    }

    # Send the POST request
    response = requests.post(url, data=payload, headers=headers)

    # Check the response status
    if response.status_code == 200:
        response_data = response.json()  # Convert response to JSON

        # Check if the error message is in the response
        if "The password you entered is incorrect." in str(response_data):
            return True  # Password is incorrect
        else:
            return False  # Password isn't incorrect or other error
    else:
        return False  # Failed request
    
def stein2(email):
    """
    This function sends a POST request to check if the email exists and returns True if found.
    Otherwise, it returns False.
    
    Parameters:
    - email: The email to check.
    """
    
    url = "https://i.instagram.com/api/v1/users/lookup/"
    
    # Create the payload using variables from Variable class
    payload = f"signed_body={Variable.sgin}.%7B%22country_codes%22%3A%22%5B%7B%5C%22country_code%5C%22%3A%5C%22{Variable.num}%5C%22%2C%5C%22source%5C%22%3A%5B%5C%22default%5C%22%5D%7D%5D%22%2C%22_csrftoken%22%3A%22{Variable.csr}%22%2C%22q%22%3A%22{email}%22%2C%22guid%22%3A%22{uuid.uuid4()}%22%2C%22device_id%22%3A%22{Variable.android}%22%2C%22directly_sign_in%22%3A%22true%22%7D&ig_sig_key_version=4"
    
    # Define headers
    headers = {
        'User-Agent': generate_user_agent(),
        'Accept-Encoding': "gzip, deflate",
        'Content-Type': "application/x-www-form-urlencoded",
        'X-Pigeon-Session-Id': str(uuid.uuid4()),
        'X-Pigeon-Rawclienttime': str("{:.3f}".format(time.time())),
        'X-IG-Connection-Speed': "-1kbps",
        'X-IG-Bandwidth-Speed-KBPS': "-1.000",
        'X-IG-Bandwidth-TotalBytes-B': "0",
        'X-IG-Bandwidth-TotalTime-MS': "0",
        'X-Bloks-Version-Id': "009f03b18280bb343b0862d663f31ac80c5fb30dfae9e273e43c63f13a9f31c0",
        'X-IG-Connection-Type': "MOBILE(LTE)",
        'X-IG-Capabilities': "3brTvw==",
        'X-IG-App-ID': "567067343352427",
        'Accept-Language': "ar-YE, en-US",
        'X-FB-HTTP-Engine': "Liger",
    }
    
    # Send the POST request and get the response text
    res = requests.post(url, data=payload, headers=headers).text
    
    # Check if the response contains "status":"ok" and the email
    if '"status":"ok"' in res and f'{email}' in res:
        return True
    else:
        return False

def stein3(email):

    
    ua = generate_user_agent()
    device_id = 'android-' + hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16]
    uui = str(uuid.uuid4())

    # Define headers
    headers = {
        'User-Agent': ua,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    # Define cookies
    cookies = {
        'csrftoken': '76HKvZYXiWJKIArQAQNEMD'  # You might want to update this if necessary
    }

    # Define data for the POST request
    data = {
        'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.' + json.dumps({
            '_csrftoken': '76HKvZYXiWJKIArQAQNEMD',
            'adid': uui,
            'guid': uui,
            'device_id': device_id,
            'query': email
        }),
        'ig_sig_key_version': '4',
    }

    # Send the POST request
    response = requests.post(
        'https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/',
        headers=headers, cookies=cookies, data=data
    ).text

    # Check if the email is present in the response and return the result
    if email in response:
        return True
    else:
        return False

def stein4(email):
    # Generate a dynamic user agent using the generate_user_agent function
    ua = generate_user_agent()
    
    # Generate unique device and GUID
    device_id = f"android-{uuid.uuid4().hex[:16]}"
    guid = str(uuid.uuid4())
    
    # Set the headers using the generated user agent
    headers = {
        'Host': 'i.instagram.com',
        'X-IG-Capabilities': 'AQ==',
        'X-IG-Connection-Type': 'WIFI',
        'User-Agent': ua,
    }
    
    # Define cookies
    cookies = {
        'csrftoken': '76HKvZYXiWJKIArQAQNEMD'
    }
    
    # Prepare the POST data
    data = {
        'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.'
                       + json.dumps({
                            '_csrftoken': '76HKvZYXiWJKIArQAQNEMD',
                            'adid': guid,
                            'guid': guid,
                            'device_id': device_id,
                            'query': email
                        }),
        'ig_sig_key_version': '4',
    }

    
    # Send POST request to initiate the password recovery flow
    response = requests.post(
        'https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/',
        headers=headers, cookies=cookies, data=data
    ).text
    
    # Check if the email is in the response
    if email in response:
        return True  # Email found in response, successful request
    else:
        return False
    
def stein5(email):
    # Generate a dynamic user agent using the generate_user_agent function
    ua = generate_user_agent()

    # Generate unique device ID and GUID
    device_id = f"android-{uuid.uuid4().hex[:16]}"
    guid = str(uuid.uuid4())

    # Set the headers with additional information
    headers = {
        'Host': 'www.instagram.com',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/accounts/signup/email/',
        'user-agent': ua,  # Using dynamically generated user agent
        'x-ig-app-id': '567067343352427',
        'x-ig-connection-type': 'WIFI',
        'x-ig-csrf-token': '76HKvZYXiWJKIArQAQNEMD',
        'x-ig-capabilities': '3brTvw==',
        'x-ig-connection-speed': '-1kbps',
        'x-ig-batch-request': 'false',
        'x-fb-httpreferer': 'https://www.instagram.com/',
        'accept-language': 'en-US',
        'x-ig-batch-referer': 'https://www.instagram.com/accounts/signup/email/',
        'accept-encoding': 'gzip, deflate'
    }

    # Prepare the POST data
    data = {
        'email': email
    }

    # Send POST request to check if email is taken
    response = requests.post('https://www.instagram.com/api/v1/web/accounts/check_email/', headers=headers, data=data)

    # Check if 'email_is_taken' is in the response text
    if 'email_is_taken' in response.text:
        return True  # Email is taken
    else:
        return False  # Email is available
    
def check_insta(email):
    # List of stein functions
    stein_functions = [stein1, stein2, stein3, stein4, stein5]
    
    # Randomly choose one function from the list
    chosen_function = random.choice(stein_functions)
    
    # Call the chosen function with the email
    if chosen_function(email):
        return True
    else:
        return False

def gen_username(date):
    if date == 2010:
        iD = random.randrange(1, 1279000)  
    elif date == 2011:
        iD = random.randrange(1279001, 17750000)   
    elif date == 2012:
        iD = random.randrange(17750000, 279760000) 
    elif date == 2013:
        iD = random.randrange(279760000, 900990000)
    elif date == 2014:
        iD = random.randrange(900990000, 1629010000)   
    elif date == 2015:
        iD = random.randrange(1629010000, 2500000000)
    elif date == 2016:
        iD = random.randrange(2500000000, 3713668786)
    elif date == 2017:
        iD = random.randrange(3713668786, 5699785217)
    elif date == 2018:
        iD = random.randrange(5699785217, 8507940634)
    elif date == 2019:
        iD = random.randrange(8507940634, 21254029834)
    elif date in [2020, 2021, 2022, 2023, 2024]:
        iD = random.randrange(21254029834, 21954029834)
    else:
        return None

    rnd = random.randint(150, 999)

    user_agent = (
        "Instagram 311.0.0.32.118 Android (" +
        random.choice(["23/6.0", "24/7.0", "25/7.1.1", "26/8.0", "27/8.1", "28/9.0"]) +
        "; " + str(random.randint(100, 1300)) + "dpi; " +
        str(random.randint(200, 2000)) + "x" + str(random.randint(200, 2000)) + "; " +
        random.choice(["SAMSUNG", "HUAWEI", "LGE/lge", "HTC", "ASUS", "ZTE", "ONEPLUS", "XIAOMI", "OPPO", "VIVO", "SONY", "REALME"]) +
        "; SM-T" + str(rnd) + "; SM-T" + str(rnd) + "; qcom; en_US; 545986" + str(random.randint(111, 999)) + ")"
    )

    lsd = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    headers = {
        'accept': '*/*',
        'accept-language': 'en,en-US;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'origin': 'https://www.instagram.com',
        'priority': 'u=1, i',
        'referer': 'https://www.instagram.com/cristiano/following/',
        'user-agent': user_agent,
        'x-fb-friendly-name': 'PolarisUserHoverCardContentV2Query',
        'x-fb-lsd': lsd,
    }

    data = {
        'lsd': lsd,
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'PolarisUserHoverCardContentV2Query',
        'variables': json.dumps({"userID": iD, "username": "cristiano"}),
        'server_timestamps': 'true',
        'doc_id': '7717269488336001',
    }

    try:
        response = requests.post('https://www.instagram.com/api/graphql', headers=headers, data=data)
        username = response.json().get('data', {}).get('user', {}).get('username')
        return username
    except:
        try:
            variables = json.dumps({"id": iD, "render_surface": "PROFILE"})
            data = {"lsd": lsd, "variables": variables, "doc_id": "25618261841150840"}
            response = requests.post("https://www.instagram.com/api/graphql", headers={"X-FB-LSD": lsd}, data=data)
            username = response.json().get('data', {}).get('user', {}).get('username')
            return username
        except:
            return None
        
def get_user_info(username):
    try:
        user_data = InfoIG.Instagram_Info(username)  # Fetch data from Instagram
        reset_value = RestInsta.Rest(username).get("email", "Nothing To Rest")

        return {
            "username": username,
            "full_name": user_data.get("Name", "N/A"),
            "id": user_data.get("ID", "N/A"),
            "followers": int(user_data.get("Followers", 0)),
            "following": int(user_data.get("Following", 0)),
            "bio": user_data.get("Bio", "N/A"),
            "private_account": user_data.get("Is Private", False),
            "number_of_posts": int(user_data.get("Posts", 0)),
            "account_created_year": get_account_creation_year(user_data.get("ID", "0")),
            "reset": reset_value
        }
    except:
        return None
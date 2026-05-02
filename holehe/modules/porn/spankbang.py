from holehe.core import *
from holehe.localuseragent import *
import random


async def spankbang(email, client, out):
    name = "spankbang"
    domain = "spankbang.com"
    method = "register"
    frequent_rate_limit = False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    try:
        req = await client.get("https://spankbang.com/signup", headers=headers)
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return

    soup = BeautifulSoup(req.content, features="html.parser")
    # Look for token or csrf
    token = None
    try:
        token_input = soup.find('input', {'name': 'token'}) or soup.find('input', {'name': 'csrf_token'})
        if token_input:
            token = token_input.get('value')
    except:
        pass

    if not token:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return

    data = {
        'check_what': 'email',
        'email': email,
        'token': token
    }

    try:
        response = await client.post("https://spankbang.com/user/check_email", headers=headers, data=data)
        if response.status_code == 200:
            resp_json = response.json()
            if 'exists' in resp_json:
                exists = resp_json['exists']
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False,
                            "exists": exists,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
            else:
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
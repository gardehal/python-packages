import time

import requests
from furl import furl

from .HttpVerb import HttpVerb


def requestCallByUrl(url, verb, body = None, headers = None, retries = 4, timeout = 4, stream = False):
    """
    Make an request (module) call to {url}, using verb. Format params, header, and body like params = {"key1": "value1", "key2": "value2"}, 
    or body as just value. Retries default 4 times, waiting default 4 seconds after fail.
    """

    f = furl(url)
    return requestCall(f.origin, f.path, verb, params = f.query.params, body = body, headers = headers, retries = retries, timeout = timeout, stream = stream)

def requestCall(baseUrl, endpoint, verb, params = None, body = None, headers = None, retries = 4, timeout = 4, stream = False):
    """
    Make an request (module) call to {baseUrl}{endpoint}, using verb. Format params, header, and body like params = {"key1": "value1", "key2": "value2"}, 
    or body as just value. Retries default 4 times, waiting default 4 seconds after fail.
    """

    print(f"Making a web request to {baseUrl}{endpoint}...")

    response = None
    for i in range(retries):
        if(verb == HttpVerb.GET):
            response = requests.get(f"{baseUrl}{endpoint}", params = params, data = body, headers = headers, stream = stream)
        if(verb == HttpVerb.POST):
            response = requests.post(f"{baseUrl}{endpoint}", params = params, data = body, headers = headers, stream = stream)

        if(response.status_code >= 200 and response.status_code < 300):
            return response
        elif(response.status_code == 408 or response.status_code == 503):
            print(f"Request to {baseUrl}{endpoint} failed with code: {response.status_code}. Codes 408 and 503 are common for websites warming up. Retrying...")
            time.sleep(timeout)
        else:
            print(f"Request to {baseUrl}{endpoint} failed with code: {response.status_code}.")
            return response

    print(f"Web request to {baseUrl}{endpoint} failed all {retries} retries, after a minimum of {retries * timeout} seconds...")
    return response

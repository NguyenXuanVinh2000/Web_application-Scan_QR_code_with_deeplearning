import requests
from lxml.html import fromstring
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)


def title(content):
    """
    Get title website by framework requests
    """
    text =""
    if "http" in content: 
        r = requests.get(content, verify=False)
        tree = fromstring(r.content) 
        text = tree.findtext('.//title')
    return str(text)


import requests

proxy = "add ip address here"

proxies = {
    "http": f"http://{proxy}",
    "https": f"http://{proxy}",
}

try:
    response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
    print("Proxy is working!")
    print("Response:", response.text)

except requests.exceptions.ProxyError:
    print("Proxy error: Proxy is not working.")

except requests.exceptions.ConnectTimeout:
    print("Connection timed out: Proxy not responding.")

except Exception as e:
    print("Proxy failed:", str(e))

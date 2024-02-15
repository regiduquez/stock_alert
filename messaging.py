import http.client
import json
def send_msg(news_list):
    try:
        for i in range(0, 3):
            conn = http.client.HTTPSConnection("ggqn8w.api.infobip.com")
            payload = json.dumps({
                "messages": [
                    {
                        "destinations": [{"to":"639467624022"}],
                        "from": "ServiceSMS",
                        "text": news_list[i]
                    }
                ]
            })
            headers = {
                'Authorization': 'App 86a4a3ff22e2577d186bdc6c427c5d37-927c76a2-bac4-4dc0-9d28-72f2f3b94655 ',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            conn.request("POST", "/sms/2/text/advanced", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
    except IndexError:
        pass
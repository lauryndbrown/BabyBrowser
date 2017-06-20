import requests



if __name__=="__main__":
    request = requests.get("https://google.com")
    print(request.status_code)
    print(request.headers['content-type'])
    #print(request.text)




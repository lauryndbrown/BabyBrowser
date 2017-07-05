import requests
class Network:
    def __init__(self):
        self.request = None
    def get(self, url):
        self.request = requests.get(url)
        return self.request.text
    def get_image(url):
        img_request = requests.get(url)
        return img_request.content
if __name__=="__main__":
    url = "https://lauryndbrown.github.io/BabyBrowser/baby_browser/Examples/helloWorld2.html"
    network = Network()
    request = network.get(url)
    print(request)
    #print(request.status_code)
    #print(request.headers['content-type'])
    #print(request.text)




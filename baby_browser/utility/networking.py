import requests
class Network:
    def __init__(self):
        self.request = None
    def get(self, url):
        """Method that sends a GET request for url
        :param url: str containing webpage url 
        :returns: str containing request response
        """
        self.request = requests.get(url)
        return self.request.text
    def get_image(url):
        """Method that sends a GET request for image url
        :param url: str containing image url 
        :returns: str containing request response
        """
        img_request = requests.get(url)
        return img_request.content

import pip._vendor.requests as request

class zipcode:
    @classmethod
    def getAddressInformation(cls,zipcodeNumber: str):
        apiKey = "3eQEDC80cElYx8NW36kBaE0LIYLhMq4uJeq7fFGTmq0zU60QKaprBZ1Ds2RuHA6o"
        url= "https://www.zipcodeapi.com/rest/"+apiKey+"/info.json/"+zipcodeNumber+"/degrees"
        try:
            resp = request.get(url)
            return resp.json()
        except request.RequestException as e:
            return None

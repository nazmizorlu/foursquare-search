# encoding: utf-8
__author__ = 'Nazmi ZORLU'
__email__ = "nazmizorlu@gmail.com"

import requests
from django.utils.translation import ugettext_lazy as _


class FoursquareClient(object):
    """
    Basic Foursquare Client
    """

    API_URL = "https://api.foursquare.com/v2"

    ENDPOINTS = {
        "venues": "/venues"
    }

    VERSION = "20161001"

    def __init__(self, clientid=None, secret=None):
        """
        :param clientid: Client ID
        :param secret: Client Secret
        :return:
        """
        if not clientid or not secret:
            raise FourSquareException(_('ID and Secret required'))
        self.CLIENT_ID = clientid
        self.CLIENT_SECRET = secret

    def make_request(self, method, endpoint, action, **kwargs):
        """
        Makes request using python-requests
        :param method: Http Method (eg: GET, POST, PUT, ...)
        :param endpoint: API endpoint will be appended to API_URL (eg: venues)
        :param action: Action for API call (eg: search)
        :param kwargs: Params for requests.request (eg: headers, params, data,.)
        :return: Response object
        """
        try:
            req = requests.request(method=method.upper(),
                                   url="%s%s/%s" % (self.API_URL,
                                                    endpoint,
                                                    action),
                                   **kwargs)
        except Exception as ex:
            raise FourSquareException(_("Connection Error"))

        if req.status_code not in [200, 201]:
            raise FourSquareException(_("Invalid status: %d") % req.status_code)

        return req

    def venues_search(self, query, location):
        """
        Search venues with given parameters
        :param query: What is going to be searched
        :param location: Where is to be searched
        :return: JSON presentation of Response
        """
        params = {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "v": self.VERSION,
            "intent": "checkin",
            "radius": 1000,
            "limit": 50,
            "query": query,
            "near": location
        }
        response = self.make_request("GET",
                                     self.ENDPOINTS["venues"],
                                     "search",
                                     params=params)

        return response.json()


class FourSquareException(Exception):
    pass

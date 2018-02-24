import urllib.request
import urllib.parse
from collections import defaultdict
import json


def get_events_facebook(place):
    """
    """
    url_request = "https://graph.facebook.com/search?"
    my_access_token = "EAAWZCiuknSSsBAJfvqWnIZCy7KbYZCO5H20AK2jee9HZA3pWKgohJDXbYdYgiSGZC247ZCZAvn9QViM6PiVca54jt70IKJpQhGnAbzrSwpEpDR8XgWKbKDnnoN5k2BtaZAAmRHYofShALYC87FkF5ihHyZC9sDNnr7CYZD"
    data = {}
    data["q"] = place
    data["type"] = "event"
    data["access_token"] = my_access_token
    url_data = urllib.parse.urlencode(data)

    events_id_list = []
    count = 0
    while True:
        with urllib.request.urlopen(url_request + url_data) as response:
            fb_events = json.loads(response.read())
            for i in fb_events["data"]:
                events_id_list.append(i["id"])
            if fb_events.get("paging", None):
                data["after"] = fb_events["paging"]["cursors"]["after"]
            else:
                break
            url_values = urllib.parse.urlencode(data)
        break


    app_access_token = "1617978221611307|OCLa5GL6yIPlTT0_lKmL2SkrqMA"
    fb_url = "https://graph.facebook.com/v2.4/"

    events_dict = defaultdict(list)
    for i in events_id_list:
        event_url = fb_url + i + "?"
        data = {}
        data["fields"] = "name,description,category"
        data["access_token"] = app_access_token
        url_values = urllib.parse.urlencode(data)
        try:
            with urllib.request.urlopen(event_url + url_values) as response:
                fb_events_list = json.loads(response.read())
                print(fb_events_list.keys())
                if "category" in fb_events_list:
                    events_dict[fb_events_list["category"]] += [(fb_events_list["name"],fb_events_list["description"])]
                else:
                    if "description" in fb_events_list:
                        events_dict["NONE"] += [(fb_events_list["name"],fb_events_list["description"])]

        except ValueError:
            pass
    return events_dict

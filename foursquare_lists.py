
import json
import requests
import sys

URL_PREFIX = "https://api.foursquare.com/v2/"
AUTH_TOKEN = "KDGVWHX0HBPV0MPJHD1U3JK5LBX0TNEV2IJPVL0HQFOXZKAE"
VERSION = "20120321"

def make_url(api_call):
    symbol = "?"
    if "?" in api_call:
        symbol = "&"
    new_url = "%s%s%soauth_token=%s&v=%s" % (URL_PREFIX, api_call, symbol, AUTH_TOKEN, VERSION)
    return new_url

def make_request(url, debug=False):
    r = requests.get(url)
    json_response = json.loads(r.content)
    if debug:
        log(url)
        log(json_response)
    return json_response

def get_intersection(friend_user_ids):
    result = {}
    for friend_user_id in friend_user_ids:
        name = friends[friend_user_id]["firstName"] + " " + friends[friend_user_id]["lastName"]
        venue_names = [list_item['venue']['name'] for list_item in friends[friend_user_id]['todos']]
        result[name] = venue_names
    return result

def log(thing):
    print(json.dumps(thing, indent=4))

# Get friends.
friends_url = make_url("users/self/friends")
friends_response = make_request(friends_url)['response']['friends']['items']

friends = {}
for friend in friends_response:
    friends[friend['id']] = friend

# Get my todo list.
my_todo_url = make_url("lists/self/todos")
my_todo_response = make_request(my_todo_url)['response']['list']['listItems']['items']

my_todo_list = []
for my_todo_item in my_todo_response:
    my_todo_list.append(my_todo_item)

# Get friends' todo list.
for friend_user_id in friends.keys():
    friends_todo_lists_url = make_url("lists/%s/todos" % friend_user_id)
    friends_todo_lists_url_response = make_request(friends_todo_lists_url)['response']['list']['listItems']['items']
    friends[friend_user_id]['todos'] = friends_todo_lists_url_response

# Get intersection of example friend's todo list and mine.
friends_to_compare_against = [friend_user_id for friend_user_id in friends.keys()]
friends_lists_venues = get_intersection(friends_to_compare_against)
friends_lists_venues["me"] = [list_item['venue']['name'] for list_item in my_todo_list]

# Output results.
for friend_name in friends_lists_venues:
    venue_names = friends_lists_venues[friend_name]
    if not venue_names:
        venue_names = "None"
    print("%s: %s\n" % (friend_name, venue_names))

"""
8630995
11823665
12199088
15602674
13619535
48417
507183
23138842
"""

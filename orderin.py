import json
import requests

r =requests.get('https://r-test.ordr.in/rd/142')
res = json.loads(r.text)

menu = res["menu"]
print(json.dumps(menu, indent=4))

menu_str = ""
for menu_item in menu:
    children = menu_item["children"]
    for child in children:
        try:
            print(child["name"])
        except:
            pass

        try:
            print(child["descrip"])
        except:
            pass

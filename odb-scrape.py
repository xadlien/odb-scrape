import json
import requests

headers = {'Accept': 'application/json', 'Referer': 'https://odb.org/2020/02/08'}
url = "https://odb.org/wp-json/wp/v2/posts?after=2020-02-07T23:59:59.000Z&before=2020-02-09T00:00:00.000Z"
r = requests.get(url, headers=headers, verify=True)
print(json.dumps(r.json(), indent=4, sort_keys=True))

import requests

url = 'https://listen-api.listennotes.com/api/v2/search'
headers = {
  'X-ListenAPI-Key': '46220315dbab4391b5efd8e27fcde507',
}
payload = {
    'q':'Waypoint Radio',
    'type':'podcast'
}
response = requests.request('GET', url, headers=headers, params=payload)

search_result = response.json()['results']

first_pod = (search_result[0]['title_original'], search_result[0]['id'])

print(first_pod)

# url = 'https://listen-api.listennotes.com/api/v2/podcasts/2e10c22da54d4514ac0fbe0ab4b3f173'
# headers = {
#   'X-ListenAPI-Key': '46220315dbab4391b5efd8e27fcde507',
# }
# response = requests.request('GET', url, headers=headers)
# response.json()
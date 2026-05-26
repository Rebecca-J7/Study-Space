import requests, json
vark = {"visual":60,"auditory":20,"reading":15,"kinesthetic":5,"dominant":"Visual"}
res = requests.post('http://127.0.0.1:3000/api/study-space/v1/recommendations', json={'vark_result': vark})
print(res.status_code)
print(res.text)

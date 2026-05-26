import requests, json, sys
text = (
	"I learn best from videos and diagrams. I create color-coded notes, draw mindmaps, "
	"and prefer watching tutorials before reading textbooks. I also explain concepts aloud."
)
r = requests.post('http://127.0.0.1:8001/v1/process_quiz', json={'input': text})
print(r.status_code)
print(r.text)

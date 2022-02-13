# Python program to read
# json file
 
 
import json
order_name = 'pizza'
 
f = open('menu.json')
data = json.load(f)

for item in data['items']:
	if item['name'].lower() == order_name:
		order_json = item
print(order_json)
 
# Closing file
f.close()
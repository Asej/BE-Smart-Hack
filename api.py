import json
from flask import Flask
from flask import jsonify

app = Flask(__name__)
app.config["DEBUG"] = False


state_population = {
	'FL':21480000,
	'TX':29900000
}
county_population ={
	'Orange County':{
		'state':"FL",
		'population':1393000
	},
	'Travis County':{
		'state':"TX",
		'population':1290690
	},
	'Bastrop County':{
		'state':"TX",
		'population':91310
	},
	'Caldwell County':{
		'state':"TX",
		'population':44891
	},
	'Hays County':{
		'state':"TX",
		'population':239339
	},
	'Williamson County':{
		'state':"TX",
		'population':608261
	},
}


citycounty = {
	'Orlando':{
			'County':["Orange County"],
			'state':"FL"
			},
	'Austin': {
			'County':["Travis County","Bastrop County","Caldwell County","Hays County","Williamson County"],
			'state':"TX"
			''
			},
}
CDCapi = {
  'statedata':[
    {
    'state':"FL",
    'County':"Orange County",
    'PositiveCases':2177,
    'DeathTotal':502
    },
    {
    'state':"TX",
    'County':"Travis County",
    'PositiveCases':30165,
    'DeathTotal':441}    
    ],
  'usdata':[
    {
    'state':"FL",
    'PositiveCases':728921,
    'DeathTotal':15372,
    'Phase':3},
    {
    'state':"TX",
    'PositiveCases':785830,
    'DeathTotal':16432,
    'Phase':3}
  ]
}
arrival_bp = {
	'name': "Deben Peterson",
	'flight_id': "AA735",
	'from_location': {
					'state': "FL",
					'city': "Orlando"
	},
 	'to_location':{
					'state': "TX",
					'city': "Austin"
	},
	'seat': "17E",
	'depart_time': "3-25-2020-9-45",
	'arrival_time': "3-25-2020-13-55"
}
departure_bp = {
	'name': "Deben Peterson",
	'flight_id': "AA678",
	'from_location': {
					'state': "TX",
					'city': "Austin"
	},
	'to_location':{
					'state': "FL",
					'city': "Orlando:"
	},
	'seat': "10A",
	'depart_time': "3-29-2020-6-20",
	'arrival_time': "3-29-2020-12-55"
	}


def countyfinder(city):
	return citycounty[city]['County']


#vlaues will print in format [state_cases, state_deaths, state_phase, county_cases, county deaths]
@app.route('/api/vi/resources/cdcdata/all', methods=['GET'])
def cdcdata():
	state = arrival_bp['to_location']['state']
	city = arrival_bp['to_location']['city']
	values = []
	for i in CDCapi['usdata']:
		if i['state'] == state:
			values.append(i['PositiveCases'])
			values.append(i['DeathTotal'])
			values.append(i['Phase'])
	for i in CDCapi['statedata']:
		if i['County'] in countyfinder(city):
			values.append(i['PositiveCases'])
			values.append(i['DeathTotal'])
	
	return jsonify(values)

@app.route('/api/vi/resources/tripreview/risk', methods=['GET'])
def riskreview():
	state = arrival_bp['to_location']['state']
	city = arrival_bp['to_location']['city']
	county = countyfinder(city)

	countycases = 0
	countypop = 0

	for i in CDCapi['statedata']:
		if i['County'] in county:
			countycases = i.get('PositiveCases')

	for i in county_population[county]:
		countypop = i.get('population')


	countycases = 2000
	countypop = 4000
	if ((countycases / countypop) > .3):
		return "Our records show you have recently traveled to a corona virus hotspot"
	


if __name__ == '__main__':
	app.run(host='127.0.0.9',port=4455,debug=True)




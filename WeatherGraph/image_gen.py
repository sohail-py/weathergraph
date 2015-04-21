import pygal
import urllib2
import json

def generate_forecast_image(city, country, days_count, image_file_name = 'bar_chart'):
	'''
	A function to generate an bar chart image in an svg format for minimum, maximum and Average
	temperature - Nishant
	'''

	api_url = "http://api.openweathermap.org/data/2.5/forecast/daily?&lang=zh_cn&q=%s,%s&units=metric&cnt=%d" % (city, country, int(days_count))

	api_response = urllib2.urlopen(api_url).read()
	weather_data = json.loads(api_response)

	weather_forecast = weather_data['list']
	max_temp_list = []
	min_temp_list = []
	day_temp_list = []
	for each_day in weather_forecast[:-1]:
		max_temp_list.append(each_day['temp']['max'])
		min_temp_list.append(each_day['temp']['min'])
		day_temp_list.append(each_day['temp']['day'])

	line_chart = pygal.Line()
	line_chart.title = 'Temperature for next 16 days in %s, %s' % (city.capitalize(), country.upper()) 
	line_chart.x_labels = map(str, range(21, 21+16))
	
	line_chart.add('Maximum Temp',  max_temp_list)
	line_chart.add('Minimum Temp', min_temp_list)
	line_chart.add('Average day Temp',day_temp_list)
	
	line_chart.render_to_file(image_file_name+'.svg')
	
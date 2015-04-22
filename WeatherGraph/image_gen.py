import pygal
import urllib2
import json


class ForcastImage:
	
	def __init__(self,city,country,days_count,image_file_name= 'bar_chart'):
		
		self.city = city
		self.country = country
		self.days_count = days_count
		self.image_file_name = image_file_name
		self.api_url = "http://api.openweathermap.org/data/2.5/forecast/daily?&lang=zh_cn&q=%s,%s&units=metric&cnt=%d"% (city, country, int(days_count))
		self.max_temp_list = []
		self.min_temp_list = []
		self.day_temp_list = []
		self.line_chart = None
		
	def generateImage(self):
		
		self.api_response = urllib2.urlopen(self.api_url).read()
		self.weather_data = json.loads(self.api_response)
		self.weather_forecast = self.weather_data['list']
		
		for each_day in self.weather_forecast[:-1]:
			self.max_temp_list.append(each_day['temp']['max'])
			self.min_temp_list.append(each_day['temp']['min'])
			self.day_temp_list.append(each_day['temp']['day'])
			
		self.line_chart = pygal.Line()
		self.line_chart.title = 'Temperature for next 16 days in %s, %s' % (self.city.capitalize(), self.country.upper()) 
		self.line_chart.x_labels = map(str, range(21, 21+16))
		
		self.line_chart.add('Maximum Temp',  self.max_temp_list)
		self.line_chart.add('Minimum Temp', self.min_temp_list)
		self.line_chart.add('Average day Temp',self.day_temp_list)
		
		self.line_chart.render_to_file(self.image_file_name+'.svg')
		self.line_chart.render_to_png(filename=self.image_file_name)
		
		
		
if __name__ == '__main__':
	f=ForcastImage('Pune','in', 10, 'pune_in')
	f.generateImage() 		
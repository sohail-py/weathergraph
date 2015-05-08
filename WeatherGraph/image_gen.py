import pygal
import urllib2
import json
import calendar
from datetime import datetime


class dayslimitexceeded(Exception):
	pass

def returnDaysAheadoftime(days_count_from_today):
	'''
	this function will return list of dates from current month to next month.
	currently only avaibale for days < 16
	'''
	if days_count_from_today > 16:
		raise dayslimitexceeded('Days limit exceeded ,days < 16')
	
	x=1
	days_list=[]
	for i in range(datetime.now().day,datetime.now().day+days_count_from_today):
		if i > calendar.monthrange(datetime.now().year,datetime.now().month)[1]:
			days_list.append(x)
			x+=1
		else:
			days_list.append(i)
	return days_list

class ForecastImage:
	'''
	this class will convert weather data in to chart.
	
	'''
	
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
		self.api_response = urllib2.urlopen(self.api_url).read()
		self.weather_data = json.loads(self.api_response)
		self.weather_forecast = self.weather_data['list']
		self.days_list=[]

	def generateImage(self):
		
		
		for each_day in self.weather_forecast[:-1]:
			self.max_temp_list.append(each_day['temp']['max'])
			self.min_temp_list.append(each_day['temp']['min'])
			self.day_temp_list.append(each_day['temp']['day'])
			
		self.line_chart = pygal.Line()
		self.line_chart.title = 'Temperature for next %s days in %s, %s' % (self.days_count,self.city.capitalize(), self.country.upper()) 
# 		self.line_chart.x_labels = map(str, range(21, 21+16))
		self.line_chart.x_labels = map(str, returnDaysAheadoftime(self.days_count))
		
		self.line_chart.add('Maximum Temp',  self.max_temp_list)
		self.line_chart.add('Minimum Temp', self.min_temp_list)
		self.line_chart.add('Average day Temp',self.day_temp_list)
		
		self.line_chart.render_to_file(self.image_file_name+'.svg')
		self.line_chart.render_to_png(filename=self.image_file_name+'.png')

class RainForecastImage:
	'''
	this class will convert weather data in to chart.
	
	'''
	
	def __init__(self,city,country,days_count,image_file_name= 'bar_chart'):
		
		self.city = city
		self.country = country
		self.days_count = days_count
		self.image_file_name = image_file_name
		self.api_url = "http://api.openweathermap.org/data/2.5/forecast/daily?&lang=zh_cn&q=%s,%s&units=metric&cnt=%d"% (city, country, int(days_count))
		
		self.rain_forecast_list = []
		self.api_response = urllib2.urlopen(self.api_url).read()
		self.weather_data = json.loads(self.api_response)
		self.weather_forecast = self.weather_data['list']
		
	def genrateRainForecastImage(self):

		for each_day in self.weather_forecast[:-1]:
			if each_day.has_key('rain') == True:

				self.rain_forecast_list.append(each_day['rain'])

			else:
				self.rain_forecast_list.append(0)
		bar_chart = pygal.Bar()
		bar_chart.title = 'Rain forecast for next 16 days in %s, %s' % (self.city.capitalize(), self.country.upper()) 
# 		bar_chart.x_labels = map(str, range(21, 21+16))
		bar_chart.x_labels = map(str, returnDaysAheadoftime(self.days_count))
		
		
		bar_chart.add('Rains',  self.rain_forecast_list)
		bar_chart.render_to_file(self.image_file_name +'.svg')
		bar_chart.render_to_png(filename=self.image_file_name+'.png')

		

if __name__ == '__main__':
	f=ForecastImage('Pune','in', 15, 'pune_in')
	f.generateImage()
	obj1 = RainForecastImage('Pune','in',16,'rain_forecast_pune')
	obj1.genrateRainForecastImage()
	obj2 = RainForecastImage('New York','us',16,'rain_forecast_ny')
	obj2.genrateRainForecastImage()
from setuptools import setup

setup(	name='inspace',
		version='0.1',
		description= 'Jump into space with Nasa s photo of the day',
		author= 'RaddadZ',
		author_email= 'ananraddad@gmail.com',
		install_requires= [
			'BeautifulSoup',
			'urllib2',
			'urllib'
		],
		zip_safe=False
	 )

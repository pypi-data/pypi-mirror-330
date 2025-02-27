from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='jobject',
	version='1.0.3',
	description='jobject: A dictionary replacement that gives additional ' \
				'access to data using C struct notation, just like ' \
				'JavaScript Objects',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/ouroboroscoding/jobject',
	project_urls={
		'Source': 'https://github.com/ouroboroscoding/jobject',
		'Tracker': 'https://github.com/ouroboroscoding/jobject/issues'
	},
	keywords=['javascript', 'object', 'struct'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='MIT',
	packages=['jobject'],
	python_requires='>=3.10',
	install_requires=[],
	zip_safe=True
)
from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='tools-oc',
	version='1.2.5',
	description='A set of tools for common python problems',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/ouroboroscoding/tools-python',
	project_urls={
		'Source': 'https://github.com/ouroboroscoding/tools-python',
		'Tracker': 'https://github.com/ouroboroscoding/tools-python/issues'
	},
	keywords=['tools', 'clone', 'diff', 'merge', 'combine'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='MIT',
	packages=['tools'],
	python_requires='>=3.10',
	install_requires=[
		"jobject>=1.0.3,<1.1"
	],
	zip_safe=True
)
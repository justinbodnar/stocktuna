from setuptools import setup, find_packages

setup(
	name='stocktuna',
	version='0.2.0',
	packages=find_packages(),
	install_requires=[
		'alpaca-trade-api',
		'matplotlib',
	],
	author='Justin Bodnar',
	author_email='contact@justinbodnar.com',
	description='A library for processing stock market data and creating trading strategies',
	license='MIT',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Libraries',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Operating System :: OS Independent',
	],
)

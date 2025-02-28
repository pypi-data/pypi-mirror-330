from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
try: 
    long_description = (this_directory / "readme.md").read_text()
except:
    long_description = "Official Library for spark.maticalgos.com"

def parse_requirements(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()
    
setup(
name='maticalgos-spark',
version='0.2.12',
author='Niraj Munot',
author_email='nirajmunot28@gmail.com',
description='SparkLib is a Python client library for interacting with https://spark.maticalgos.com . It provides functionalities to manage accounts, strategies, place orders, and much more.',
long_description=long_description,
include_package_data=True,
package_data={"map.json":['maticalgos/sparkLib/utility/dataws/dependencies/fyersAPIv3/map.json']},
data_files=[("map.json", ['maticalgos/sparkLib/utility/dataws/dependencies/fyersAPIv3/map.json'])],
long_description_content_type='text/markdown',
packages=find_packages(),
install_requires=['websocket-client==1.7.0', 'numpy==1.26.4', 'requests==2.31.0'],
extras_require={'dataws' : ['python-engineio==3.13.0', 'python-socketio==4.6.0', 'aws-lambda-powertools==1.25.5', 'websockets==13.0.1', 'protobuf==5.28.1'], 
                'wsHandler' : ['python-engineio==3.13.0', 'python-socketio==4.6.0','aws-lambda-powertools==1.25.5', 
                               'websockets==13.0.1', 'protobuf==5.28.1',
                               'pyzmq==26.2.0', 'redis==4.3.4'],
                "full" : ['python-engineio==3.13.0', 'python-socketio==4.6.0','aws-lambda-powertools==1.25.5', 
                               'websockets==13.0.1', 'protobuf==5.28.1','websocket-client==1.7.0', 'numpy==1.26.4', 'requests==2.31.0', #websockets==8.1 protobuf==3.20.1
                               'pyzmq==26.2.0', 'redis==4.3.4','duckdb==1.0.0','datetime==4.3', 'pandas==2.2.2']}, ##pyzmq==26.2.0 #old 23.2.0
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)
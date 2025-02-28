from setuptools import setup, find_packages

setup(
    name='biz-affordabox-rss-parser',
    version='0.1',
    packages=find_packages(
        exclude=[
            'packages', 
            'packages.*', 
            'lambda_function.py', 
            'requirements.txt', 
            'server.py', 
            'test.py',
            'venv',
            'venv.*'
            ]),
    install_requires=[
        'beautifulsoup4==4.9.3',
        'boto3==1.17.4',
        'botocore==1.20.4',
        'dateparser==1.0.0',
        'feedparser==6.0.2',
        'lxml==4.6.3',
        'pytz==2021.1',
        'requests==2.25.1',
        's3fs==0.5.1'
    ],
    
)
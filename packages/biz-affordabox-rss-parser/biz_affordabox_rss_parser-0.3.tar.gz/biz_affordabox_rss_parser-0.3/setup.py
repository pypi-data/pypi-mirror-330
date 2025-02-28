from setuptools import setup, find_packages

setup(
    name='biz-affordabox-rss-parser',
    version='0.3',
    packages=find_packages(
        exclude=[
            'biz-affordabox-rss-parser-python.packages', 
            'biz-affordabox-rss-parser-python.packages.*', 
            'biz-affordabox-rss-parser-python.lambda_function', 
            'biz-affordabox-rss-parser-python.requirements', 
            'biz-affordabox-rss-parser-python.server', 
            'biz-affordabox-rss-parser-python.test',
            'biz-affordabox-rss-parser-python.venv',
            'biz-affordabox-rss-parser-python.venv.*'
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
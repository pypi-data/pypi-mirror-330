from setuptools import setup, find_packages

setup(
    name='biz-affordabox-rss-parser',
    version='0.4',
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
        'beautifulsoup4',
        'boto3',
        'botocore',
        'dateparser',
        'feedparser',
        'lxml',
        'pytz',
        'requests',
        's3fs'
    ],
    
)
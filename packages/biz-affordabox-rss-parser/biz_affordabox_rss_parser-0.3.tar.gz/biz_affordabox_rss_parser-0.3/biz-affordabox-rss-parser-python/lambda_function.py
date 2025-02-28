import sys
sys.path.insert(1, './package')

from fetch_doh import fetch_press_releases
from fetch_pagasa import fetch_weather_outlook
from fetch_phivolcs import fetch_volcano_bulletins

from save_s3 import write_file_to_s3
from parser.create_rss_feed import RSSFeed
from parser.create_rss_item import RSSItem

import json
import pytz
from datetime import datetime, timedelta
from dateutil import parser
import os
import re
import hashlib

from parser.rss_generator import RSSFeedGenerator
from pprint import pprint

def is_running_on_aws_lambda():
    return 'AWS_LAMBDA_FUNCTION_NAME' in os.environ

def trim_and_collapse_whitespace(text):
    # return text
    return re.sub(r'\s+', ' ', text).strip()

def to_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def parse_date_time(date_str):
    try:
        return parser.parse(date_str)
    except ValueError:
        return date_str

def save_parsed_data_to_s3(suffix, processedData):
    thisDatetime = datetime.now(pytz.timezone('Asia/Manila')).strftime('%Y-%m-%d %H:%M:%S')
    bucket_name = os.getenv('AWS_S3_DEFAULT_BUCKET')
    region_name = os.getenv('AWS_ACCOUNT_REGION')
    path_prefix = os.getenv('AWS_S3_OUTPUT_PATH')

    path = f"{path_prefix}/archive/{thisDatetime}-{suffix}.json"
    pathLatest = f"{path_prefix}/latest/{suffix}.json"
    pathRss = f"{path_prefix}/latest/{suffix}.rss"
    pathMainRss = f"{path_prefix}/{suffix}.rss"

    current_data = get_s3_file(bucket_name, pathLatest, region_name)
    previous_data = json.loads(current_data) if current_data else []
    output_data = previous_data + processedData

    unique_output_data = [dict(t) for t in {tuple(d.items()) for d in output_data}]
    sorted_previous_data = sorted(previous_data, key=lambda x: parser.parse(x['published_date']), reverse=True)
    sorted_unique_output_data = sorted(unique_output_data, key=lambda x: parser.parse(x['published_date']), reverse=True)

    print("==============================Output===================================")
    pprint(sorted_unique_output_data)
    print("=======================================================================")
    if sorted_previous_data != sorted_unique_output_data:
        write_file_to_s3(bucket_name, path, json.dumps(sorted_unique_output_data), 'application/json', region_name)
        write_file_to_s3(bucket_name, pathLatest, json.dumps(sorted_unique_output_data[:100]), 'application/json', region_name)

        rss_output = generate_rss_feed(suffix,{}, sorted_unique_output_data)
        rss_output_50 = generate_rss_feed(suffix,{}, sorted_unique_output_data[:50])
        # rss_data = generate_rss_items(sorted_unique_output_data, suffix, {}, rss_output)
        # rss_data_50 = generate_rss_items(sorted_unique_output_data[:50], suffix, {}, rss_output_50)

        write_file_to_s3(bucket_name, pathRss, rss_output, 'application/xml', region_name, True)
        write_file_to_s3(bucket_name, pathMainRss, rss_output_50, 'application/xml', region_name, True)

        data = [
            f"https://s3.{region_name}.amazonaws.com/{bucket_name}/{path}",
            f"https://s3.{region_name}.amazonaws.com/{bucket_name}/{pathLatest}",
            f"https://s3.{region_name}.amazonaws.com/{bucket_name}/{pathRss}",
            f"https://s3.{region_name}.amazonaws.com/{bucket_name}/{pathMainRss}"
        ]
    else:
        data = [
            'No new data',
            f"https://s3.{region_name}.amazonaws.com/{bucket_name}/{pathLatest}",
            f"https://s3.{region_name}.amazonaws.com/{bucket_name}/{pathMainRss}"
        ]

    return data

def rss_config_parameters(rss_type, args):
    if rss_type == 'gmartv':
        title = 'GMA Regional TV News'
        link = 'https://www.gmanetwork.com/regionaltv/news/'
        guid_prefix = 'https://www.gmanetwork.com/regionaltv/news/'
        if os.getenv('ENVIRONMENT') != 'PRODUCTION':
           guid_prefix = 'https://www.tgmanetwork.com/regionaltv/news/'

        twitter_username = 'gmaregionaltv'
        description = 'Regional TV (RTV) Department is the operational arm of GMA Network, Inc. in key cities and provinces in the Philippines. With our regional stations and offices strategically located across the country, GMA Regional TV produces top-rating and award-winning local programs and TV specials, and mounts tailor-fit events and activities for a diverse regional audience and clientele.'
    elif rss_type == 'gmanews':
        title = 'GMA News'
        link = 'https://www.gmanetwork.com/news/'
        guid_prefix = ''
        description = ''
    elif rss_type == 'pagasa':
        title = 'PAGASA-DOST'
        link = 'https://www.pagasa.dost.gov.ph/weather/weather-outlook-weekly'
        guid_prefix = 'https://www.pagasa.dost.gov.ph/weather/weather-outlook-weekly'
        twitter_username = 'dost_pagasa'
        description = 'Philippine Atmospheric, Geophysical and Astronomical Services Administration'
    elif rss_type == 'phivolcs':
        title = 'PHIVOLCS-DOST'
        link = 'https://www.phivolcs.dost.gov.ph/index.php/volcano-hazard/volcano-bulletin2'
        guid_prefix = 'https://www.phivolcs.dost.gov.ph/index.php/volcano-hazard/volcano-bulletin2'
        twitter_username = 'phivolcs_dost'
        description = 'PHIVOLCS is the service institute of the DOST for monitoring and mitigation of volcanic eruptions, earthquakes and tsunami.'
    elif rss_type == 'doh':
        title = 'Department of Health'
        link = 'https://doh.gov.ph/news/press-releases/'
        guid_prefix = 'https://doh.gov.ph/news/press-releases/'
        twitter_username = 'DOHgovph'
        description = 'Tweets of the Official Twitter Account of the Department of Health, Philippines'
    else:
        rss_type = 'testing'
        title = 'Testing'
        link = 'https://www.example.com/'
        guid_prefix = 'https://twitter.com/testing/status/'
        twitter_username = 'testing'
        description = 'Testing Description'

    return {
        'title': title,
        'link': link,
        'guid_prefix': guid_prefix,
        'twitter_username': twitter_username,
        'description': description
    }

def generate_rss_items(formatted_output, rss_type, args, feed : RSSFeedGenerator):
    rss_items = []
    rss_config = rss_config_parameters(rss_type, args)
    for item in formatted_output:

        # PARSING DATE - per source format
        formatted_date = item['published_date']

        # guid_url = rss_config['guid_prefix'] + item['post_id']
        # if (rss_type == 'gmartv'):
        #     guid_url = rss_config['guid_prefix'] + item['post_id'] + '/' + item['title'].encode('ascii',errors='ignore').decode().replace(' ', '-').lower() + '/' + 'story'

        guid_url = '-'

        feed.insert_item(title=item['title'], pubdate=formatted_date)

#         rss_item = f"""<item>
# <title>{item['title']}</title>
# <pubDate>{formatted_date}</pubDate>
# </item>"""

#         # EXPLORATORY - DO NOT USE YET
#         rss_item_new = f"""<item>
# <title>{item['title']}</title>
# <pubDate>{formatted_date}</pubDate>
# <guid>{guid_url}</guid>
# </item>"""

        
    return feed

def generate_rss_feed(rss_type, args = {}, formatted_output : list[dict] = []):
    rss_config = rss_config_parameters(rss_type, args)

    print(rss_config)

    title = rss_config.get('title', '')
    link = rss_config.get('link', '')
    description = rss_config.get('description', '')

    data = {
        'title': title,
        'link': link,
        'description': description,
    }

    feed = RSSFeedGenerator(**data)

    print("============Formatted Output============")
    pprint(formatted_output)

    for item in formatted_output:
        # pprint(item)
        formatted_date = item['published_date']
        description = item.get('description', '')
        link = item.get('link', '')
        # print("Description: ", description)


        feed.insert_item(title=item['title'], 
                         pubDate=formatted_date, 
                         guid=item['id'], 
                         description=description, 
                         link=link)

    # pprint(feed.get_element_string())
    return feed.get_element_string().decode('utf-8')

#     rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
# <rss version="2.0">
# <channel>
# <title>{rss_config.get('title', '')}</title>
# <link>{rss_config.get('link', '')}</link>
# <description>{rss_config.get('description', '')}</description>
# {''.join(rss_items)}</channel></rss>"""    
    
#     # EXPLORATORY - DO NOT USE YET
#     rss_feed_new = f"""<?xml version="1.0" encoding="UTF-8"?>
# <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
# <channel>
# <title>{rss_config.get('title', '')}</title>
# <link>{rss_config.get('link', '')}</link>
# <description>{rss_config.get('description', '')}</description>
# <atom:link href="https://data.gmanews.tv/affordabox_rss/{rss_type}.rss" rel="self" type="application/rss+xml" />
# {''.join(rss_items)}</channel></rss>"""
#     return rss_feed

def lambda_handler(event, context):
    thisDatetime = datetime.now(pytz.timezone('Asia/Manila')).strftime('%Y-%m-%d %H:%M:%S')
    thisPath = event.get('rawPath', '')
    data = []

    if thisPath == '/v1/get/pagasa':
        url = os.getenv('SOURCE_URL_PAGASA')
        data = fetch_weather_outlook(url)

    elif thisPath == '/v1/get/phivolcs':
        volcano_bulletins_url = os.getenv('SOURCE_URL_PHIVOLCS')
        data = fetch_volcano_bulletins(volcano_bulletins_url)
        pprint(data['bulletins'])

    elif thisPath == '/v1/get/doh':
        press_releases_url = os.getenv('SOURCE_URL_DOH')
        data = fetch_press_releases(press_releases_url)

    elif thisPath == '/v1/get/gmartv':
        bucket_name = os.getenv('SOURCE_BUCKET_RTV')
        path = os.getenv('SOURCE_PATH_RTV')
        region_name = os.getenv('SOURCE_REGION_RTV')
        s3Data = get_s3_file(bucket_name, path, region_name)
        data = json.loads(s3Data)

        print("===========================GMA RTV=================================")
        pprint(data)
        print("===================================================================")

    elif thisPath == '/v1/parse/pagasa':
        url = os.getenv('SOURCE_URL_PAGASA')
        weather_data = fetch_weather_outlook(url)
        readData = weather_data

        processedData = []
        for item in readData['advisories']:
            print(item)
            split_date = readData.get('issued_date', '').split(',')
            reformat_date = split_date[1] + ', ' + split_date[0] if len(split_date) > 1 else readData.get('issued_date', '')
            parsed_date = parse_date_time(trim_and_collapse_whitespace(reformat_date))
            philippine_tz = pytz.timezone('Asia/Manila')
            if (is_running_on_aws_lambda()):
                parsed_date = parsed_date - timedelta(hours=8)

            # PARSING DATE - format output
            formatted_date = parsed_date.astimezone(philippine_tz).strftime('%b %d, %Y %I:%M %p')

            processedData.append({
                'id': to_md5(trim_and_collapse_whitespace(readData.get('issued_date', '') + ' : ' + item.get('date', ''))),
                'description': str(trim_and_collapse_whitespace(item.get('description', ''))).strip(),
                'title': str(trim_and_collapse_whitespace(item.get('title', ''))).strip(),
                'published_date': formatted_date,
                'source': 'pagasa'
            })

        print("==================================================================")
        print("Processed Data (Pagasa): ")
        pprint(processedData)
        print("==================================================================")

        data = save_parsed_data_to_s3('pagasa', processedData)

    elif thisPath == '/v1/parse/phivolcs':
        volcano_bulletins_url = os.getenv('SOURCE_URL_PHIVOLCS')
        bulletins_data = fetch_volcano_bulletins(volcano_bulletins_url)
        readData = bulletins_data

        processedData = []
        for item in readData['bulletins']:
            parsed_date = parse_date_time(trim_and_collapse_whitespace(item.get('publication_date', '')))
            philippine_tz = pytz.timezone('Asia/Manila')

            # PARSING DATE - format output
            formatted_date = parsed_date.astimezone(philippine_tz).strftime('%b %d, %Y %I:%M %p')

            processedData.append({
                'id': to_md5(trim_and_collapse_whitespace(item.get('publication_date', ''))),
                'description': trim_and_collapse_whitespace(item.get('description', '')),
                'title': trim_and_collapse_whitespace(item.get('title', '')),
                'published_date': formatted_date,
                'source': 'phivolcs'
            })
        
        print("==================================================================")
        print("Processed Data (Phivolcs): ")
        pprint(processedData)
        print("==================================================================")

        data = save_parsed_data_to_s3('phivolcs', processedData)

    elif thisPath == '/v1/parse/doh':
        press_releases_url = os.getenv('SOURCE_URL_DOH')
        press_releases_data = fetch_press_releases(press_releases_url)
        readData = press_releases_data

        processedData = []
        for item in readData['press_releases']:
            parsed_date = parse_date_time(trim_and_collapse_whitespace(item.get('publication_date', '')))
            philippine_tz = pytz.timezone('Asia/Manila')

            # PARSING DATE - format output
            formatted_date = parsed_date.astimezone(philippine_tz).strftime('%b %d, %Y %I:%M %p')

            processedData.append({
                'id': to_md5(trim_and_collapse_whitespace(item.get('publication_date', ''))),
                'title': trim_and_collapse_whitespace(item.get('title', '')),
                'published_date': formatted_date,
                'source': 'doh'
            })

        data = save_parsed_data_to_s3('doh', processedData)

    elif thisPath == '/v1/parse/gmartv':
        bucket_name = os.getenv('SOURCE_BUCKET_RTV')
        path = os.getenv('SOURCE_PATH_RTV')
        region_name = os.getenv('SOURCE_REGION_RTV')
        s3Data = get_s3_file(bucket_name, path, region_name)
        readData = json.loads(s3Data)

        print("===========================GMA RTV=================================")
        pprint(readData)
        print("===================================================================")

        processedData = []
        for item in readData['data']['details']:
            parsed_date = parse_date_time(trim_and_collapse_whitespace(item.get('published_date', '')))
            philippine_tz = pytz.timezone('Asia/Manila')
            if (is_running_on_aws_lambda()):
                parsed_date = parsed_date - timedelta(hours=8)

            # PARSING DATE - format output
            formatted_date = parsed_date.astimezone(philippine_tz).strftime('%b %d, %Y %I:%M %p')

            processedData.append({
                'id': trim_and_collapse_whitespace(item.get('id', '')),
                'title': trim_and_collapse_whitespace(item.get('title', '')),
                'description' : trim_and_collapse_whitespace(item.get('body', '')),
                'published_date': formatted_date,
                'source': 'gmartv'
            })

        data = save_parsed_data_to_s3('gmartv', processedData)
        
    elif thisPath == '/v2/parse/pagasa':
        from main_parsers import parse_pagasa_v2
        parse_pagasa_v2()
        
    output = {
        'path': thisPath,
        'datetime': thisDatetime,
        'data': data
    }

    return {
        'statusCode': 200,
        'headers': {"content-type": "application/javascript"},
        'body': json.dumps(output)
    }

if not is_running_on_aws_lambda():
    print("Running locally")
    first_argument = sys.argv[1] if len(sys.argv) > 1 else ''
    output = lambda_handler({'rawPath': '/' + first_argument}, None)
    print("=====================================================")
    print(output)
    print("=====================================================")

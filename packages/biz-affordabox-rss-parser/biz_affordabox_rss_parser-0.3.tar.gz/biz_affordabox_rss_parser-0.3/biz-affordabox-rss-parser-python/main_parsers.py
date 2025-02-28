from parser.rss_generator import RSSFeedGenerator
from pprint import pprint
from save_s3 import write_file_to_s3
from fetch_s3 import get_s3_file

import json
import pytz
from datetime import datetime, timedelta
from dateutil import parser
import os
import re
import hashlib

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
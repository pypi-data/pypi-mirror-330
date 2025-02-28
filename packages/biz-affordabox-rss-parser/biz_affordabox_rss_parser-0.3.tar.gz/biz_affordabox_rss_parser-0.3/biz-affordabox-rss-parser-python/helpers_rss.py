from datetime import datetime, timedelta

def rss_config_parameters(rss_type, args):
    if rss_type == 'gmartv':
        title = 'GMA Regional TV News'
        link = 'https://www.gmanetwork.com/regionaltv/news/'
        if args.environment != 'production':
            guid_prefix = 'https://www.tgmanetwork.com/regionaltv/news/'
        else:
            guid_prefix = 'https://www.gmanetwork.com/regionaltv/news/'
        twitter_username = 'gmaregionaltv'
        description = 'Regional TV (RTV) Department is the operational arm of GMA Network, Inc. in key cities and provinces in the Philippines. With our regional stations and offices strategically located across the country, GMA Regional TV produces top-rating and award-winning local programs and TV specials, and mounts tailor-fit events and activities for a diverse regional audience and clientele.'
    elif rss_type == 'gmanews':
        title = 'GMA News'
        link = 'https://www.gmanetwork.com/news/'
        guid_prefix = ''
        description = ''
    elif rss_type == 'pagasa':
        title = 'PAGASA-DOST'
        link = 'https://twitter.com/dost_pagasa'
        guid_prefix = 'https://twitter.com/dost_pagasa/status/'
        twitter_username = 'dost_pagasa'
        description = 'Philippine Atmospheric, Geophysical and Astronomical Services Administration'
    elif rss_type == 'phivolcs':
        title = 'PHIVOLCS-DOST'
        link = 'https://twitter.com/phivolcs_dost'
        guid_prefix = 'https://twitter.com/phivolcs_dost/status/'
        twitter_username = 'phivolcs_dost'
        description = 'PHIVOLCS is the service institute of the DOST for monitoring and mitigation of volcanic eruptions, earthquakes and tsunami.'
    elif rss_type == 'doh':
        title = 'Department of Health'
        link = 'https://twitter.com/DOHgovph'
        guid_prefix = 'https://twitter.com/dohgovph/status/'
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

def rss_convert_array_to_items(formatted_output, rss_type, args):
    rss_items = []
    rss_config = rss_config_parameters(rss_type, args)
    for item in formatted_output:

        # Check if the published_date is a string or a datetime object
        if isinstance(item['published_date'], str):
            # Parse the date string
            date_obj = datetime.strptime(item['published_date'], '%Y-%m-%d %H:%M:%S')
        elif isinstance(item['published_date'], datetime):
            date_obj = item['published_date']
        else:
            raise ValueError("published_date must be a string or datetime object")

        # OLD: Format the date string to 'Mon Day, YYYY HH:MM am/pm'
        formatted_date = date_obj.strftime('%b %d, %Y %I:%M %p').lower()

        # Format the date to RFC-822
        # formatted_date = convert_to_rfc822_philippine_time(item['published_date'])

        formatted_date = formatted_date[0].upper() + formatted_date[1:]

        guid_url = rss_config['guid_prefix'] + item['post_id']
        if (rss_type == 'gmartv'):
            guid_url = rss_config['guid_prefix'] + item['post_id'] + '/' + item['title'].encode('ascii',errors='ignore').decode().replace(' ', '-').lower() + '/' + 'story'

        rss_item = f"""<item>
<title>{item['title']}</title>
<pubDate>{formatted_date}</pubDate>
</item>
"""

        rss_item_new = f"""<item>
<title>{item['title']}</title>
<pubDate>{formatted_date}</pubDate>
<guid>{guid_url}</guid>
</item>
"""

        rss_items.append(rss_item)
    return rss_items

def rss_format_create(rss_type, rss_items = [], args = {}):
    rss_config = rss_config_parameters(rss_type, args)

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>{rss_config.get('title', '')}</title>
<link>{rss_config.get('link', '')}</link>
<description>{rss_config.get('description', '')}</description>
<atom:link href="https://data.gmanews.tv/affordabox_rss/{rss_type}.rss" rel="self" type="application/rss+xml" />
{''.join(rss_items)}
</channel>
</rss>"""    
    
    rss_feed_new = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>{rss_config.get('title', '')}</title>
<link>{rss_config.get('link', '')}</link>
<description>{rss_config.get('description', '')}</description>
{''.join(rss_items)}
</channel>
</rss>"""
    return rss_feed

def get_destination_path(rss_type, environment = ''):
    output = {}
    if environment == 'production':
        output['bucket'] = 'data3.gmanews.tv'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rss'
        output['filename'] =  rss_type
    elif environment == 'production_preprod':
        output['bucket'] = 'data3.gmanews.tv'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rss'
        output['filename'] =  rss_type + '_output'
    elif environment == 'production_prod':
        output['bucket'] = 'data3.gmanews.tv'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rssprod'
        output['filename'] =  rss_type
    elif environment == 'production_dev':
        output['bucket'] = 'data3.gmanews.tv'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rssdev'
        output['filename'] =  rss_type
    elif environment == 'test001':
        output['bucket'] = 'test1.gmanetwork.com'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rss'
        output['filename'] =  rss_type
    elif environment == 'test001_test':
        output['bucket'] = 'test1.gmanetwork.com'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rss'
        output['filename'] =  rss_type + '_output'
    elif environment == '3pa':
        output['bucket'] = '3pa.gmanetwork.com'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rss'
        output['filename'] =  rss_type
    elif environment == '3pa_test':
        output['bucket'] = '3pa.gmanetwork.com'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rss'
        output['filename'] =  rss_type + '_output'
    elif environment == 'testing':
        output['bucket'] = 'test.gmanetwork.com'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rss'
        output['filename'] =  rss_type
    elif environment == 'testing_test':
        output['bucket'] = 'test.gmanetwork.com'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rss'
        output['filename'] =  rss_type + '_output'
    elif environment == 'testing2':
        output['bucket'] = 'test.gmanetwork.com'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rss_test'
        output['filename'] =  rss_type
    elif environment == 'dev':
        output['bucket'] = 'dev.gmanetwork.com'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rss'
        output['filename'] =  rss_type
    elif environment == 'dev_test':
        output['bucket'] = 'dev.gmanetwork.com'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rss'
        output['filename'] =  rss_type + '_output'
    else:
        output['bucket'] = 'dev.gmanetwork.com'
        output['region'] = 'ap-southeast-1'
        output['path'] = 'affordabox_rss_test'
        output['filename'] =  rss_type

    return output

def convert_to_rfc822_philippine_time(date_input):
    # Check if the input is a string or a datetime object
    if isinstance(date_input, str):
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date_input, '%Y-%m-%d %H:%M:%S')
    elif isinstance(date_input, datetime):
        date_obj = date_input
    else:
        raise ValueError("date_input must be a string or datetime object")

    # Manually adjust to Philippine Time (UTC+8)
    # date_obj_pht = date_obj + timedelta(hours=8)

    # Already in Philippine Time (UTC+8)
    date_obj_pht = date_obj

    # Format the date to RFC-822
    formatted_date = date_obj_pht.strftime('%a, %d %b %Y %H:%M:%S +0800')

    return formatted_date
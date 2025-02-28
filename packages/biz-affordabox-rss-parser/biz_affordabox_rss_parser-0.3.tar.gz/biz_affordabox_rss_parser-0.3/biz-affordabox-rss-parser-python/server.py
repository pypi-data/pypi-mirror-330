from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from fetch_pagasa import fetch_weather_outlook
from fetch_doh import fetch_press_releases
from fetch_phivolcs import fetch_volcano_bulletins
from fetch_s3 import get_s3_file
from dotenv import load_dotenv
from main_parsers import *
import json

load_dotenv()

production = os.getenv("PRODUCTION", False)

app = FastAPI(
    openapi_url="/parser/openapi.json" if production else "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/v1/get/pagasa")
def get_pagasa():
    url = os.getenv("SOURCE_URL_PAGASA")
    data = fetch_weather_outlook(url)
    return data

@app.get("/v1/get/doh")
def get_doh():
    url = os.getenv("SOURCE_URL_DOH")
    data = fetch_press_releases(url)
    return data

@app.get("/v1/get/phivolcs")
def get_phivolcs():
    url = os.getenv("SOURCE_URL_PHIVOLCS")
    data = fetch_volcano_bulletins(url)
    return data

@app.get("/v1/get/gmartv")
def get_gmartv():
    bucket = os.getenv("SOURCE_BUCKET_RTV")
    path = os.getenv("SOURCE_PATH_RTV")
    region = os.getenv("SOURCE_REGION_RTV")
    data = get_s3_file(bucket, path, region)
    return json.loads(data)

@app.get("/v1/parse/doh")
def parse_gmartv():
    url = os.getenv("SOURCE_URL_DOH")
    data = fetch_press_releases(url)
    read_data = data

    processedData = []
    for item in read_data['press_releases']:

        parsed_date = parse_date_time(trim_and_collapse_whitespace(item.get('publication_date', '')))
        philippine_tz = pytz.timezone('Asia/Manila')
        formatted_date = parsed_date.astimezone(philippine_tz).strftime('%b %d, %Y %I:%M %p')

        processedData.append({
            'id' : to_md5(trim_and_collapse_whitespace(item.get('publication_date', ''))),
            'title' : trim_and_collapse_whitespace(item.get('title', '')),
            'published_date' : formatted_date,
            'source' : 'doh'
        })

        data = save_parsed_data_to_s3('doh', processedData)

        return {
            "success" : True,
            "data" : data
        }
    
@app.get("/v1/parse/phivolcs")
def parse_phivolcs():
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

    data = save_parsed_data_to_s3('phivolcs', processedData)

    return {
        "success": True,
        "data": data
    }

@app.get("/v1/parse/pagasa")
def parse_pagasa():
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

    return {
        "success": True,
        "data": data
    }

@app.get("/v1/parse/gmartv")
def parse_rtv():
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

    return {
        "success": True,
        "data": data
    }
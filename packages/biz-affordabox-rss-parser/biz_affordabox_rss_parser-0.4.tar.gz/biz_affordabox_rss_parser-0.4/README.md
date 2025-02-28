# README
This repository offers a sample project structure for building and deploying AWS Lambda functions.
It includes tools to automate the packaging and deployment processes.
Each subdirectory within the project represents an individual Lambda function and can have its own set of Node.js / Python dependencies.

+ ROOT
|-+ package.json (project deploy tools)
|-+ build-project-package.js (project zip tools)
|-+ deploy_biz-affordabox-rss-parser-python.sh ( aws lambda function deploy script )
|
|--/biz-affordabox-rss-parser-python
|---+ lambda_function.py

# DEPENDENCIES
- aws cli 2.x
- aws credentials key with sufficient permissions
- node.js: module aarchiver
- python

# OTHER NOTES
- check current python verson and path
- check node.js version
- check current aws clli version

# AWS PERMISSIONS & ACCOUNTS NEEDED
- AWS Lambda Admin (Read/Write)
- Default AWS Credentials - tgmanetwork aws keys
- NOTE: Might need Other Project-Specific AWS Credentials
- !!! NEEDS AWS S3 Read / Update Credential Keys [default]
- !!! NEEDS AWS Lambda Read / Update Credential Keys [default-lambda]

# DEPENDENCIES: python

> python 3.10 +

> biz-affordabox-rss-parser (python)
>> boto3                             | This is built in AWS Lambda 
>> cloudscraper                      | used for extraction of web content
>> BeautifulSoup                     | used for html content parsing
>> pytz                              | used for timezone processing
>> python-dateutil                   | used for datetime processing

# DEPENDENCIES: node.js

> node.js 10.14

# INSTALL DEPENDENCIES - node.js

```bash
### USING nvm on to execute with specific node version 10.14.0
npm install --with=dev
```

# QUICK DEPLOY GUIDE
```bash
# Working Directory: ./biz-lambda-parsers

# Check Node and Python Versions
node -v
python3 --version

# !!! Ensure AWS Keys are prepared beforehand
[default]
aws_access_key_id=***
aws_secret_access_key=***
region=ap-southeast-1

[default-lambda]
aws_access_key_id=***
aws_secret_access_key=***
region=ap-southeast-1

# Execute Export Command For Default AWS CLI Keys
export SHARED_KEY_AWS_S3_ACCOUNT_ID=***
export SHARED_KEY_AWS_S3_ACCOUNT_SECRET=***
export SHARED_KEY_AWS_S3_REGION=ap-southeast-1

# Execute AWS Lambda Deploy Script
sh deploy_biz-affordabox-rss-parser-python.sh dev2 nodezip dependencies
```

# BUILD DEPLOY (LAMBDA Python)- biz-affordabox-rss-parser-python

> NOTE: Ensure *AWS Credential keys* is properly set-up (default-lambda)

> SHARED ENV VARS CREDENTIALS REFERENCE: http://km.gmanmi.com/display/SD/2.4.1.1.+AWS+Lambdas

```bash
### USING nvm on to execute with specific node version
###
### COMMAND contains 2 parts
### 1. export vars script - export vars need to be created beforehand
### 2. server script runner & command options

# -- DEV2 Marjon Environment
source /.h1de3nV/3nV/parsers/rnd_parsers/export-vars-parser-dev2-pytest.sh && sh server-deploy-lambda.sh pytest nodezip dependencies

# -- DEV2 Environment
source /.h1de3nV/3nV/parsers/rnd_parsers/export-vars-parser-dev2.sh && sh server-deploy-lambda.sh dev2 nodezip dependencies

# -- DEV Environment
source /.h1de3nV/3nV/parsers/rnd_parsers/export-vars-parser-dev.sh && sh server-deploy-lambda.sh dev nodezip dependencies

# -- TEST Environment
source /.h1de3nV/3nV/parsers/rnd_parsers/export-vars-parser-test.sh && sh server-deploy-lambda.sh test nodezip dependencies

# -- PREPROD ENVIRONMENT
source /.h1de3nV/3nV/parsers/rnd_parsers/export-vars-parser-preprod.sh && sh server-deploy-lambda.sh preprod nodezip dependencies

# -- PROD ENVIRONMENT
source /.h1de3nV/3nV/parsers/rnd_parsers/export-vars-parser-prod.sh && sh server-deploy-lambda.sh prod nodezip dependencies

# npm run deploy:affodabox_rss_python_prod
# npm run zip_deploy:affodabox_rss_python_prod
```

### LOCAL SERVER RUN - Affordabox RSS DOH Parser
```bash
# 1. Install Dependencies
sh server-install-python-deps.sh

# 2. Set Env Variable Exports
- dev2 environment or individual subfolders
- dev environment
- test environment
- regression environment
- preprod environment
- prod environment

# 3. Execute Parser Script in Server
source ./path/to/export-vars-parser-dev2-pytest.sh && sh server-run-*.sh

source ./path/to/export-vars-parser-dev2-pytest.sh && sh server-run-get-doh.sh
source ./path/to/export-vars-parser-dev2-pytest.sh && sh server-run-get-phivolcs.sh
source ./path/to/export-vars-parser-dev2-pytest.sh && sh server-run-get-pagasa.sh
source ./path/to/export-vars-parser-dev2-pytest.sh && sh server-run-get-gmartv.sh

source ./path/to/export-vars-parser-dev2-pytest.sh && sh server-run-parse-doh.sh
source ./path/to/export-vars-parser-dev2-pytest.sh && sh server-run-parse-phivolcs.sh
source ./path/to/export-vars-parser-dev2-pytest.sh && sh server-run-parse-pagasa.sh
source ./path/to/export-vars-parser-dev2-pytest.sh && sh server-run-parse-gmartv.sh
```
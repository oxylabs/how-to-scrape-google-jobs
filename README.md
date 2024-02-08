# How To Scrape Google Jobs

[![Oxylabs promo code](https://user-images.githubusercontent.com/129506779/250792357-8289e25e-9c36-4dc0-a5e2-2706db797bb5.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)

Learn how to build your own Google Jobs scraper that simultaneously scrapes Google Jobs for multiple search queries and geo-locations with Python and [Oxylabs’ Google Jobs Scraper API](https://oxylabs.io/products/scraper-api/serp/google/jobs).

## Google Jobs website overview

Once you visit the Google Jobs page, you'll see that all job listings for a query are displayed on the left side. Looking at the HTML structure, you can see that each listing is enclosed in the ```<li>``` tag and collectively wrapped within the ```<ul>``` tag:

[image]

In this guide, let’s scrape Google Jobs results asynchronously and extract the following publicly available data:

1. Job title
2. Company name
3. Job location
4. Job posted via *[platform]*
5. Job listing date
6. Salary

[image] 

If you want to extract even more public data, such as job highlights, job description, and similar jobs, expand the code shown in this article to make additional API calls to the scraped job URLs.

### 1. Get a free trial and send a request
<p>Visit the Oxylabs dashboard and create an account to claim your 1-week free trial for Google Jobs API, which is part of Oxylabs’ SERP Scraper API. It’s equipped with proxy servers, Headless Browser, Custom Parser, and other advanced features that’ll help you overcome blocks and fingerprinting. See this short guide that shows how to navigate the dashboard and get the free trial.</p>

#### Install Python
</p>If you don’t have Python installed yet, you can download it from the official Python website. This tutorial is written with Python 3.12.0, so ensure that you have a compatible version.</p>

#### Send a request for testing
</p>After creating an API user, copy and save your API user credentials, which you’ll use for authentication. Next, open your terminal and install the requests library:</p>

```pip install requests```

Then run the following code that scrapes Google Jobs results and retrieves the entire HTML file:

```import requests

payload = {
    "source": "google",
    "url": "https://www.google.com/search?q=developer&ibp=htl;jobs&hl=en&gl=us",
    "render": "html"
}

response = requests.post(
    "https://realtime.oxylabs.io/v1/queries",
    auth=("USERNAME", "PASSWORD"),	# Replace with your API user credentials
    json=payload
)
print(response.json())
print(response.status_code)
```
Once it finishes running, you should see a JSON response with HTML results and a status code of your request. If everything works correctly, the status code should be ```200```.

### 2. Install and import libraries

For this project, let’s use the asyncio and aiohttp libraries to make asynchronous requests to the API. Additionally, the json and pandas libraries will help you deal with JSON and CSV files. 

Open your terminal and run the following command to install the necessary libraries:

```pip install asyncio aiohttp pandas```

Then, import them into your Python file:

```import asyncio, aiohttp, json, pandas as pd
from aiohttp import ClientSession, BasicAuth
```

### 3. Add your API user credentials

Create the API user ```credentials``` variable and use ```BasicAuth```, as aiohttp requires this for authentication:

```credentials = BasicAuth("USERNAME", "PASSWORD") # Replace with your API user credentials```

### 4. Set up queries and locations

You can easily form Google Jobs URLs for different queries by manipulating the q= parameter:

```https://www.google.com/search?q=developer&ibp=htl;jobs&hl=en&gl=us```

This enables you to scrape job listings for as many search queries as you want. 

**Note** that the ```q=```, ```ibp=htl;jobs```, ```hl=```, and ```gl=``` parameters are mandatory for the URL to work.

Additionally, you could set the UULE parameter for geo-location targeting yourself, but that’s unnecessary since the geo_location parameter of Google Jobs Scraper API does that by default.

#### URL parameters

Create the URL_parameters list to store your search queries:

```URL_parameters = ["developer", "chef", "manager"]``` 

### Locations

Then, create the ```locations``` dictionary where the key refers to the country, and the value is a list of geo-location parameters. This dictionary will be used to dynamically form the API payload and localize Google Jobs results for the specified location. The two-letter country code will be used to modify the ```gl=``` parameter in the Google Jobs URL:

```locations = {
    "US": ["California,United States", "Virginia,United States", "New York,United States"],
    "GB": ["United Kingdom"],
    "DE": ["Germany"]
}
```

Visit our [documentation](https://developers.oxylabs.io/scraper-apis/serp-scraper-api/google?_gl=1*1ppa1cd*_gcl_au*MTcyMDU1MDYxNi4xNzA3MzkxNjU5#geo_location) for more details about geo-locations.

### 5. Prepare the API payload with parsing instructions

Google Jobs Scraper API takes web scraping instructions from a ```payload``` dictionary, making it the most important configuration to fine-tune. The ```url``` and ```geo_location``` keys are set to ```None```, as the scraper will pass these values dynamically for each search query and location. The ```"render": "html"``` parameter enables JavaScript rendering and returns the rendered HTML file:

```payload = {
    "source": "google",
    "url": None,
    "geo_location": None,
    "user_agent_type": "desktop",
    "render": "html"
}
```

Next, use [Custom Parser](https://developers.oxylabs.io/scraper-apis/custom-parser?_gl=1*ugfwm0*_gcl_au*MTcyMDU1MDYxNi4xNzA3MzkxNjU5) to define your own parsing logic with xPath or CSS selectors and retrieve only the data you need. Remember that you can create as many functions as you want and extract even more data points than shown in this guide. Head to this Google Jobs URL in your browser and open Developer Tools by pressing Ctrl+Shift+I (Windows) or Option + Command + I (macOS). Use Ctrl+F or Command+F to open a search bar and test selector expressions.

As mentioned previously, the job listings are within the <li> tags, which are wrapped with the <ul> tag:

[image]

As there is more than one ```<ul>``` list on the Google Jobs page, you can form an xPath selector by specifying the ```div``` element that contains the targeted list:

```//div[@class='nJXhWc']//ul/li```

You can use this selector to specify the location of all job listings in the HTML file. In the ```payload``` dictionary, set the ```parse``` key to ```True``` and create the ```parsing_instructions``` parameter with the jobs function:

```payload = {
    "source": "google",
    "url": None,
    "geo_location": None,
    "user_agent_type": "desktop",
    "render": "html",
    "parse": True,
    "parsing_instructions": {
        "jobs": {
            "_fns": [
                {
                    "_fn": "xpath",
                    "_args": ["//div[@class='nJXhWc']//ul/li"]
                }
            ],
        }
    }
}
```

Next, create the _items iterator that will loop over the jobs list and extract details for each listing:

```payload = {
    "source": "google",
    "url": None,
    "geo_location": None,
    "user_agent_type": "desktop",
    "render": "html",
    "parse": True,
    "parsing_instructions": {
        "jobs": {
            "_fns": [
                {
                    "_fn": "xpath", # You can use CSS or xPath
                    "_args": ["//div[@class='nJXhWc']//ul/li"]
                }
            ],
            "_items": {
                "data_point_1": {
                    "_fns": [
                        {
                            "_fn": "selector_type",  # You can use CSS or xPath
                            "_args": ["selector"]
                        }
                    ]
                },
                "data_point_2": {
                    "_fns": [
                        {
                            "_fn": "selector_type",
                            "_args": ["selector"]
                        }
                    ]
                },
            }
        }
    }
}
```

For each data point, you can create a separate function within the ```_items``` iterator. Let’s see how xPath selectors should look like for each Google Jobs data point:

### Job title

[image]

```.//div[@class='BjJfJf PUpOsf']/text()```

### Company name

[image]

```.//div[@class='vNEEBe']/text()```

### Location

[image]

```.//div[@class='Qk80Jf'][1]/text()```

### Date

[image]

```.//div[@class='PuiEXc']//span[@class='LL4CDc' and contains(@aria-label, 'Posted')]/span/text()```

### Salary

[image]

```.//div[@class='PuiEXc']//div[@class='I2Cbhb bSuYSc']//span[@aria-hidden='true']/text()```

### Job posted via

[image]

```.//div[@class='Qk80Jf'][2]/text()```

### URL

[image]

```.//div[@data-share-url]/@data-share-url```

**Please be aware** that you can only access this job listing URL in your browser with an IP address from the same country used during web scraping. If you’ve used a United States proxy, make sure to use a US IP address in your browser.

In the end, you should have a ```payload``` that looks like shown below. Save it to a separate JSON file and ensure that the ```None``` and ```True``` parameter values are converted to respective JSON values: ```null``` and ```true```:

```import json

payload = {
    "source": "google",
    "url": None,
    "geo_location": None,
    "user_agent_type": "desktop",
    "render": "html",
    "parse": True,
    "parsing_instructions": {
        "jobs": {
            "_fns": [
                {
                    "_fn": "xpath",
                    "_args": ["//div[@class='nJXhWc']//ul/li"]
                }
            ],
            "_items": {
                "job_title": {
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [".//div[@class='BjJfJf PUpOsf']/text()"]
                        }
                    ]
                },
                "company_name": {
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [".//div[@class='vNEEBe']/text()"]
                        }
                    ]
                },
                "location": {
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [".//div[@class='Qk80Jf'][1]/text()"]
                        }
                    ]
                },
                "date": {
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [".//div[@class='PuiEXc']//span[@class='LL4CDc' and contains(@aria-label, 'Posted')]/span/text()"]
                        }
                    ]
                },
                "salary": {
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [".//div[@class='PuiEXc']//div[@class='I2Cbhb bSuYSc']//span[@aria-hidden='true']/text()"]
                        }
                    ]
                },
                "posted_via": {
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [".//div[@class='Qk80Jf'][2]/text()"]
                        }
                    ]
                },
                "URL": {
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [".//div[@data-share-url]/@data-share-url"]
                        }
                    ]
                }
            }
        }
    }
}

with open("payload.json", "w") as f:
    json.dump(payload, f, indent=4)
```

This allows you to import the payload and make the scraper code much shorter:

```payload = {}
with open("payload.json", "r") as f:
    payload = json.load(f)
```

### 6. Define functions 

There are several ways you can [integrate](https://developers.oxylabs.io/scraper-apis/getting-started/integration-methods?_gl=1*bftxvn*_gcl_au*MTcyMDU1MDYxNi4xNzA3MzkxNjU5) Oxylabs Scraper APIs, namely Realtime, [Push-Pull](https://developers.oxylabs.io/scraper-apis/getting-started/integration-methods/push-pull?_gl=1*1lxuuik*_gcl_au*MTcyMDU1MDYxNi4xNzA3MzkxNjU5), and Proxy endpoint. For this guide, let’s use [Push-Pull](https://developers.oxylabs.io/scraper-apis/getting-started/integration-methods/push-pull?_gl=1*1j36jm8*_gcl_au*MTcyMDU1MDYxNi4xNzA3MzkxNjU5#batch-query), as you won’t have to keep your connection open after submitting a scraping job to the API. The API endpoint to use in this scenario is https://data.oxylabs.io/v1/queries.

You could also use another endpoint to submit batches of up to 1000 URLs or queries. Keep in mind that making this choice will require you to modify the code shown in this tutorial. Read up about batch queries in our documentation.

#### Submit job
Define an async function called submit_job and pass the session: ClientSession together with the payload to submit a web scraping job to the Oxylabs API using the POST method. This will return the ID number of the submitted job:





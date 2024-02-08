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

Google Jobs Scraper API takes web scraping instructions from a ```payload``` dictionary, making it the most important configuration to fine-tune. The ```url``` and ```geo_location``` keys are set to None, as the scraper will pass these values dynamically for each search query and location. The "render": "html" parameter enables JavaScript rendering and returns the rendered HTML file:

















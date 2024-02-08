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

1. 

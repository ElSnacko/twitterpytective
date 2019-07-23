
# Twitterpytective
> APIless historical tweet collector

Twitterpytective is a historical APIless Tweet collection wrapper. This library was created to avoid the cost of paying for Twitter's enterprise API and the finicking with the API restrictions while still having the capability to be able to access historical tweets from any search and save it to a csv.

## Installing / Getting started

The way to use the library is to download the raw file save it to your appropreiate sitepackage folder or in the local dir.

```shell
import twitterpytective as tp
#startdate and enddate needs to be in this format '2017-11-30'
browser =tp.browser(tpe.urlconfig([HASHTAG], [STARTDATE],[ENDDATE]))
tp.csver(tp.soupcollector(browser),'[NAMEOFCSV].csv')
```

Under the hood what happens is that with the use of web crawling and scrapping tools (Selenium & Bs4), a browser opens up then a scroll functions is activated to load the webpage fully (due to the infinite scroll) then the information is scrapped with Bs4.

## Features
* Csv creation of configurable time and search
* documents time, tweet, and picture presence notation

## Contributing
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome."

## Licensing

"The code in this project is licensed under MIT license."

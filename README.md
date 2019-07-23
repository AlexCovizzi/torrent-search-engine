# torrent-search-engine

Python library to search torrents from multiple websites.

# About
This Python library allows you to search torrents by scraping torrent websites.

You can add websites to scrape by providing a configuration file (see ... on how to create a configuration file).

# Usage

## Requirements
This library requires python 3.5 or higher.

## Installation
You can install this library from Github using this command:

```
$ pip install git+https://github.com/AlexCovizzi/torrent-search-engine
```

## Example

```python
from torrentsearchengine import TorrentSearchEngine

search_engine = TorrentSearchEngine()
# add torrent provider from a file or url
search_engine.add_provider(path)
# perform the query and find max 50 results
results = search_engine.search(query, limit=50)
# retrieve the magnet of the first result
magnet = results[0].fetch_magnet()
```

## Providers
You can add torrent providers from json files or an urls to a json file.

You can find an explained example of provider file in [this example](/examples/PROVIDER_EXAMPLE.md)

The torrent provider json file has the following structure:

- **name** _(required)_ - The name (and identifier) of the torrent provider.

- **fullname** _(optional)_ - The full name of the torrent provider, this is the diplayed name. Defaults to the **name**.
    
- **url** _(required)_ - The base url of the torrent provider.

- **headers** _(optional)_ - HTTP headers to use in the requests to this website.

- **search** _(required)_ - The search path relative to the base url.

- **whitespace** _(optional)_ - The whitespaces in the query are replaced with this character (by default they are replace with %20).
    
    The path needs to include the search query as a variable using the keyword: `{query}`.

- **list** _(required)_ - This property defines how to scrape the data from the torrent provider.

    It includes the following properties:

    - **items** _(required)_ - The CSS selector that selects all the torrent html elements (e.g the rows of a table).

    - **next** _(optional)_ - The CSS selector that selects the link to the next page.
    
    - **item** _(required)_ - This property defines the selectors to scrape the data from a the torrent html element.

        The attributes currently supported are:

        - **title** _(required)_ - Title of the torrent.
        - **url** _(optional)_ - Link to the page of the torrent.
        - **size** _(optional)_ - Size of the torrent.
        - **time** _(optional)_ - Time of the torrent.
        - **seeds** _(optional)_ - Number of seeders of this torrent (the selected value must be an **integer**).
        - **leechers** _(optional)_ - Number of leechers of this torrent (the selected value must be an **integer**).
        - **magnet** _(optional)_ - The torrent's magnet link.

        **Note**: The selector used to select the torrent data has the following structure:
        
        ```
        <CSS selector> @ <html attribute> | re: <regex matcher> | fmt: <regex formatter>
        ```
        The default html attribute is `text` (the inner text of the html element selected).

        The options `re` and `fmt` are optional, their job is to select only part of the text or format the text, you can use regex capturing groups in `re` and `fmt`.

- **item** _(optional)_ - This property defines how to scrape the data from the torrent page (the page linked by the **url** torrent attribute).

    It includes the following properties:

    - **magnet** _(optional)_ - The torrent's magnet link.
    
        (**Note**: you can define the magnet property here or in the **list.item** property)





This is an example of torrent provider configuration file to scrape this pages.

```html
https://cool-torrent-website.io/search?q=Big-Buck-Bunny-720p

<body>
    Cool Torrent Website
    <table class="tbl">
        <thead>
            <tr>
                <th>TITLE</th>
                <th>SIZE</th>
                <th>TIME</th>
                <th>S</th>
                <th>L</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><a href="/big-buck-bunny-1">Big Buck Bunny 720p - 1</a></td>
                <td>320MB</td>
                <td>yesterday</td>
                <td>20<span>^</span></td>
                <td><div class="l">12</div></td>
            <tr>
        </tbody>
    </table>
    <div class="pagination">
        <ul>
            <li class="active"><a href="/page_1">1</li>
            <li><a href="/page_2">2</li>
            <li><a href="/page_3">3</li>
        </ul>
    </div>
</body>


https://cool-torrent-website.io/big-buck-bunny-1

<body>
    <div class="magnet-section">
        <a href="magnet:...">Magnet here</a>
    </div>
</body>
```

And this is the configuration file:

```json
{
    "cool-torrent-website": {
        // base url of the website
        "url": "https://cool-torrent-website.io/",
        // {query} is the query variable
        "search": "/search?q={query}",
        // the wihitespaces in the query are replaced with '-'
        "whitespace": "-",
        "list": {
            "items": "table.tbl > tbody > tr",
            // link to the next page, we are selecting the li next to li.active
            "next": ".pagination > ul > li.active + li > a @ href",
            "item": {
                "title": "td:nth-of-type(1) > a @ text",
                // link to the torrent page
                "url": "td:nth-of-type(1) > a @ href",
                "size": "td:nth-of-type(2) @ text",
                "time": "td:nth-of-type(3) @ text",
                // we are interested only at the numbers, so we use the regex
                "seeds": "td:nth-of-type(4) @ text | re: [0-9]+",
                "leechers": "td.l"
            }
        },
        // since the magnet is in the torrent page we need to define this property
        "item": {
            "magnet": "div.magnet-section > a @ href"
        }
    }
}
```
# HEI scraper

<img src="https://www.heinetwork.tv/wp-content/uploads/2021/03/logo_block-1-rev.jpg" alt="HEI logo" width="300">

Hi guys, it's movie time!

This repo is the scraper responsible for getting data from the HEI Network website and others in order to create a full On Cinema timeline.

### Progress

- [x] On Cinema (show)
- [x] Decker
- [x] Automate creating one large combined json file in root of repo
- [x] On Cinema (podcast)
- [x] HEI Network News v1
- [ ] HEI Network News v2: Using the 'previous' button to go further back
- [ ] Updated data structure (see below)
- [ ] Non-scraped content, in the correct structure (for example the screening of Port of Call on YouTube)
- [ ] Automate checking

### Data structure

#### v1

```json
  {
    "show": "on_cinema",
    "media_type": "episode",
    "collection": "Season 15",
    "title": "'Valiant One' & 'Dog Man'",
    "description": null,
    "date_published": "2025-01-29T00:00:00",
    "url": "https://heinetwork.tv/episode/valiant-one-dog-man/",
    "poster_url": "https://www.heinetwork.tv/wp-content/uploads/2025/01/on_cinema_s15_ep06.png",
  },
```

#### v2

```json
  {
    "franchise": "on_cinema", // replacing 'show'
    "media_type": "episode", // Other options: Article, trailer, movie (for Mister America)
    "season_name": "Season 15",
    "season_number": "15", // useful for sorting, in particular the Decker seasons
    "title": "'Valiant One' & 'Dog Man'",
    "date_published": "2025-01-29T00:00:00",
    "published_by": null, // in the case of articles, we'll add the name
    "url": "https://heinetwork.tv/episode/valiant-one-dog-man/",
    "poster_url": "https://www.heinetwork.tv/wp-content/uploads/2025/01/on_cinema_s15_ep06.png",
    "is_bonus": "false", // to easily find if something is a 'bonus' bit of content
    "is_meta": "false", // to easily find if something is meta content, for example the wrap parties
  },
```

## Acknowledgements

This work wouldn't be possible without the amazing [On Cinema Timeline](https://oncinematimeline.com) website to use as a resource and as inspiration.

## Related repos

[HEI api](https://github.com/samcolson4/hei_api)

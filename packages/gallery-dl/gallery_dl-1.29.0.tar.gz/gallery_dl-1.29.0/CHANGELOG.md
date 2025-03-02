## 1.29.0 - 2025-03-01
### Changes
- build `gallery-dl.exe` on Windows 10 / Python 3.13 ([#6684](https://github.com/mikf/gallery-dl/issues/6684))
- provide Windows 7 / Python 3.8 builds as `gallery-dl_x86.exe`
### Extractors
#### Additions
- [bilibili] add `user-articles-favorite` extractor ([#6725](https://github.com/mikf/gallery-dl/issues/6725) [#6781](https://github.com/mikf/gallery-dl/issues/6781))
- [boosty] add `direct-messages` extractor ([#6768](https://github.com/mikf/gallery-dl/issues/6768))
- [discord] add support ([#454](https://github.com/mikf/gallery-dl/issues/454) [#6836](https://github.com/mikf/gallery-dl/issues/6836) [#7059](https://github.com/mikf/gallery-dl/issues/7059) [#7067](https://github.com/mikf/gallery-dl/issues/7067))
- [furry34] add support ([#1078](https://github.com/mikf/gallery-dl/issues/1078) [#7018](https://github.com/mikf/gallery-dl/issues/7018))
- [hentaiera] add support ([#3046](https://github.com/mikf/gallery-dl/issues/3046) [#6952](https://github.com/mikf/gallery-dl/issues/6952) [#7020](https://github.com/mikf/gallery-dl/issues/7020))
- [hentairox] add support ([#7003](https://github.com/mikf/gallery-dl/issues/7003))
- [imgur] add support for personal posts ([#6990](https://github.com/mikf/gallery-dl/issues/6990))
- [imhentai] add support ([#1660](https://github.com/mikf/gallery-dl/issues/1660) [#3046](https://github.com/mikf/gallery-dl/issues/3046) [#3824](https://github.com/mikf/gallery-dl/issues/3824) [#4338](https://github.com/mikf/gallery-dl/issues/4338) [#5936](https://github.com/mikf/gallery-dl/issues/5936))
- [tiktok] add support ([#3061](https://github.com/mikf/gallery-dl/issues/3061) [#4177](https://github.com/mikf/gallery-dl/issues/4177) [#5646](https://github.com/mikf/gallery-dl/issues/5646) [#6878](https://github.com/mikf/gallery-dl/issues/6878) [#6708](https://github.com/mikf/gallery-dl/issues/6708))
- [vsco] support `/video/` URLs ([#4295](https://github.com/mikf/gallery-dl/issues/4295) [#6973](https://github.com/mikf/gallery-dl/issues/6973))
#### Fixes
- [bunkr] decrypt file URLs ([#7058](https://github.com/mikf/gallery-dl/issues/7058) [#7070](https://github.com/mikf/gallery-dl/issues/7070) [#7085](https://github.com/mikf/gallery-dl/issues/7085) [#7089](https://github.com/mikf/gallery-dl/issues/7089) [#7090](https://github.com/mikf/gallery-dl/issues/7090))
- [chevereto/jpgfish] fix extraction ([#7073](https://github.com/mikf/gallery-dl/issues/7073) [#7079](https://github.com/mikf/gallery-dl/issues/7079))
- [generic] fix config lookups by subcategory
- [philomena] fix `date` values without UTC offset ([#6921](https://github.com/mikf/gallery-dl/issues/6921))
- [philomena] download `full` URLs to prevent potential 404 errors ([#6922](https://github.com/mikf/gallery-dl/issues/6922))
- [pixiv] prevent exceptions during `comments` extraction ([#6965](https://github.com/mikf/gallery-dl/issues/6965))
- [reddit] restrict subreddit search results ([#7025](https://github.com/mikf/gallery-dl/issues/7025))
- [sankaku] fix extraction ([#7071](https://github.com/mikf/gallery-dl/issues/7071) [#7072](https://github.com/mikf/gallery-dl/issues/7072))
- [subscribestar] fix `post` extractor ([#6582](https://github.com/mikf/gallery-dl/issues/6582))
- [twitter] revert generated CSRF token length to 32 characters ([#6895](https://github.com/mikf/gallery-dl/issues/6895))
- [vipergirls] change default `domain` to `viper.click` ([#4166](https://github.com/mikf/gallery-dl/issues/4166))
- [weebcentral] fix extracting wrong number of chapter pages ([#6966](https://github.com/mikf/gallery-dl/issues/6966))
#### Improvements
- [b4k] update domain to `arch.b4k.dev` ([#6955](https://github.com/mikf/gallery-dl/issues/6955) [#6956](https://github.com/mikf/gallery-dl/issues/6956))
- [bunkr] update default archive ID format ([#6935](https://github.com/mikf/gallery-dl/issues/6935))
- [bunkr] provide fallback URLs for 403 download links ([#6732](https://github.com/mikf/gallery-dl/issues/6732) [#6972](https://github.com/mikf/gallery-dl/issues/6972))
- [bunkr] implement fast `--range` support ([#6985](https://github.com/mikf/gallery-dl/issues/6985))
- [furaffinity] use a default delay of 1 second between requests ([#7054](https://github.com/mikf/gallery-dl/issues/7054))
- [itaku] support gallery section URLs ([#6951](https://github.com/mikf/gallery-dl/issues/6951))
- [patreon] support `/profile/creators` URLs
- [subscribestar] detect and handle redirects ([#6916](https://github.com/mikf/gallery-dl/issues/6916))
- [twibooru] match URLs with `www` subdomain ([#6903](https://github.com/mikf/gallery-dl/issues/6903))
- [twitter] support `grok` cards content ([#7040](https://github.com/mikf/gallery-dl/issues/7040))
- [vsco] improve `m3u8` handling
- [weibo] add `movies` option ([#6988](https://github.com/mikf/gallery-dl/issues/6988))
#### Metadata
- [bunkr] extract `id_url` metadata ([#6935](https://github.com/mikf/gallery-dl/issues/6935))
- [erome] extract `tags` metadata ([#7076](https://github.com/mikf/gallery-dl/issues/7076))
- [issuu] unescape HTML entities
- [newgrounds] provide `comment_html` metadata ([#7038](https://github.com/mikf/gallery-dl/issues/7038))
- [patreon] extract `campaign` metadata ([#6989](https://github.com/mikf/gallery-dl/issues/6989))
### Downloaders
- implement `downloader` options per extractor category
- [http] add `sleep-429` option ([#6996](https://github.com/mikf/gallery-dl/issues/6996))
- [ytdl] support specifying `module` as filesystem paths ([#6991](https://github.com/mikf/gallery-dl/issues/6991))
### Archives
- [archive] implement support for PostgreSQL databases ([#6152](https://github.com/mikf/gallery-dl/issues/6152))
- [archive] add `archive-table` option ([#6152](https://github.com/mikf/gallery-dl/issues/6152))
### Miscellaneous
- [aes] handle errors during `cryptodome` import ([#6906](https://github.com/mikf/gallery-dl/issues/6906))
- [executables] fix loading `certifi` SSL certificates ([#6393](https://github.com/mikf/gallery-dl/issues/6393))
- improve `\f` format string handling for `--print`

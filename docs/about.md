# About

## Caveats / Disclaimer

DeviantArt's history as a website is storied. Prior to the release of Eclipse, there were two options with creating tooling around its UI:
- The [Public DeviantArt API](https://www.deviantart.com/developers/). See [accompanying Python wrapper](https://pypi.org/project/deviantart/). The API is relatively easy to use - and utilizes OAuth2 for authentication - but its endpoints and functionality are sparce. It also was not updated for some time but now appears to be getting a handful of new endpoints based on the changelog.
- The internal [DeviantArt Interactive Fragment Interface (DiFi)](https://github.com/danopia/deviantart-difi/wiki). DiFi has a wide range of functionality but is volatile/unreliable and difficult to use - especially compared to modern APIs.

On October 2019, DeviantArt announced [DeviantArt Eclipse](https://www.deviantart.com/team/journal/DeviantArt-Eclipse-is-Here-814629875), a new UI (mostly) built in React. There are still a handful of pages on the website that expose the old website (i.e. https://www.deviantart.com/groups/) where functionality hasn't been completely ported. But with the new React UI brought along a third option for tooling:
- The internal **DeviantArt NAPI**, currently undocumented. The structure of its endpoints resembles RESTful practices, and authentication is done through scraping a CSRF token on the website or using a user's stored `.deviantart.com` cookies.

The implementation in this library relies on the DeviantArt NAPI. As such, functionality may break without warning depending on whether the internal DeviantArt team makes changes to these endpoints.
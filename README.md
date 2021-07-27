# dAEclipse
`daeclipse` is a Python library for DeviantArt Eclipse functionality.

This repo also contains a handy CLI to expose and test `daeclipse` capabilities.

```bash
python3 cli.py --help
```
```
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

  DeviantArt Eclipse CLI

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  add-art-to-groups  Submit DeviantArt deviation to groups.
  gif-preset         Generate an animated pixel icon gif based on a stored preset.
  gif-random         Generate an animated pixel icon gif with randomized assets.
```

## Installation

```bash
python3 -m pip install daeclipse
```

## Usage

```py
import daeclipse

# Fetches a list of group names the user is a member of.
# You will need to be logged into DeviantArt and have a chrome page open.
eclipse = daeclipse.Eclipse()
groups, has_more, next_offset, total = eclipse.get_groups("Pepper-Wood", 0)
for group in groups:
    print(group.username)
```

## Caveats / Disclaimer

DeviantArt's history as a website is storied. Prior to the release of Eclipse, there were two options with creating tooling around its UI:
- The [Public DeviantArt API](https://www.deviantart.com/developers/). See [accompanying Python wrapper](https://pypi.org/project/deviantart/). The API is relatively easy to use - and utilizes OAuth2 for authentication - but its endpoints and functionality are sparce. It also was not updated for some time but now appears to be getting a handful of new endpoints based on the changelog.
- The internal [DeviantArt Interactive Fragment Interface (DiFi)](https://github.com/danopia/deviantart-difi/wiki). DiFi has a wide range of functionality but is volatile/unreliable and difficult to use - especially compared to modern APIs.

On October 2019, DeviantArt announced [DeviantArt Eclipse](https://www.deviantart.com/team/journal/DeviantArt-Eclipse-is-Here-814629875), a new UI (mostly) built in React. There are still a handful of pages on the website that expose the old website (i.e. https://www.deviantart.com/groups/) where functionality hasn't been completely ported. But with the new React UI brought along a third option for tooling:
- The internal **DeviantArt NAPI**, currently undocumented. The structure of its endpoints resembles RESTful practices, and authentication is done through scraping a CSRF token on the website or using a user's stored `.deviantart.com` cookies.

The implementation in this library relies on the DeviantArt NAPI. As such, functionality may break without warning depending on whether the internal DeviantArt team makes changes to these endpoints.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

## License
[MIT](https://github.com/Pepper-Wood/daeclipse/blob/main/LICENSE)

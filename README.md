# MitzyBanana
![](https://github.com/Pepper-Wood/MitzyBanana/workflows/Pylint/badge.svg)
A set of tools to automate a DeviantArt adoptable account.

Color Palette reference: https://lospec.com/palette-list/juice-56

# Future ideas with no clear implementation flowchart
These will eventually be added to a Milestone. Not sure how to add them to the issues queue without cluttering at the moment.
- A way to preview what the array of colors for skin/hair/eyes are so that it's easier for me to add new palettes
  - Live preview would be dope too, but that strays into JavaScript territory
  - Maybe this means moving the colors files to a separate location. When a new palette is added, a command is run to generate the RGB values and store in separate file. This would speed up the recoloring process, instead of needing to reconvert the hex values to RGB every time.
- Resulting image will have the gif resized to twice its size with a crop of a painted headshot
- The ability to generate multiple of these side-by-side (while still saving these files as separates)
- Add Mitzy watermark over the enlarged gif
- Ability to send in config file or config arguments to force generate the resulting sprite

# Notes about da-groups.py
## Fetching group and folder ids for json file
### folder_id
In the folder's url, the number in it is the folder_id.
i.e. given https://www.deviantart.com/all-things-cute/gallery/, getting the link for "Pixel Art" is https://www.deviantart.com/all-things-cute/gallery/63180664/pixel-art
folder_id = 63180664

### group_id
Go into the page source of the group and search for gruser_id. The number that succeeds is the group_id. i.e. view sourcing https://www.deviantart.com/all-things-cute
group_id = 14718292

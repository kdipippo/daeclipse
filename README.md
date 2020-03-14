# MitzyBanana
A set of tools to automate a DeviantArt adoptable account.

Color Palette reference: https://lospec.com/palette-list/juice-56

# Next Steps
✅ Fix bug where skin tones in the eye layer aren't being recolored.
✅ Add a different type of hairstyle that can be randomly selected.
⚪ Add watermark
⚪ Add a different type of outfit that can be randomly selected.
⚪ Make gif transparent
✅ Reorganize files in test/ to be better scalable
⚪ Add background option (sparkles, hearts, win95 window)

# Future ideas with no clear implementation flowchart
- A way to preview what the array of colors for skin/hair/eyes are so that it's easier for me to add new palettes
  - Live preview would be dope too, but that strays into JavaScript territory
  - Maybe this means moving the colors files to a separate location. When a new palette is added, a command is run to generate the RGB values and store in separate file. This would speed up the recoloring process, instead of needing to reconvert the hex values to RGB every time.
- Resulting image will have the gif resized to twice its size with a crop of a painted headshot
- The ability to generate multiple of these side-by-side (while still saving these files as separates)
- Add Mitzy watermark over the enlarged gif
- Ability to send in config file or config arguments to force generate the resulting sprite

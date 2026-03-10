# LaunchLED mini

tool to draw gifs and png:s (and maybe other image file formats) onto a novation launchpad mini mk1...

the original launchpad mini has a very limited colour range, with it only having red and green LED:s and those only having a certain amount of possible 'lightness', as in light level.

this probably works with other launchpad models, but expect the colours to be wacky...

optional arguments:

`-fps` the fps to run the gif at

`-m` or `--mode` colour mode, options are 'red', 'green' 'yellow', and 'full', defaults to 'full'

usage:

basic gif drawing works as such: `python main.py ~/path/to/file.gif`

if, for example, you want to run the gif at 20fps, and only using yellow as the colour, the command would be `python main.py ~/path/to/file.gif -fps 20 -m yellow`

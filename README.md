# reddit-spotlight

Use Reddit to download images and prepare them for wallpaper and
lockscreen usage. The objective is to provide an experience similar
to Microsoft Spotlight on linux.

## i3lock-color

To use with i3lock-color, please use the following options:

```
i3lock \
	--ignore-empty-password \
	--image $(find /usr/local/share/spotlight-from-reddit/lock -maxdepth 1 -name "*.jpg" | shuf -n1) \
	--force-clock --indicator \
	--ind-pos="x+470:y+h-106" --radius 48 --ring-width=4 \
	--inside-color=00000000 --ring-color=ffffff90 --keyhl-color=ffffffc0 --line-uses-inside \
	--insidever-color=00000000 --ringver-color=0000ff80 \
	--insidewrong-color=00000000 --ringwrong-color=ff000080 \
	--time-pos="x+240:y+h-103" --time-color="e8e8e8e0" --time-size=60\
	--date-str="%A %-d %B %Y" --date-pos="tx:ty+40" --date-color="e8e8e8e0" --date-size=25 \
	--pass-media-keys --pass-screen-keys --pass-volume-keys \
	--verif-text="" --wrong-text="" --noinput-text=""
```

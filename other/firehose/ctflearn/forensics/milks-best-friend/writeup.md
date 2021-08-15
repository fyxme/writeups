1. Run `binwalk -e oreo.jpg` to extract rar folder from image
2. Unrar archive
3. `strings b.jpg | grep flag` returns flag: `flag{eat_more_oreos}`

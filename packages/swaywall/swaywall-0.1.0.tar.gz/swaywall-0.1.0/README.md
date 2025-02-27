## Swaywall

An intelligent wallpaper switcher for `swaywm`.

+ Sets a random wallpaper from a given directory
+ Remembers previous selections:
	- Never repeats a wallpaper until the entire catalogue has been cycled through
	- Can restore the latest selection (useful on `swaywm` start)

---

``` 
usage: swaywall [-h] [-r] dir

positional arguments:
  dir            path to wallpaper directory

options:
  -h, --help     show this help message and exit
  -r, --restore  restore latest wallpaper
```

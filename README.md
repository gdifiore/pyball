# `pyball`

**Mostly-finished** Library for grabbing baseball statistics in python

## Why `pyball`

Another python library for getting baseball statistics already exists ([pybaseball](https://github.com/jldbc/pybaseball)), however, pyball just provides barebones functions for retriving stats from Baseball-Reference, and Baseball Savant.

## Requirements
- Python 3(.8)

## Install/Build From Source
```
pip install --user --upgrade setuptools

cd pyball

setup.py install
```

## Tutorials

Read the [wiki](https://github.com/SummitCode/pyball/wiki) for tutorials on using pyball. **Updated version coming soon**

## Credits

`playerid_lookup.py` by [James LeDoux](https://github.com/jldbc/pybaseball) (MIT License)

## Comments and Suggestions
Leave any comments or suggestions in [an issue](https://github.com/SummitCode/pyball/issues/new) or directly make make [a pull request](https://github.com/SummitCode/pyball/compare) adding code.

## License

`pyball` is licensed under the [MIT license](https://github.com/SummitCode/pyball/blob/master/LICENSE)

## TODO
- find a way to cache websites vistied by Selenium (just for the day, because data is updated everyday during the baseball season)
- only use selenium for tables updated by js (Savant's #detailedPitches)
- update documentation
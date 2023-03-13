# `pyball`

Library for grabbing baseball statistics in Python, designed for use in Jupyter Notebooks.

## Why `pyball`

Another python library for getting baseball statistics already exists ([pybaseball](https://github.com/jldbc/pybaseball)), however, pyball just provides barebones functions for retriving stats from Baseball-Reference, and Baseball Savant.

## Requirements
- Python 3(.8)

## Install/Build From Source
Some manual install work is needed temporarily, navigate to the `chromedriver` [download page](https://chromedriver.chromium.org/downloads). This is needed for `selenium` (an explanation can be found in `utils.py`, or just trust that it works).

Add this `exe` to your Windows `PATH` or MacOS/Linux `$PATH`, and proceed with the install.

```
pip install --user --upgrade setuptools

cd pyball

setup.py install
```

## Docs

Read the [docs](https://gdifiore.github.io/pyball/docs/pyball/index.html) for function descriptions.

For examples, look at my [MLBResearch Repo](https://github.com/gdifiore/MLBResearch/blob/main/Parse_BBRef_Table/bbref_table.ipynb) where I test most of the functions.

## Credits

`playerid_lookup.py` by [James LeDoux](https://github.com/jldbc/pybaseball) (MIT License)

## Comments and Suggestions
Leave any comments or suggestions in [an issue](https://github.com/SummitCode/pyball/issues/new) or directly make make [a pull request](https://github.com/SummitCode/pyball/compare) adding code.

## License

`pyball` is licensed under the [MIT license](https://github.com/SummitCode/pyball/blob/master/LICENSE)

## TODO
- update documentation
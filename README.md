# pyball

Library for grabbing baseball statistics in Python, designed for use in Jupyter Notebooks.

## Why `pyball`

Another python library for getting baseball statistics already exists ([pybaseball](https://github.com/jldbc/pybaseball)), however, pyball just provides barebones functions for retriving stats from Baseball-Reference, and Baseball Savant.

## Install/Build From Source
```
git clone https://github.com/gdifiore/pyball.git

cd pyball

python -m venv .venv

(activate .venv)

poetry install
```

## Samples
Read the sample [jupyter notebook](https://gdifiore.github.io/pyball/examples/pyball_tutorial.html).

## Comments and Suggestions
Leave any comments or suggestions in [an issue](https://github.com/SummitCode/pyball/issues/new) or directly make make [a pull request](https://github.com/SummitCode/pyball/compare) adding code.

## License

`pyball` is licensed under the [MIT license](https://github.com/SummitCode/pyball/blob/master/LICENSE)

## To-do
- Would like to make a base class of shared functions (_get_soup(), _find_table(), ...) but I kinda hate how python classes work.

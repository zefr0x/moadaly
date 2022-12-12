# Contributing

## Bug report
For now [GitHub bug traker](https://github.com/zer0-x/moadaly/issues) is used for this project.

If you find a wrong behaviour in the calculation, please open an issue to discuss it. You can then implement a fix if you want or just wait for someone else to do it.

We aim to be user friendly, so if you have any issue or suggestion for the [UI](https://en.wikipedia.org/wiki/User_interface_design)/[UX](https://en.wikipedia.org/wiki/User_experience_design) or about the [application packing](https://en.wikipedia.org/wiki/Package_(package_management_system)), please tell us, we appreciate it.

If your school/university uses a strange calculation system that is not supported by the program, please open a issue with some useful resources and ideas for how to implement it.

## Development
- The 3rd version of the [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) programming language is used mainly in this project.
- Dependencies managment is handled using [requirements files](requirements) with [pip-tools](https://pip-tools.rtfd.io/).
    - `requirements.in` contain requirements for running the application and `requirements-dev.in` contain requirements for development.
    - `.txt` files are locked requirements with hashes generated using `pip-tools` to provide a reproducible environment.
    - For development you will need to use both files, while users just need to use the `requirements.txt` file.

>    `pre-commit` will take care about generating `.txt` files. You should just edit `.in` files or use `pip-tools` to upgrade locked requirements.

### Create a virtual environment and install dependencies
First clone the git repository:
```
git clone https://github.com/zer0-x/moadaly.git
```

For development you are recomended to use [pip-tools](https://pip-tools.rtfd.io/) for reproducing the same environment.
1. Create a virtual environment and activate it
```shell
virtualenv .env

source .env/bin/activate
```
2. Install `pip-tools` in the virtualenv
```shell
pip install pip-tools
```
3. Run the folowing command in the project's root directory to install all the dependencies for development
```shell
pip-sync requirements/{requirements,requirements-dev}.txt
```
4. Then you can run the application as a python module
```shell
python3 -m moadaly
```

### Style
- You should [type hint](https://docs.python.org/3/library/typing.html) every thing as possible.
- You should comment every thing to keep the code easy to read. Every file, every class, every function and any line that need a comment.

You should use:
- [mypy](http://www.mypy-lang.org/) `(Static Type Checker)`
- [flake8](https://flake8.pycqa.org/) `(Style Enforcer)`
- [pydocstyle](https://www.pydocstyle.org/) `(Checking compliance with Python docstring conventions)`
- [black](https://black.readthedocs.io/) `(Code Formatter)`

You can also use any tool that you want as long as it's compatable with the required ones.

#### Installing `pre-commit`
To make every thing easy [**`pre-commit`**](https://pre-commit.com/) is used in this project, it should run in every commit, so you shouldn't commit any thing without checking it first.

First install it:
```shell
pip install pre-commit
```

> You can use another way to install it, maybe from your OS's package manager.


Then add it as a git hook while you are inside the repository:
```shell
pre-commit install
```

## Translation
The application's GUI is prepared for [internationalisation](https://en.wikipedia.org/wiki/Internationalization_and_localization), but I didn't set it up yet.

For now you have two files to translate:
- [`io.github.zer0_x.moadaly.desktop`](https://github.com/zer0-x/moadaly/blob/main/io.github.zer0_x.moadaly.desktop)
- [`io.github.zer0_x.moadaly.metainfo.xml`](https://github.com/zer0-x/moadaly/blob/main/io.github.zer0_x.moadaly.metainfo.xml)

### Translating the application name
The name of the application can be written with different letters from your language, but it must be the same word and with the same Arabic pronunciation.

If you are able to write the application name with your language letters to match the Arabic pronunciation then do it, but if you can't just use the name that is written with english letters.
To listen to the Arabic pronunciation, just copy the Arabic name from the README.md page and paste it into Google Translate or any similar program.

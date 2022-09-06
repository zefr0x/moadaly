# Moadaly | مُعَدَّلِي
A **feature-rich** and **user friendly** [Linux](https://en.wikipedia.org/wiki/Linux) [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface) desktop application for calculating the [GPA](https://en.wikipedia.org/wiki/Grade_point_average) and other related stuff, for every student.

## Features
- 🧾 Free software under the [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html) licence.
- 🗃️ Create multible profiles and switch between them in the fly, to manage multible separate CGPAs.
- 💾 All your data are saved localy, so you can always go back and modify them as you progrees in your studies.
- 📤 Export & 📥 Import, so you can easly transform data to another device or create a backup. `(import functionality is not yet implemented)`
- 💯 Every known grading or calculating system is supported. `(only few are implemented for now)`
- 🧮 A dynamic grades panel for semesters and ther courses.
- 🧰 Some extra tools thet may help you in your calculation. `(Only one tool is avialable, yet)`
- 📊 Some charts to make you understand your grades better. `(Not yet implemented)`
- 🖨️ PDF reports. `(Not yet implemented)`


## Installation
### Flatpak
Not available yet...
### AppImage
Not available yet...
### AUR
Not available yet...
### pypi <sup>`(Not recomended)`</sup>
Not available yet...
### From the git repo <sup>`(Not recomended)`</sup> 
1. Clone the repo from github and cd to it
```shell
git clone https://github.com/zer0-x/moadaly.git
cd modaly
```
2. Use the `setup.py` file to install it
```shell
python3 setup.py install
```
> You can create a virtual environment before that if you wanted.
3. Now it should be in your path. Just type `moadaly` to run the GUI
```shell
moadaly
```

## Development
For development you are recomended to use [Pipenv](https://pipenv.pypa.io) for reproducing the same environment.
1. Install pipenv if you  don't have it
```shell
python3 -m pip install pipenv
```
2. Run the folowing command in the project's root directory to install all the dependencies form `Pipfile.lock`
```shell
pipenv install --dev
# Don't use the `--dev` flag to not install the development packages
```
3. Then you can activate the virtual environment and run the application as a python module
```shell
pipenv shell
python3 -m moadaly
```

## Contribution
If you find a wrong behaviour in the calculation, please open an issue to discuss it. You can then implement a fix if you want or just wait for someone to do it.

We aim to be user friendly, so if you have any issue or suggestion for the [UI](https://en.wikipedia.org/wiki/User_interface_design)/[UX](https://en.wikipedia.org/wiki/User_experience_design) or about the [application packing](https://en.wikipedia.org/wiki/Package_(package_management_system)), please tell us, we appreciate it.

If your school/university uses a strange calculation system that is not supported by the program, please open a issue with some useful resources and ideas for how to implement it.

If you want to contribute but you can't do those things, you can just spread the program to people and direct your friends and those you know to use it. This may be the most useful thing to do.

## Troubleshooting
If you got some issues with the PySide6 module that prevent the app from starting, try running:
```shell
python3 -m pip install --force-reinstall --no-cache-dir PySide6
```

## Q&A

Q: What does `Moadaly` mean?
- It is an Arabic word `مُعَدَّلِي` that could be translated to `My GPA` in english.

# Moadaly
A **feature-rich** Qt6 application to calculate the grade point average and other related stuff for university students.

## Features
- 🧾 Free software under the [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html) licence.
- 🗃️ Create multible profiles and switch between them in the fly, to manage multible CGPAs.
- 💾 All data are saved in a database to be loaded in the next session.
- 📤 Export & 📥 Import database data to a json file. `(import functionality is not yet implemented)`
- 5️⃣ point scale & 4️⃣ point scale systems are both supported. `(4 point scale is not yet implemented)`
- 💯 Both grading systems, noramel and curve are supported. `(curve system is not yet implemented)`
- 🧮 A dynamic grades panel for semesters and ther courses.
- 🧰 Some extra tools thet may help you in your calculation. `(Not yet implemented)`
- 📊 Some charts to make you understand your grades better. `(Not yet implemented)`
- 🖨️ Printable reports. `(Not yet implemented)`
- 🔐 Database encreption. `(Under thought, may or may not be implemented)`


## Installation
### Flatpak
Not available yet...
### AppImage
Not available yet...
### AUR
Not available yet...
### pypi
Not available yet...
### From the git repo
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

## Troubleshooting
If you got some issues with the PySide6 module that prevent the app from starting, try running:
```shell
python3 -m pip install --force-reinstall --no-cache-dir PySide6
```

## Q&A

Q: What does `Moadaly` mean?
- It is an Arabic word `مُعَدَّلِي` that could be translated to `My GPA` in english.

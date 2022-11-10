# Unreleased

# 0.1.0-alpha.2
## Added
    - Implement database features.
        - Now you can create and delete profiles.
        - You can switch between profiles in the fly.
        - Calculation settings are getting pulled from the database.
        - Creation of new semester and courses will be pushed to the database.
        - When deleting profile or semester ther childs will be deleting as will.
        - When updating course data, they will be updated in the database as will.
        - Every time you open a profile, it's data will be loaded to the GUI.
        - Now an action is available in the profile menu to export database to a json file.
    - The app's entry point exit is now in the __main__.py file.
    - `setup.py` file is now available to easily install the app.

# 0.1.0-alpha.1
- First alpha release.
- Database related features are not yet implemented, the calculation just works, and the data are in memory while the app is running.

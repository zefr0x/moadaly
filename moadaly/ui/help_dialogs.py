"""Some help dialogs."""

from gettext import gettext as _

from PySide6 import QtCore, QtGui, QtWidgets

from moadaly.__about__ import APP_VERSION

about_text = _(
    """\
<b>Moadaly</b> is a <b>feature-rich</b> and <b>user-friendly</b> Linux desktop
<b>GUI</b> application for calculating the <b>GPA</b> and other related stuff,
for every student.
<br><br>
Project Maintainers:
<ul>
<li>zer0-x</li>
</ul>\
""",
)

license_text = _(
    """\
Copyright (C) Moadaly
<br>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3
as published by the Free Software Foundation.
<br><br>
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
<br><br>
You should have received a copy of the GNU General Public License
along with this program.
If not, see <a href="https://www.gnu.org/licenses/">https://www.gnu.org/licenses/</a>.\
""",
)


class About(QtWidgets.QDialog):
    """Dialog for some information about the application."""

    def __init__(self) -> None:
        """Initialize main components of the dialog."""
        super().__init__()

        self.setMinimumSize(400, 600)
        self.setWindowTitle(_("About"))

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addSpacing(10)

        title_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(title_layout)

        title_layout.addStretch()

        logo = QtWidgets.QLabel()
        logo.setPixmap(
            QtGui.QIcon().fromTheme("io.github.zer0_x.moadaly").pixmap(64, 64),
        )
        title_layout.addWidget(logo)

        title = QtWidgets.QLabel(_("Moadaly <sup>{0}</sup>").format(APP_VERSION))
        title_font = QtGui.QFont()
        title_font.setPointSize(30)
        title_font.setBold(True)
        title.setFont(title_font)
        title_layout.addWidget(title)

        title_layout.addStretch()

        main_layout.addSpacing(10)

        tabs = QtWidgets.QTabWidget()
        main_layout.addWidget(tabs)

        main_about = QtWidgets.QTextEdit(about_text)
        main_about.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.LinksAccessibleByKeyboard
            | QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse
            | QtCore.Qt.TextInteractionFlag.TextBrowserInteraction,
        )

        tabs.addTab(main_about, _("About"))

        gpl3_license = QtWidgets.QTextEdit(license_text)
        gpl3_license.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.LinksAccessibleByKeyboard
            | QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse
            | QtCore.Qt.TextInteractionFlag.TextBrowserInteraction,
        )
        tabs.addTab(gpl3_license, _("License"))

        close_button = QtWidgets.QPushButton(_("Close"))
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button)

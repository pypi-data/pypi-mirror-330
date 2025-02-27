from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QSize,
    Qt,
)

from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QButtonGroup,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)
from . import resources_1_rc


class Ui_Arduino_GetData_W(object):
    def setupUi(self, Arduino_GetData_W):
        if not Arduino_GetData_W.objectName():
            Arduino_GetData_W.setObjectName("Arduino_GetData_W")
        Arduino_GetData_W.resize(545, 355)
        Arduino_GetData_W.setStyleSheet(
            "QComboBox QAbstractItemView {\n"
            "    background-color: rgb(77, 77, 77);\n"
            "}\n"
            "\n"
            "QComboBox QAbstractItemView::item:focus{\n"
            "    background-color: rgb(140, 140, 140);\n"
            "}\n"
            "\n"
            "QDoubleSpinBox{\n"
            "	background-color: rgb(77, 77, 77);\n"
            "	\n"
            "	border-top: 1.5px solid rgb(46, 46, 46);\n"
            "	border-left: 1.5px solid rgb(46, 46, 46);\n"
            "\n"
            "	border-bottom: 1.5px solid rgb(166, 166, 166);\n"
            "	border-right: 1.5px solid rgb(166, 166, 166);\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::up-button{\n"
            "    image: url(:/imgs/imgs/drop_up_arrow.png);\n"
            "	width: 11px;\n"
            "\n"
            "	background-color: rgb(0, 79, 0);\n"
            "	border-top: 1.5px solid rgb(127, 167, 127);\n"
            "	border-left: 1.5px solid rgb(127, 167, 127);\n"
            "\n"
            "	border-bottom: 1.5px solid rgb(0, 0, 0);\n"
            "	border-right: 1.5px solid rgb(0, 0, 0);\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::up-button:pressed{\n"
            "	border: 2px solid rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::up-button:hover{\n"
            "	background-color: rgb(0, 50, 0);\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::down-button{\n"
            ""
            "    image: url(:/imgs/imgs/drop_down_arrow.png);\n"
            "	width: 11px;\n"
            "\n"
            "	background-color: rgb(0, 79, 0);\n"
            "	border-top: 1.5px solid rgb(127, 167, 127);\n"
            "	border-left: 1.5px solid rgb(127, 167, 127);\n"
            "\n"
            "	border-bottom: 1.5px solid rgb(0, 0, 0);\n"
            "	border-right: 1.5px solid rgb(0, 0, 0);\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::down-button:pressed{\n"
            "	border: 2px solid rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::down-button:hover{\n"
            "	background-color: rgb(0, 50, 0);\n"
            "}\n"
            "\n"
            "QWidget#Arduino_GetData_W{\n"
            "	background-color: rgb(64, 64, 64);\n"
            "}\n"
            "\n"
            "QWidget{\n"
            "	color: rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QComboBox{\n"
            "	background-color: rgb(77, 77, 77);\n"
            "	\n"
            "	border-top: 1.5px solid rgb(46, 46, 46);\n"
            "	border-left: 1.5px solid rgb(46, 46, 46);\n"
            "\n"
            "	border-bottom: 1.5px solid rgb(166, 166, 166);\n"
            "	border-right: 1.5px solid rgb(166, 166, 166);\n"
            "}\n"
            "\n"
            "\n"
            "QComboBox::drop-down{\n"
            "	image: url(:/imgs/imgs/drop_down_arrow.png);\n"
            "	width: 11px;\n"
            "\n"
            "	backgr"
            "ound-color: rgb(0, 79, 0);\n"
            "	border-top: 2px solid rgb(127, 167, 127);\n"
            "	border-left: 2px solid rgb(127, 167, 127);\n"
            "\n"
            "	border-bottom: 2px solid rgb(0, 0, 0);\n"
            "	border-right: 2px solid rgb(0, 0, 0);\n"
            "}\n"
            "\n"
            "QComboBox::drop-down:hover{\n"
            "	background-color: rgb(0, 50, 0);\n"
            "}\n"
            "\n"
            "QComboBox::drop-down:pressed{\n"
            "	border: 2px solid rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QPushButton{\n"
            "	background-color: rgb(0, 79, 0);\n"
            "\n"
            "	border-top: 1.5px solid rgb(127, 167, 127);\n"
            "	border-left: 1.5px solid rgb(127, 167, 127);\n"
            "\n"
            "	border-bottom: 1.5px solid rgb(0, 0, 0);\n"
            "	border-right: 1.5px solid rgb(0, 0, 0);\n"
            "\n"
            "	\n"
            '	font: 12pt "Helvetica";\n'
            "	text-align:center;\n"
            "}\n"
            "\n"
            "QWidget{\n"
            '	font: 12pt "Helvetica";\n'
            "}\n"
            "\n"
            "QPushButton:hover{\n"
            "	background-color: rgb(0, 50, 0);\n"
            "}\n"
            "\n"
            "QPushButton:pressed{\n"
            "	border: 2px solid rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QLineEdit{\n"
            "	background-color: rgb(77, 77, 77);\n"
            "	border-top: 1.5px solid rgb(46, 4"
            "6, 46);\n"
            "	border-left: 1.5px solid rgb(46, 46, 46);\n"
            "\n"
            "	border-bottom: 1.5px solid rgb(166, 166, 166);\n"
            "	border-right: 1.5px solid rgb(166, 166, 166);\n"
            "}\n"
            "\n"
            "QRadioButton::indicator{\n"
            "	border-radius: 6px;\n"
            "	border-top: 1.5px solid rgb(0, 0, 0);\n"
            "	border-left: 1.5px solid rgb(0, 0, 0);\n"
            "\n"
            "	border-bottom: 1.5px solid rgb(160, 160, 160);\n"
            "	border-right: 1.5px solid rgb(160, 160, 160);\n"
            "}\n"
            "\n"
            "QRadioButton::indicator::checked{\n"
            "	background-color: white;\n"
            "}\n"
            "\n"
            "QRadioButton::indicator::unchecked:hover{\n"
            "	background-color: #9F9F9F;\n"
            "}\n"
            "\n"
            "QRadioButton::indicator::pressed{\n"
            "	border: 1.5px solid #505050\n"
            "}\n"
            "\n"
            "QPushButton#reload_devices{\n"
            "	image: url(:/imgs/imgs/reload.png);\n"
            "	width: 11px;\n"
            "	background-color: rgb(0, 79, 0);\n"
            "\n"
            "	border-top: 1.5px solid rgb(127, 167, 127);\n"
            "	border-left: 1.5px solid rgb(127, 167, 127);\n"
            "\n"
            "	border-bottom: 1.5px solid rgb(0, 0, 0);\n"
            "	border-right: 1.5px solid rgb(0, 0, 0);\n"
            "\n"
            "	\n"
            ""
            '	font: 12pt "Helvetica";\n'
            "	text-align:center;\n"
            "}\n"
            "\n"
            "QPushButton#reload_devices:hover{\n"
            "	background-color: rgb(0, 50, 0);\n"
            "}\n"
            "\n"
            "QPushButton#reload_devices:pressed{\n"
            "	border: 2px solid rgb(255, 255, 255);\n"
            "}"
        )
        self.verticalLayout = QVBoxLayout(Arduino_GetData_W)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QWidget(Arduino_GetData_W)
        self.widget.setObjectName("widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.device_combo = QComboBox(self.widget_2)
        self.device_combo.setObjectName("device_combo")
        self.device_combo.setMinimumSize(QSize(0, 22))
        self.device_combo.setMaximumSize(QSize(16777215, 22))

        self.gridLayout_3.addWidget(self.device_combo, 0, 0, 1, 1)

        self.reload_devices = QPushButton(self.widget_2)
        self.reload_devices.setObjectName("reload_devices")
        self.reload_devices.setMinimumSize(QSize(22, 22))
        self.reload_devices.setMaximumSize(QSize(22, 22))

        self.gridLayout_3.addWidget(self.reload_devices, 0, 1, 1, 1)

        self.gridLayout.addWidget(self.widget_2, 0, 2, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.label_7.setMinimumSize(QSize(0, 30))
        self.label_7.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)

        self.widget_7 = QWidget(self.widget)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout = QHBoxLayout(self.widget_7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.yes_plot_radio = QRadioButton(self.widget_7)
        self.plot_radio_group = QButtonGroup(Arduino_GetData_W)
        self.plot_radio_group.setObjectName("plot_radio_group")
        self.plot_radio_group.addButton(self.yes_plot_radio)
        self.yes_plot_radio.setObjectName("yes_plot_radio")
        self.yes_plot_radio.setChecked(True)

        self.horizontalLayout.addWidget(self.yes_plot_radio)

        self.no_plot_radio = QRadioButton(self.widget_7)
        self.plot_radio_group.addButton(self.no_plot_radio)
        self.no_plot_radio.setObjectName("no_plot_radio")

        self.horizontalLayout.addWidget(self.no_plot_radio)

        self.gridLayout.addWidget(self.widget_7, 3, 2, 1, 1, Qt.AlignLeft)

        self.widget_9 = QWidget(self.widget)
        self.widget_9.setObjectName("widget_9")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.path_line_edit = QLineEdit(self.widget_9)
        self.path_line_edit.setObjectName("path_line_edit")
        self.path_line_edit.setMinimumSize(QSize(0, 22))
        self.path_line_edit.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_3.addWidget(self.path_line_edit, 0, Qt.AlignVCenter)

        self.path_folder_browse = QPushButton(self.widget_9)
        self.path_folder_browse.setObjectName("path_folder_browse")
        self.path_folder_browse.setMinimumSize(QSize(0, 30))
        self.path_folder_browse.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_3.addWidget(self.path_folder_browse, 0, Qt.AlignVCenter)

        self.gridLayout.addWidget(self.widget_9, 5, 2, 1, 1)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.label_4.setMinimumSize(QSize(0, 30))
        self.label_4.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.label_6.setMinimumSize(QSize(0, 30))
        self.label_6.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName("label_8")
        self.label_8.setMinimumSize(QSize(0, 30))
        self.label_8.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.label_8, 5, 0, 1, 1)

        self.line = QFrame(self.widget)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 0, 1, 6, 1)

        self.widget_5 = QWidget(self.widget)
        self.widget_5.setObjectName("widget_5")
        self.gridLayout_6 = QGridLayout(self.widget_5)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.Ts_in = QDoubleSpinBox(self.widget_5)
        self.Ts_in.setObjectName("Ts_in")
        self.Ts_in.setMinimumSize(QSize(0, 22))
        self.Ts_in.setMaximumSize(QSize(16777215, 22))
        self.Ts_in.setDecimals(4)
        self.Ts_in.setMaximum(999.990000000000009)
        self.Ts_in.setSingleStep(0.010000000000000)
        self.Ts_in.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.Ts_in.setValue(0.500000000000000)

        self.gridLayout_6.addWidget(self.Ts_in, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.widget_5, 1, 2, 1, 1)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.label_5.setMinimumSize(QSize(0, 30))
        self.label_5.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.widget_8 = QWidget(self.widget)
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.yes_save_radio = QRadioButton(self.widget_8)
        self.save_radio_group = QButtonGroup(Arduino_GetData_W)
        self.save_radio_group.setObjectName("save_radio_group")
        self.save_radio_group.addButton(self.yes_save_radio)
        self.yes_save_radio.setObjectName("yes_save_radio")
        self.yes_save_radio.setChecked(True)

        self.horizontalLayout_2.addWidget(self.yes_save_radio)

        self.no_save_radio = QRadioButton(self.widget_8)
        self.save_radio_group.addButton(self.no_save_radio)
        self.no_save_radio.setObjectName("no_save_radio")

        self.horizontalLayout_2.addWidget(self.no_save_radio)

        self.gridLayout.addWidget(self.widget_8, 4, 2, 1, 1, Qt.AlignLeft)

        self.widget_6 = QWidget(self.widget)
        self.widget_6.setObjectName("widget_6")
        self.gridLayout_7 = QGridLayout(self.widget_6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.sesh_dur_in = QDoubleSpinBox(self.widget_6)
        self.sesh_dur_in.setObjectName("sesh_dur_in")
        self.sesh_dur_in.setMinimumSize(QSize(0, 22))
        self.sesh_dur_in.setMaximumSize(QSize(16777215, 22))
        self.sesh_dur_in.setDecimals(4)
        self.sesh_dur_in.setMaximum(86400.990000000005239)
        self.sesh_dur_in.setSingleStep(0.010000000000000)
        self.sesh_dur_in.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.sesh_dur_in.setValue(10.000000000000000)

        self.gridLayout_7.addWidget(self.sesh_dur_in, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.widget_6, 2, 2, 1, 1)

        self.verticalLayout.addWidget(self.widget)

        self.line_2 = QFrame(Arduino_GetData_W)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.start_get_data = QPushButton(Arduino_GetData_W)
        self.start_get_data.setObjectName("start_get_data")
        self.start_get_data.setMinimumSize(QSize(0, 30))
        self.start_get_data.setMaximumSize(QSize(16777215, 30))
        self.start_get_data.setStyleSheet("")

        self.verticalLayout.addWidget(self.start_get_data, 0, Qt.AlignHCenter)

        self.retranslateUi(Arduino_GetData_W)

        QMetaObject.connectSlotsByName(Arduino_GetData_W)

    # setupUi

    def retranslateUi(self, Arduino_GetData_W):
        Arduino_GetData_W.setWindowTitle(
            QCoreApplication.translate("Arduino_GetData_W", "Form", None)
        )
        # if QT_CONFIG(tooltip)
        self.reload_devices.setToolTip(
            QCoreApplication.translate(
                "Arduino_GetData_W",
                "<html><head/><body><p>Update COM ports</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.reload_devices.setText("")
        self.label.setText(
            QCoreApplication.translate(
                "Arduino_GetData_W", "Choose your arduino:", None
            )
        )
        self.label_7.setText(
            QCoreApplication.translate("Arduino_GetData_W", "Save data?", None)
        )
        self.yes_plot_radio.setText(
            QCoreApplication.translate("Arduino_GetData_W", "Yes", None)
        )
        self.no_plot_radio.setText(
            QCoreApplication.translate("Arduino_GetData_W", "No", None)
        )
        self.path_folder_browse.setText(
            QCoreApplication.translate("Arduino_GetData_W", " Browse ", None)
        )
        self.label_4.setText(
            QCoreApplication.translate("Arduino_GetData_W", "Sample period (s)", None)
        )
        self.label_6.setText(
            QCoreApplication.translate("Arduino_GetData_W", "Plot data?", None)
        )
        self.label_8.setText(
            QCoreApplication.translate("Arduino_GetData_W", "Path", None)
        )
        self.label_5.setText(
            QCoreApplication.translate(
                "Arduino_GetData_W", "Session duration (s)", None
            )
        )
        self.yes_save_radio.setText(
            QCoreApplication.translate("Arduino_GetData_W", "Yes", None)
        )
        self.no_save_radio.setText(
            QCoreApplication.translate("Arduino_GetData_W", "No", None)
        )
        self.start_get_data.setText(
            QCoreApplication.translate("Arduino_GetData_W", " GET DATA ", None)
        )

    # retranslateUi

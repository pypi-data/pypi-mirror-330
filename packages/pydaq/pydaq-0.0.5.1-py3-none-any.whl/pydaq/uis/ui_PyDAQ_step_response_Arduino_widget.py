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
    QWidget,
)
from . import resources_1_rc


class Ui_Arduino_StepResponse_W(object):
    def setupUi(self, Arduino_StepResponse_W):
        if not Arduino_StepResponse_W.objectName():
            Arduino_StepResponse_W.setObjectName("Arduino_StepResponse_W")
        Arduino_StepResponse_W.resize(603, 401)
        Arduino_StepResponse_W.setStyleSheet(
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
            "QWidget#Arduino_StepResponse_W{\n"
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
            "	b"
            "ackground-color: rgb(0, 79, 0);\n"
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
            "	border-top: 1.5px solid rgb("
            "46, 46, 46);\n"
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
            ""
            "	\n"
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
        self.gridLayout_3 = QGridLayout(Arduino_StepResponse_W)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.widget = QWidget(Arduino_StepResponse_W)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_14 = QLabel(self.widget)
        self.label_14.setObjectName("label_14")

        self.gridLayout_2.addWidget(self.label_14, 3, 0, 1, 1)

        self.label_9 = QLabel(self.widget)
        self.label_9.setObjectName("label_9")
        self.label_9.setMinimumSize(QSize(0, 30))
        self.label_9.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_2.addWidget(self.label_9, 4, 0, 1, 1)

        self.widget_10 = QWidget(self.widget)
        self.widget_10.setObjectName("widget_10")
        self.gridLayout_8 = QGridLayout(self.widget_10)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.sesh_dur_in = QDoubleSpinBox(self.widget_10)
        self.sesh_dur_in.setObjectName("sesh_dur_in")
        self.sesh_dur_in.setMinimumSize(QSize(0, 22))
        self.sesh_dur_in.setMaximumSize(QSize(16777215, 22))
        self.sesh_dur_in.setDecimals(4)
        self.sesh_dur_in.setMaximum(86400.990000000005239)
        self.sesh_dur_in.setSingleStep(0.010000000000000)
        self.sesh_dur_in.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.sesh_dur_in.setValue(10.000000000000000)

        self.gridLayout_8.addWidget(self.sesh_dur_in, 0, 0, 1, 1)

        self.gridLayout_2.addWidget(self.widget_10, 2, 3, 1, 1)

        self.widget_11 = QWidget(self.widget)
        self.widget_11.setObjectName("widget_11")
        self.gridLayout_9 = QGridLayout(self.widget_11)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.Ts_in = QDoubleSpinBox(self.widget_11)
        self.Ts_in.setObjectName("Ts_in")
        self.Ts_in.setMinimumSize(QSize(0, 22))
        self.Ts_in.setMaximumSize(QSize(16777215, 22))
        self.Ts_in.setDecimals(4)
        self.Ts_in.setMaximum(999.990000000000009)
        self.Ts_in.setSingleStep(0.010000000000000)
        self.Ts_in.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.Ts_in.setValue(0.500000000000000)

        self.gridLayout_9.addWidget(self.Ts_in, 0, 0, 1, 1)

        self.gridLayout_2.addWidget(self.widget_11, 1, 3, 1, 1)

        self.widget_15 = QWidget(self.widget)
        self.widget_15.setObjectName("widget_15")
        self.gridLayout_12 = QGridLayout(self.widget_15)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.step_on_s_in = QDoubleSpinBox(self.widget_15)
        self.step_on_s_in.setObjectName("step_on_s_in")
        self.step_on_s_in.setMinimumSize(QSize(0, 22))
        self.step_on_s_in.setMaximumSize(QSize(16777215, 22))
        self.step_on_s_in.setMaximum(999.990000000000009)
        self.step_on_s_in.setSingleStep(0.010000000000000)
        self.step_on_s_in.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.step_on_s_in.setValue(3.000000000000000)

        self.gridLayout_12.addWidget(self.step_on_s_in, 0, 0, 1, 1)

        self.gridLayout_2.addWidget(self.widget_15, 3, 3, 1, 1)

        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName("label_10")
        self.label_10.setMinimumSize(QSize(0, 30))
        self.label_10.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_2.addWidget(self.label_10, 2, 0, 1, 1)

        self.widget_12 = QWidget(self.widget)
        self.widget_12.setObjectName("widget_12")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_12)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.yes_save_radio = QRadioButton(self.widget_12)
        self.save_radio_group = QButtonGroup(Arduino_StepResponse_W)
        self.save_radio_group.setObjectName("save_radio_group")
        self.save_radio_group.addButton(self.yes_save_radio)
        self.yes_save_radio.setObjectName("yes_save_radio")
        self.yes_save_radio.setChecked(True)

        self.horizontalLayout_5.addWidget(self.yes_save_radio)

        self.no_save_radio = QRadioButton(self.widget_12)
        self.save_radio_group.addButton(self.no_save_radio)
        self.no_save_radio.setObjectName("no_save_radio")

        self.horizontalLayout_5.addWidget(self.no_save_radio)

        self.gridLayout_2.addWidget(self.widget_12, 5, 3, 1, 1, Qt.AlignLeft)

        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName("label_11")
        self.label_11.setMinimumSize(QSize(0, 30))
        self.label_11.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_2.addWidget(self.label_11, 5, 0, 1, 1)

        self.label_12 = QLabel(self.widget)
        self.label_12.setObjectName("label_12")
        self.label_12.setMinimumSize(QSize(0, 30))
        self.label_12.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_2.addWidget(self.label_12, 6, 0, 1, 1, Qt.AlignVCenter)

        self.widget_13 = QWidget(self.widget)
        self.widget_13.setObjectName("widget_13")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_13)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.yes_plot_radio = QRadioButton(self.widget_13)
        self.plot_radio_group = QButtonGroup(Arduino_StepResponse_W)
        self.plot_radio_group.setObjectName("plot_radio_group")
        self.plot_radio_group.addButton(self.yes_plot_radio)
        self.yes_plot_radio.setObjectName("yes_plot_radio")
        self.yes_plot_radio.setChecked(True)

        self.horizontalLayout_6.addWidget(self.yes_plot_radio)

        self.no_plot_radio = QRadioButton(self.widget_13)
        self.plot_radio_group.addButton(self.no_plot_radio)
        self.no_plot_radio.setObjectName("no_plot_radio")

        self.horizontalLayout_6.addWidget(self.no_plot_radio)

        self.gridLayout_2.addWidget(self.widget_13, 4, 3, 1, 1, Qt.AlignLeft)

        self.line_2 = QFrame(self.widget)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_2, 0, 2, 7, 1)

        self.widget_16 = QWidget(self.widget)
        self.widget_16.setObjectName("widget_16")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_16)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.path_line_edit = QLineEdit(self.widget_16)
        self.path_line_edit.setObjectName("path_line_edit")
        self.path_line_edit.setMinimumSize(QSize(0, 22))
        self.path_line_edit.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_7.addWidget(self.path_line_edit, 0, Qt.AlignVCenter)

        self.path_folder_browse = QPushButton(self.widget_16)
        self.path_folder_browse.setObjectName("path_folder_browse")
        self.path_folder_browse.setMinimumSize(QSize(0, 30))
        self.path_folder_browse.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_7.addWidget(self.path_folder_browse, 0, Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.widget_16, 6, 3, 1, 1)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.label_2.setMinimumSize(QSize(0, 30))
        self.label_2.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.device_combo = QComboBox(self.widget_3)
        self.device_combo.setObjectName("device_combo")
        self.device_combo.setMinimumSize(QSize(0, 22))
        self.device_combo.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_8.addWidget(self.device_combo)

        self.reload_devices = QPushButton(self.widget_3)
        self.reload_devices.setObjectName("reload_devices")
        self.reload_devices.setMinimumSize(QSize(22, 22))
        self.reload_devices.setMaximumSize(QSize(22, 22))

        self.horizontalLayout_8.addWidget(self.reload_devices)

        self.gridLayout_2.addWidget(self.widget_3, 0, 3, 1, 1)

        self.label_15 = QLabel(self.widget)
        self.label_15.setObjectName("label_15")
        self.label_15.setMinimumSize(QSize(0, 30))
        self.label_15.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_2.addWidget(self.label_15, 1, 0, 1, 1)

        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)

        self.line_3 = QFrame(Arduino_StepResponse_W)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line_3, 1, 0, 1, 1)

        self.start_step_response = QPushButton(Arduino_StepResponse_W)
        self.start_step_response.setObjectName("start_step_response")
        self.start_step_response.setMinimumSize(QSize(130, 30))
        self.start_step_response.setMaximumSize(QSize(130, 30))

        self.gridLayout_3.addWidget(
            self.start_step_response, 2, 0, 1, 1, Qt.AlignHCenter
        )

        self.retranslateUi(Arduino_StepResponse_W)

        QMetaObject.connectSlotsByName(Arduino_StepResponse_W)

    # setupUi

    def retranslateUi(self, Arduino_StepResponse_W):
        Arduino_StepResponse_W.setWindowTitle(
            QCoreApplication.translate("Arduino_StepResponse_W", "Form", None)
        )
        self.label_14.setText(
            QCoreApplication.translate("Arduino_StepResponse_W", "Step ON (s)", None)
        )
        self.label_9.setText(
            QCoreApplication.translate("Arduino_StepResponse_W", "Plot data?", None)
        )
        self.label_10.setText(
            QCoreApplication.translate(
                "Arduino_StepResponse_W", "Session duration (s)", None
            )
        )
        self.yes_save_radio.setText(
            QCoreApplication.translate("Arduino_StepResponse_W", "Yes", None)
        )
        self.no_save_radio.setText(
            QCoreApplication.translate("Arduino_StepResponse_W", "No", None)
        )
        self.label_11.setText(
            QCoreApplication.translate("Arduino_StepResponse_W", "Save data?", None)
        )
        self.label_12.setText(
            QCoreApplication.translate("Arduino_StepResponse_W", "Path", None)
        )
        self.yes_plot_radio.setText(
            QCoreApplication.translate("Arduino_StepResponse_W", "Yes", None)
        )
        self.no_plot_radio.setText(
            QCoreApplication.translate("Arduino_StepResponse_W", "No", None)
        )
        self.path_folder_browse.setText(
            QCoreApplication.translate("Arduino_StepResponse_W", " Browse ", None)
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "Arduino_StepResponse_W", "Choose your arduino:", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.reload_devices.setToolTip(
            QCoreApplication.translate(
                "Arduino_StepResponse_W",
                "<html><head/><body><p>Update COM ports</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.reload_devices.setText("")
        self.label_15.setText(
            QCoreApplication.translate(
                "Arduino_StepResponse_W", "Sample period (s)", None
            )
        )
        self.start_step_response.setText(
            QCoreApplication.translate("Arduino_StepResponse_W", "STEP RESPONSE", None)
        )

    # retranslateUi

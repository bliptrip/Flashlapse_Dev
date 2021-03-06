# import basic libraries
import sys
import time

#import settings
import Settings

# import custom functions
import Commands
import Threads
import Functions
import Call_Thread

# import UI functions
import UI_Update

# import Qt content
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

# import generated UI
import FlashLapse_UI

#global variables
default_dir = "/home/pi/Desktop"
date = time.strftime('%m_%d_%Y')

# create class for Raspberry Pi GUI


class MainWindow(QMainWindow, FlashLapse_UI.Ui_MainWindow):
 # access variables inside of the UI's file

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file
        Settings.init(self)
        Commands.startup()

        fh = open("../_temp/save_data.txt", "r")
        self.Email_lineEdit.setText(fh.readline())
        fh.close
        Settings.email = self.Email_lineEdit.text()

        self.Start_spinBox.valueChanged.connect(
            lambda: UI_Update.LED_validate(self))
        self.End_spinBox.valueChanged.connect(
            lambda: UI_Update.LED_validate(self))

        self.lightConfirm_pushButton.clicked.connect(
            lambda: Commands.light_confirm(self))
        self.lightReset_pushButton.clicked.connect(
            lambda: Commands.light_reset(self))

        self.disco_pushButton.clicked.connect(lambda: Commands.disco_run(self))
        self.rainbow_pushButton.clicked.connect(
            lambda: Commands.rainbow_run(self))
        self.sundial_pushButton.clicked.connect(
            lambda: Commands.sundial_run(self))
        self.pulse_pushButton.clicked.connect(lambda: Commands.pulse_run(self))

        self.confirmCycle_pushButton.clicked.connect(
            lambda: Call_Thread.start_cycle(self))

        self.schedulerTest_pushButton.clicked.connect(
            lambda: Call_Thread.schedule_test(self))
        self.schedulerSet_pushButton.clicked.connect(
            lambda: Call_Thread.schedule_run(self))
        self.motorSpeed_slider.valueChanged.connect(
            lambda: Commands.motorSliderChange(self))
        self.motorSpeed_slider.sliderReleased.connect(
            lambda: Commands.motorSliderRelease(self))

        self.clinostatSet_pushButton.clicked.connect(
            lambda: Commands.clinoStart(self))
        self.snapshot_pushButton.clicked.connect(
            lambda: Call_Thread.start_snapshot(self))
        self.liveFeed_pushButton.clicked.connect(
            lambda: Call_Thread.start_livefeed(self))
        self.preview_pushButton.clicked.connect(
            lambda: Call_Thread.start_preview(self))

        self.rotate_pushButton.clicked.connect(
            lambda: Call_Thread.rotate_image(self))

        self.xAxis_horizontalSlider.valueChanged.connect(
            lambda: Functions.zoomSliderChange(self))
        self.xAxis_horizontalSlider.sliderReleased.connect(
            lambda: Call_Thread.start_snapshot(self))

        self.yAxis_horizontalSlider.valueChanged.connect(
            lambda: Functions.zoomSliderChange(self))
        self.yAxis_horizontalSlider.sliderReleased.connect(
            lambda: Call_Thread.start_snapshot(self))

        self.motorConfirm_pushButton.clicked.connect(
            lambda: Commands.motor_rotate(self.motor_spinBox.value()))

        self.imageTitle_lineEdit.textChanged.connect(
            lambda: Functions.IST_Edit(self))
        self.addDate_pushButton.clicked.connect(
            lambda: Functions.add_date(self))
        self.ImageInterval_spinBox.valueChanged.connect(
            lambda: Functions.ICI_Change(self))
        self.imageDuration_spinBox.valueChanged.connect(
            lambda: Functions.ISD_Change(self))
        self.directory_pushButton.clicked.connect(
            lambda: Functions.select_directory(self))
        
        self.cloudType_ComboBox.currentIndexChanged.connect(
            lambda i: Functions.CloudTypeCombo_Change(self,i))
        self.cloudSettings_stackedWidget.currentChanged.connect(
            lambda i: Functions.CloudSettingsStacked_Change(self,i))

        self.Email_lineEdit.textChanged.connect(
            lambda: Functions.Email_Change(self))
        self.emailConfirm_pushButton.clicked.connect(
            lambda: Functions.Email_Entered(self))
        self.emailDefault_pushButton.clicked.connect(
            lambda: Functions.Save_Email(self))


        cyverse_data_path = "../_temp/.cyverse_data.txt"
        try:
            with open(cyverse_data_path, "r") as fh:
                Settings.cyverseUsername = fh.readline().strip('\n')
                self.cyverseUsername_lineEdit.setText(Settings.cyverseUsername)
                Settings.cyversePassword = fh.readline().strip('\n')
                self.cyversePassword_lineEdit.setText(Settings.cyversePassword)
                fh.close()
        except FileNotFoundError:
            pass
        self.cyverseUsername_lineEdit.textChanged.connect(
            lambda t: Functions.CyverseUsername_Change(self, t))
        self.cyversePassword_lineEdit.textChanged.connect(
            lambda t: Functions.CyversePassword_Change(self, t))
        self.cyverseConfirm_pushButton.clicked.connect(
            lambda: Functions.Cyverse_Confirm(self))
        self.cyverseDefault_pushButton.clicked.connect(
            lambda: Functions.Cyverse_Save(self))

        self.storage_tabWidget.currentChanged.connect(
            lambda: UI_Update.validate_input(self))
        self.startRoutines_pushButton.clicked.connect(
            lambda: Call_Thread.start_sequence(self))

        self.JPG_radioButton.toggled.connect(
            lambda: Functions.img_format(self))
        self.PNG_radioButton.toggled.connect(
            lambda: Functions.img_format(self))

        self.lightingPreset_pushButton.clicked.connect(
            lambda: Functions.start_lighting_preset(self))
        self.MotionPreset_pushButton.clicked.connect(
            lambda: Call_Thread.start_motion_preset(self))


# main function
def main():
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()

    # without this, the script exits immediately.
    sys.exit(app.exec_())


# python bit to figure how who started This
if __name__ == "__main__":
    main()

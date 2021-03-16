from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import json
import sys
import os

from rclpy.node import Node
from rclpy import node
import rclpy
import demjson

from DynamicPatternTOP import DynamicPatternTOP
from pattern_interfaces.srv import PassData
from Ui_MainWindow import Ui_MainWindow

        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.row_total = int(self.ui.tableWidget.rowCount())  # 當前行數
        
        self.pattern_api = DynamicPatternTOP()
        self.res_length = int(self.ui.lineEdit_length.text())
        self.res_width = int(self.ui.lineEdit_width.text())

        for i in range(self.row_total):
            self.comboBox = QtWidgets.QComboBox()
            self.comboBox.addItem("circle")
            self.comboBox.addItem("square")
            self.ui.tableWidget.setCellWidget(i, 0, self.comboBox)

        self.cross_line = "False"
        self.btn_connect()

    def btn_connect(self):
        self.ui.open_btn.clicked.connect(lambda:self.send_re(self.get_data_from_tabelwidget()))
        self.ui.action_save.triggered.connect(self.save_json)
        self.ui.action_import.triggered.connect(self.import_json)
        self.ui.cross_line_click.stateChanged.connect(self.cross_line_checkbox)

    def get_data_from_tabelwidget(self):
        self.circle_data_dict_total = {}
        radius = 0
        for i in range(self.row_total):
            self.circle_data_dict = {}
            self.shape_value_at_tablewidget = self.ui.tableWidget.cellWidget(i, 0)
            self.radius_value_at_tablewidget = self.ui.tableWidget.item(i, 1)
            self.color_value_at_tablewidget = self.ui.tableWidget.item(i, 2)
            self.position_value_at_tablewidget = self.ui.tableWidget.item(i, 3)
            if (self.radius_value_at_tablewidget is not None and self.radius_value_at_tablewidget.text() != '') and (self.color_value_at_tablewidget is not None and self.radius_value_at_tablewidget.text() != ''):  # 判斷空格是否為空的

                if self.shape_value_at_tablewidget is not None and self.radius_value_at_tablewidget.text() != '':
                    self.circle_data_dict.setdefault("shape", str(self.shape_value_at_tablewidget.currentText()))

                if self.radius_value_at_tablewidget is not None and self.radius_value_at_tablewidget.text() != '':
                    radius += int(self.radius_value_at_tablewidget.text())
                    self.circle_data_dict.setdefault("radius", int(self.radius_value_at_tablewidget.text()))

                if self.color_value_at_tablewidget is not None and self.color_value_at_tablewidget.text() != '':
                    color = list(map(int, self.color_value_at_tablewidget.text().split(',')))
                    self.circle_data_dict.setdefault("color", color)

                if self.position_value_at_tablewidget is not None and self.position_value_at_tablewidget.text() != '':
                    position = list(map(int, self.position_value_at_tablewidget.text().split(',')))
                    self.circle_data_dict.setdefault("position", position)

                self.circle_data_dict_total.setdefault(str(i+1), self.circle_data_dict)
            else:
                break
        self.circle_data_dict_total.setdefault("cross_line", self.cross_line)
        return self.circle_data_dict_total

    def save_json(self):
        curPath = QDir.currentPath()
        dlgTitle = "Import File"
        filt = "all_file(*.json*)"
        filename = QFileDialog.getSaveFileName(None, dlgTitle, curPath, filt)
        if filename[0] == '':
            pass
        else:
            json_file = os.path.split(filename[0])
            json_path = json_file[0]
            json_name = json_file[1]
            self.pattern_api.save_json(path=json_path, name=json_name)

    def import_json(self):
        curPath = QDir.currentPath()
        dlgTitle = "Import File"
        filt = "all_file(*.json*)"
        filename = QFileDialog.getOpenFileName(None, dlgTitle, curPath, filt)
        if filename[0] == '':
            pass
        else:
            json_file = self.pattern_api.load_json(path=filename[0])
            self.set_data_at_tabelwidget(json_file)  

    def set_data_at_tabelwidget(self, data:dict):
        for index, circle_index in enumerate(data):
            if circle_index != "cross_line":
                circle_data = data[circle_index]
                print(circle_data)
                shape = circle_data["shape"]
                radius = circle_data["radius"]
                shape_combobox = self.ui.tableWidget.cellWidget(int(index), 0)
                if shape == "circle":
                    shape_combobox.setCurrentIndex(0)
                elif shape == "square":
                    shape_combobox.setCurrentIndex(1)
                else:
                    pass
                self.ui.tableWidget.setItem(int(index), 1, QTableWidgetItem(str(radius)))
                if "color" not in circle_data:
                    self.ui.tableWidget.setItem(int(index), 2, QTableWidgetItem("0, 0, 0"))
                else:
                    color = circle_data["color"]
                    color = str(color).lstrip("[")
                    color = str(color).strip("]")
                    self.ui.tableWidget.setItem(int(index), 2, QTableWidgetItem(str(color)))
                if "position" not in circle_data:
                    self.ui.tableWidget.setItem(int(index), 3, QTableWidgetItem("0, 0"))
                else:
                    position = circle_data["position"]
                    position = str(position).lstrip("[")
                    position = str(position).strip("]")
                    self.ui.tableWidget.setItem(int(index), 3, QTableWidgetItem(str(position)))
            else:
                if data[circle_index] == "True":
                    self.cross_line = "True"
                    self.ui.cross_line_click.setCheckState(Qt.Checked)
                else:
                    self.cross_line = "False"
        self.get_data_from_tabelwidget()

    def cross_line_checkbox(self, checkbox_state:int):
        if (QtCore.Qt.Checked == checkbox_state):
            self.cross_line = "True"
        else:
            self.cross_line = "False"
            
    def send_re(self,data):
        rclpy.init(args=None)
        node = rclpy.create_node('ControlPatternNode')
        cli = node.create_client(PassData, 'pass_data')
        req = PassData.Request()
        req.width = self.res_width
        req.height = self.res_length
        req.data = demjson.encode(data)
        while not cli.wait_for_service(timeout_sec=1.0):
            node.get_logger().info('service not available, waiting again...')
        future = cli.call_async(req)
        rclpy.spin_until_future_complete(node, future)
        result = future.result()
        node.get_logger().info('width:%d\n height:%d\n pattern data:\n%s' %(req.width, req.height, req.data))
        node.destroy_node()
        rclpy.shutdown()
        curPath = QDir.currentPath()
        with open(os.path.join(curPath, "tmp.json"), 'w') as savefile:
            savefile.write(json.dumps(data, indent=4))
    


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
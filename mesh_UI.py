
from PyQt5 import QtCore, QtGui, QtWidgets
from mesh_Algo import Slicer_Algo

import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph as pg

# Pour fonctionner ce script necessite :
# - numpy 1.16 ou superieur (l'argument max_rows de la fonction np.loadtxt est une nouvauté de la version 1.16)
# - pyqtgraph --> pip install pyqtgraph
# - PyQt5 --> pip install pyqt5 (attention aux conflits avec pyqt4)


# *************************************************************************************
# Affiche une fenetre pour l'exploration de fichiers
# *************************************************************************************
class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog().Options()

        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "STL Reader", "", "(*.stl;*.txt)", options=options)
        if fileName:
            temp_filepath = str(fileName).split('/')
            filepath = ''
            for step in temp_filepath[:-1]:
                filepath = filepath + '/' + step
            return fileName

# *************************************************************************************
# Affiche la fenetre principale
# *************************************************************************************


class Ui_MESH(object):
    def setupUi(self, MESH):

        # *************************************************************************************
        # Definition de l'UI
        # *************************************************************************************

        MESH.setObjectName("MESH")
        MESH.resize(1000, 600)
        self.widget = QtWidgets.QWidget(MESH)
        self.widget.setGeometry(QtCore.QRect(0, 0, 750, 600))
        self.widget.setObjectName("widget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(MESH)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(760, 30, 220, 540))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_0 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_0.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_0.setObjectName("verticalLayout_0")
        self.line_4 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_0.addWidget(self.line_4)
        self.label_title = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.verticalLayout_0.addWidget(self.label_title)
        self.line_8 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.verticalLayout_0.addWidget(self.line_8)
        self.label_e1 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_e1.setText("")
        self.label_e1.setObjectName("label_e1")
        self.verticalLayout_0.addWidget(self.label_e1)
        self.bttn_open = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.bttn_open.setObjectName("bttn_open")
        self.verticalLayout_0.addWidget(self.bttn_open)
        self.gridLayout_33 = QtWidgets.QGridLayout()
        self.gridLayout_33.setObjectName("gridLayout_33")
        self.line_nb_segments = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.line_nb_segments.setObjectName("line_nb_segments")
        self.gridLayout_33.addWidget(self.line_nb_segments, 0, 1, 1, 1)
        self.label_file_name = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_file_name.setFont(font)
        self.label_file_name.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_file_name.setObjectName("label_file_name")
        self.gridLayout_33.addWidget(self.label_file_name, 1, 0, 1, 1)
        self.line_file_name = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.line_file_name.setObjectName("line_file_name")
        self.gridLayout_33.addWidget(self.line_file_name, 1, 1, 1, 1)
        self.label_nb_tri = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_nb_tri.setFont(font)
        self.label_nb_tri.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_nb_tri.setObjectName("label_nb_tri")
        self.gridLayout_33.addWidget(self.label_nb_tri, 0, 0, 1, 1)
        self.verticalLayout_0.addLayout(self.gridLayout_33)
        self.line_6 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_0.addWidget(self.line_6)
        self.label_e2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_e2.setText("")
        self.label_e2.setObjectName("label_e2")
        self.verticalLayout_0.addWidget(self.label_e2)
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.label_e6 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_e6.setText("")
        self.label_e6.setObjectName("label_e6")
        self.verticalLayout_1.addWidget(self.label_e6)
        self.line_5 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_1.addWidget(self.line_5)
        self.label_plan_title = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_plan_title.setFont(font)
        self.label_plan_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_plan_title.setObjectName("label_plan_title")
        self.verticalLayout_1.addWidget(self.label_plan_title)
        self.grid_cut_definition = QtWidgets.QGridLayout()
        self.grid_cut_definition.setObjectName("grid_cut_definition")
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.grid_cut_definition.addWidget(self.line, 3, 1, 1, 1)
        self.grid_point = QtWidgets.QGridLayout()
        self.grid_point.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.grid_point.setHorizontalSpacing(15)
        self.grid_point.setObjectName("grid_point")
        self.label_y_direction = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_y_direction.setFont(font)
        self.label_y_direction.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_y_direction.setObjectName("label_y_direction")
        self.grid_point.addWidget(self.label_y_direction, 1, 0, 1, 1)
        self.label_x_direction = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_x_direction.setFont(font)
        self.label_x_direction.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_x_direction.setObjectName("label_x_direction")
        self.grid_point.addWidget(self.label_x_direction, 0, 0, 1, 1)
        self.line_x_dir = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.line_x_dir.setObjectName("line_x_dir")
        self.grid_point.addWidget(self.line_x_dir, 0, 1, 1, 1)
        self.line_z_dir = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.line_z_dir.setObjectName("line_z_dir")
        self.grid_point.addWidget(self.line_z_dir, 2, 1, 1, 1)
        self.label_z_direction = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_z_direction.setFont(font)
        self.label_z_direction.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_z_direction.setObjectName("label_z_direction")
        self.grid_point.addWidget(self.label_z_direction, 2, 0, 1, 1)
        self.line_y_dir = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.line_y_dir.setObjectName("line_y_dir")
        self.grid_point.addWidget(self.line_y_dir, 1, 1, 1, 1)
        self.grid_cut_definition.addLayout(self.grid_point, 3, 2, 1, 1)
        self.grid_pnt = QtWidgets.QGridLayout()
        self.grid_pnt.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.grid_pnt.setHorizontalSpacing(15)
        self.grid_pnt.setObjectName("grid_pnt")
        self.label_y_point = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_y_point.setFont(font)
        self.label_y_point.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_y_point.setObjectName("label_y_point")
        self.grid_pnt.addWidget(self.label_y_point, 1, 0, 1, 1)
        self.label_x_point = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_x_point.setFont(font)
        self.label_x_point.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_x_point.setObjectName("label_x_point")
        self.grid_pnt.addWidget(self.label_x_point, 0, 0, 1, 1)
        self.line_x_pnt = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.line_x_pnt.setObjectName("line_x_pnt")
        self.grid_pnt.addWidget(self.line_x_pnt, 0, 1, 1, 1)
        self.line_z_pnt = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.line_z_pnt.setObjectName("line_z_pnt")
        self.grid_pnt.addWidget(self.line_z_pnt, 2, 1, 1, 1)
        self.label_z_point = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_z_point.setFont(font)
        self.label_z_point.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_z_point.setObjectName("label_z_point")
        self.grid_pnt.addWidget(self.label_z_point, 2, 0, 1, 1)
        self.line_y_pnt = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.line_y_pnt.setObjectName("line_y_pnt")
        self.grid_pnt.addWidget(self.line_y_pnt, 1, 1, 1, 1)
        self.grid_cut_definition.addLayout(self.grid_pnt, 3, 0, 1, 1)
        self.label_point_title = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_point_title.setMaximumSize(QtCore.QSize(16777215, 16777214))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_point_title.setFont(font)
        self.label_point_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_point_title.setObjectName("label_point_title")
        self.grid_cut_definition.addWidget(self.label_point_title, 2, 0, 1, 1)
        self.label_dir_title = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_dir_title.setFont(font)
        self.label_dir_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dir_title.setObjectName("label_dir_title")
        self.grid_cut_definition.addWidget(self.label_dir_title, 2, 2, 1, 1)
        self.verticalLayout_1.addLayout(self.grid_cut_definition)
        self.bttn_cut = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.bttn_cut.setObjectName("bttn_cut")
        self.verticalLayout_1.addWidget(self.bttn_cut)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_1.addWidget(self.line_2)
        self.grid_cut_result = QtWidgets.QGridLayout()
        self.grid_cut_result.setObjectName("grid_cut_result")
        self.label_perimeter = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_perimeter.setFont(font)
        self.label_perimeter.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_perimeter.setObjectName("label_perimeter")
        self.grid_cut_result.addWidget(self.label_perimeter, 1, 0, 1, 1)
        self.label_nb_segment = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_nb_segment.setFont(font)
        self.label_nb_segment.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_nb_segment.setObjectName("label_nb_segment")
        self.grid_cut_result.addWidget(self.label_nb_segment, 0, 0, 1, 1)
        self.line_nb_segments_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.line_nb_segments_2.setObjectName("line_nb_segments_2")
        self.grid_cut_result.addWidget(self.line_nb_segments_2, 0, 1, 1, 1)
        self.line_area = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.line_area.setObjectName("line_area")
        self.grid_cut_result.addWidget(self.line_area, 2, 1, 1, 1)
        self.label_area = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_area.setFont(font)
        self.label_area.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_area.setObjectName("label_area")
        self.grid_cut_result.addWidget(self.label_area, 2, 0, 1, 1)
        self.line_perimeter = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.line_perimeter.setObjectName("line_perimeter")
        self.grid_cut_result.addWidget(self.line_perimeter, 1, 1, 1, 1)
        self.verticalLayout_1.addLayout(self.grid_cut_result)
        self.verticalLayout_0.addLayout(self.verticalLayout_1)
        self.line_7 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_0.addWidget(self.line_7)
        self.label_e3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_e3.setText("")
        self.label_e3.setObjectName("label_e3")
        self.verticalLayout_0.addWidget(self.label_e3)
        self.label_e2_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_e2_2.setText("")
        self.label_e2_2.setObjectName("label_e2_2")
        self.verticalLayout_0.addWidget(self.label_e2_2)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_0.addWidget(self.line_3)
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.bttn_close = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.bttn_close.setObjectName("bttn_close")
        self.horizontalLayout_1.addWidget(self.bttn_close)
        self.verticalLayout_0.addLayout(self.horizontalLayout_1)
        self.widget.raise_()
        self.label_plan_title.raise_()
        self.verticalLayoutWidget_2.raise_()

        self.retranslateUi(MESH)
        QtCore.QMetaObject.connectSlotsByName(MESH)

        # *************************************************************************************
        # Integration de la fenetre pyqtgraph au widget
        # *************************************************************************************
        self.layout = QtWidgets.QVBoxLayout(self.widget)
        self.w = gl.GLViewWidget()
        self.w.setBackgroundColor(180, 180, 180)
        self.layout.addWidget(self.w)

        # *************************************************************************************
        # Affectation des boutons
        # *************************************************************************************
        self.bttn_open.clicked.connect(self.__open_file)
        self.bttn_close.clicked.connect(self.__close)
        self.bttn_cut.clicked.connect(self.__cut)

        # *************************************************************************************
        # Creation d'une instance de l'objet Slicer_Algo qui va faire les calculs
        # *************************************************************************************
        self.slicer = Slicer_Algo()

    def retranslateUi(self, MESH):
        _translate = QtCore.QCoreApplication.translate
        MESH.setWindowTitle(_translate("MESH", "MESH & SURFACES"))
        self.label_title.setText(_translate("MESH", "MESH AND SURFACES"))
        self.bttn_open.setText(_translate("MESH", "Open"))
        self.label_file_name.setText(_translate("MESH", "File name"))
        self.label_nb_tri.setText(_translate("MESH", "Number of triangles"))
        self.label_plan_title.setText(_translate("MESH", "PLANE DEFINITION"))
        self.label_y_direction.setText(_translate("MESH", "y"))
        self.label_x_direction.setText(_translate("MESH", "x"))
        self.label_z_direction.setText(_translate("MESH", "z"))
        self.label_y_point.setText(_translate("MESH", "y"))
        self.label_x_point.setText(_translate("MESH", "x"))
        self.label_z_point.setText(_translate("MESH", "z"))
        self.label_point_title.setText(_translate("MESH", "Point"))
        self.label_dir_title.setText(_translate("MESH", "Direction"))
        self.bttn_cut.setText(_translate("MESH", "Cut"))
        self.label_perimeter.setText(_translate("MESH", "Perimeter"))
        self.label_nb_segment.setText(_translate("MESH", "Number of segments"))
        self.label_area.setText(_translate("MESH", "Area"))
        self.bttn_close.setText(_translate("MESH", "Close"))

    # *************************************************************************************
    # Redessine la fenetre pyqtgraph
    # *************************************************************************************
    def refresh_display(self):
        if self.tri is not None:
            # self.w = gl.GLViewWidget()
            if len(self.w.items) != 0:
                for i in range(len(self.w.items)):
                    self.w.removeItem(self.w.items[0])

            m2 = gl.GLMeshItem(vertexes=self.tri, color=(0, 1, 36, 100), drawEdges=True, edgeColor=(0, 0, 254, 1), smooth=False, shader='balloon')
    # m2.translate(-5, 5, 0)
            self.w.addItem(m2)
            dim_view = 3 * np.max(self.tri)
            self.w.opts['distance'] = dim_view

            axis = gl.GLAxisItem()
            axis.setSize(x=dim_view / 3 * 1.5, y=dim_view / 3 * 1.5, z=dim_view / 3 * 1.5)
            self.w.addItem(axis)

    def __close(self):
        MESH.close()

    # *************************************************************************************
    # Ouvre un fichier .stl ou .txt avec points et connections des points
    # *************************************************************************************
    def __open_file(self):
        f_dial = App()
        self.file_path = f_dial.openFileNameDialog()
        if self.file_path is not None:
            self.tri = self.slicer.read_file(self.file_path)
            self.line_nb_segments.setText('  ' + str(len(self.tri)))
            self.line_file_name.setText('  ' + self.file_path.split('/')[-1])
            self.refresh_display()

    # *************************************************************************************
    # Calcul l'intersection et affiche le resultat dans la fenetre
    # Calcul le perimetre de l'intersection
    # Calcul l'aire defini par le perimetre
    # *************************************************************************************
    def __cut(self):
        self.plane = np.array([[float(self.line_x_pnt.text()), float(self.line_y_pnt.text()), float(self.line_z_pnt.text())],
                               [float(self.line_x_dir.text()), float(self.line_y_dir.text()), float(self.line_z_dir.text())]])

        intersection = self.slicer.cut(self.plane)
        area = self.slicer.compute_area(intersection)
        perimeter = self.slicer.compute_perimeter(intersection)
        nb_vertex = len(intersection)

        self.line_area.setText('  ' + str(round(area, 4)))
        self.line_perimeter.setText('  ' + str(round(perimeter, 4)))
        self.line_nb_segments_2.setText('  ' + str(round(nb_vertex, 4)))

        pnts = []
        for vertex in intersection:
            pnts.append(vertex[0])
            pnts.append(vertex[1])

        pnts = np.array(pnts)

        plt = gl.GLLinePlotItem(pos=pnts, color=(1, 0, 0, 1), width=3., antialias=True)
        self.w.addItem(plt)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MESH = QtWidgets.QWidget()
    ui = Ui_MESH()
    ui.setupUi(MESH)
    MESH.show()
    sys.exit(app.exec_())

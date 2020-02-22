### Louise Harding
### MLDM M1
### Advanced algorithm TSP project

import copy
import sys
import networkx as nx
import math
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from PyQt5.uic import loadUi
from branchandbound.BranchAndBoundTSP import BranchAndBound
from bruteforce.bruteforce import Brute
from dynamic.tspdp import TspDp
from randomTSP.tsprandom import TspRandom
from Greedy.Greedy import GreedyTsp
from GeneticTSP.GeneticAlgorithm import Genetic
from MST.MST import MST
from Generator import Generator
from Parser import Parser
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from BnBAddingRemovingEdges.BnB import AddRemoveEdges
from antcolonyapproach.antcolonyapproach import AntApproach

#uncomment for high resolution screen
#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

class TSP(QDialog):
    def __init__(self):
        super(TSP, self).__init__()
        loadUi("UI/TSP.ui", self)
        # List of available algorithms
        algos = ["Brute Force", "Branch and Bound", "Add and Remove Edges", "Genetic", "Random", "Dynamic", "Greedy", "Minimum Spanning Tree", "Ant Colony", ]
        self.matrix = []
        self.cboAlgo.clear()
        self.cboAlgo.addItems(algos)
        formats = ["Generator", "TSP Library"]
        self.cboFormat.addItems(formats)
        self.frmUpload.move(10, 70)
        self.frmUpload.setHidden(True)
        self.frmResults.setHidden(True)

        self.btnRun.clicked.connect(self.on_run_clicked)
        self.btnData.clicked.connect(self.load_data)
        self.btnBrowse_Open.clicked.connect(self.on_browse_open_clicked)
        self.btnBrowse_Save.clicked.connect(self.on_browse_save_clicked)
        self.btnClear.clicked.connect(self.on_btnClear_clicked)
        self.optGenerate.toggled.connect(self.optGenerate_clicked)
        self.optExisting.toggled.connect(self.optExisting_clicked)
        self.onlyInt = QIntValidator()
        self.txtVertices.setValidator(self.onlyInt)
        self.txtConnect.setValidator(self.onlyInt)
        self.txtMin.setValidator(self.onlyInt)
        self.txtMax.setValidator(self.onlyInt)

        ## a figure instance to plot on
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.wdGraph.setLayout(layout)

    def plot_initial(self, matrix):

        self.canvas.figure.clf()
        # create networkx graph
        graph = nx.Graph()

        row_pos = 0
        # add edges from adj matrix
        for row in matrix:
            col_pos = 0
            for col in row:
                if (col != math.inf and col != -1):
                    graph.add_edge(row_pos + 1, col_pos + 1, label=col)
                col_pos +=1
            row_pos +=1

        # set layout and other settings
        graph_pos=nx.shell_layout(graph)
        node_size = 1000
        font_size = 12
        node_colour = 'green'
        vertex_count = len(matrix)
        if vertex_count > 10:
            node_size =500
            font_size = 8

        if vertex_count > 20:
            graph_pos=nx.random_layout(graph)
            node_size =250

        if vertex_count >=50:
            node_size =50
            node_colour = 'black'

        # draw graph
        nx.draw_networkx_nodes(graph,graph_pos,node_size=node_size, alpha=0.5, node_color=node_colour)
        nx.draw_networkx_edges(graph,graph_pos,width=1,alpha=0.5,edge_color='blue')
        if vertex_count < 70:
            nx.draw_networkx_labels(graph, graph_pos,font_size=font_size, font_family='sans-serif')

        if vertex_count <= 10:
            nx.draw_networkx_edge_labels(graph, graph_pos, edge_labels={(u, v): d["label"] for u, v, d in graph.edges(data=True)},
                                     label_pos=0.4, font_size=8)

        # show graph
        plt.axis("off")
        self.canvas.draw()

    def plot_path(self, path):

        self.canvas.figure.clf()
        # create networkx graph
        graph=nx.Graph()

        row_pos = 0

        graph.add_path(nodes=path)
        # set layout and other settings
        graph_pos=nx.shell_layout(graph)

        node_size = 1000
        font_size = 12
        node_colour = 'green'
        vertex_count = len(path)
        if vertex_count > 10:
            node_size =500
            font_size = 8

        if vertex_count > 20:
            graph_pos=nx.random_layout(graph)
            node_size =250

        if vertex_count >=50:
            node_size =50
            node_colour = 'black'

        # draw graph
        nx.draw_networkx_nodes(graph,graph_pos,node_size=node_size, alpha=0.5, node_color=node_colour)
        nx.draw_networkx_edges(graph,graph_pos,width=1,alpha=0.5,edge_color='red')
        nx.draw_networkx_labels(graph, graph_pos,font_size=font_size, font_family='sans-serif')

        # show graph
        plt.axis("off")
        self.canvas.draw()

    def optGenerate_clicked(self):
        self.frmGenerate.setEnabled(self.optGenerate.isChecked())
        self.frmGenerate.setHidden(False)
        self.frmUpload.setHidden(True)

    def optExisting_clicked(self):
        self.frmGenerate.setEnabled(self.optGenerate.isChecked())
        self.frmGenerate.setHidden(True)
        self.frmUpload.setHidden(False)

    def on_btnClear_clicked(self):
        self.frmResults.setHidden(True)
        self.canvas.figure.clf()
        self.canvas.draw()

    def on_browse_open_clicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '\data')
        self.txtFileName.setText(fname[0])

    def on_browse_save_clicked(self):
        fname = QFileDialog.getSaveFileName(self, 'Open file', '\data')
        self.txtSaveAs.setText(fname[0])

    def validate_generator_entries(self):
        error_message = ""
        if len(self.txtVertices.text()) == 0:
            error_message += "Please enter a number for vertices. \n"
        if len(self.txtConnect.text()) == 0:
            error_message += "Please enter a number for connectivity. \n"
        if len(self.txtMin.text()) == 0:
            error_message += "Please enter a number for min edge weight. \n"
        if len(self.txtMax.text()) == 0:
            error_message += "Please enter a number for max edge weight. \n"
        return error_message

    #hide the results frame
    def hide_frame(self, frame):
        frame.hide()

    #how the results frame
    def show_frame(self, frame):
        frame.show()

    #load the data
    def load_data(self):
        # Create a new generator.
        generator = Generator()
        #first of all see what is selected from the data options
        if self.optGenerate.isChecked():
            errors = self.validate_generator_entries()
            if len(errors) == 0:
                numVert = int(self.txtVertices.text())
                connect = int(self.txtConnect.text())
                minWgt = int(self.txtMin.text())
                maxWgt = int(self.txtMax.text())
                if minWgt >= maxWgt:
                    QMessageBox.question(self, 'Generator validation', "Min edge weight must be less than max edge weight.", QMessageBox.Ok)
                    return
                symmetric = self.chkSym.isChecked()
                # Generate a new matrix with given parameters.
                matrix = generator.generate(numVert, connect, minWgt, maxWgt, symmetric)
                #if the Save_As text box is not empty, save for later.
                if len(self.txtSaveAs.text()) > 0:
                    generator.save_to_file(matrix, self.txtSaveAs.text())
            else:
                QMessageBox.question(self, 'Generator validation', errors, QMessageBox.Ok)
                return
        else:
            #check for a file path
            if len(self.txtFileName.text()) == 0:
                QMessageBox.question(self, 'Generator validation', "Please select a file to open.", QMessageBox.Ok)
                return
            #Open and process the selected file
            try:
                if self.cboFormat.currentText() == "Generator":
                    matrix = generator.read_from_file(self.txtFileName.text())
                else:
                    # Open the problem file (Either .tsp or .atsp)
                    file = open(self.txtFileName.text(), 'r')
                    # Create a new TSP library parser and parse the file
                    parser = Parser()
                    matrix = parser.parse_file(file)
            except:
                QMessageBox.question(self, 'File validation', "File not in required format. Please check the file type.", QMessageBox.Ok)
                return

        #Plot the data
        if not self.chkHideGraph.isChecked():
            self.plot_initial(matrix)

        self.matrix = matrix


    @pyqtSlot()
    def on_run_clicked(self):
        if len(self.matrix) == 0:
            self.load_data()

        #TODO: Warn here if large dataset and BnB or Brute Force (maybe others)
        #Now we have the data, process the selected algorithm
        path_cost = 0
        best_path = []
        run_time = 0
        matrix = copy.deepcopy(self.matrix)
        if self.cboAlgo.currentText() == "Brute Force":
            brute = Brute(matrix)
            path_cost, best_path, run_time = brute.algo()

        if self.cboAlgo.currentText() == "Branch and Bound":
            algo = BranchAndBound()
            path_cost, best_path, run_time = algo.run_branch_and_bound(matrix)

        elif self.cboAlgo.currentText() == "Minimum Spanning Tree":
            algo = MST(matrix)
            path_cost, best_path, run_time = algo.mst()

        elif self.cboAlgo.currentText() == "Genetic":
            algo = Genetic(matrix)
            path_cost, best_path, run_time = algo.main()

        elif self.cboAlgo.currentText() == "Add and Remove Edges":
            algo = AddRemoveEdges(matrix)
            path_cost, best_path, run_time = algo.main()

        elif self.cboAlgo.currentText() == "Greedy":
            algo = GreedyTsp(matrix)
            path_cost, best_path, run_time = algo.greedy_tsp()

        elif self.cboAlgo.currentText() == "Dynamic":
            algo = TspDp(matrix)
            path_cost, best_path, run_time = algo.run()

        elif self.cboAlgo.currentText() == "Random":
            algo = TspRandom(matrix)
            path_cost, best_path, run_time = algo.run()

        elif self.cboAlgo.currentText() == "Ant Colony":
            ant_colony = AntApproach(matrix)
            path_cost, best_path, run_time = ant_colony.Algo()

        #set fields
        self.lblDistance.setText("Best Distance: " + str(path_cost))
        self.lblPath.setText("Best Path: " + str(best_path))
        self.lblExec.setText("Execution Time (s): " + str(round(run_time, 2)))
        self.show_frame(self.frmResults)
        if not self.chkHideGraph.isChecked():
            self.plot_path(best_path)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    window = TSP()
    window.show()
    sys.exit(app.exec_())

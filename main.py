from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFileDialog, QComboBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.colors as mcolors
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
from graphWidget import *
from gui import * 

class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.unitUI = Ui_MainWindow()
        self.unitUI.setupUi(self)
        self.setGeometry(40, 40, 1300, 950)

        self.x_axis = ""
        self.y_axis = ""
        self.size= ""
        self.hue= ""
        self.marker = ""

        self.setText()
        self.addItem()
        self.actionTriggered()

    def setText(self):

        self.unitUI.label_3.setText("x axis :")
        self.unitUI.label_4.setText("y axis :")
        self.unitUI.label_5.setText("size :")
        self.unitUI.label_6.setText("color :")
        self.unitUI.label.setText("marker :")

        self.unitUI.pushButton_4.setText("select the file")
        self.unitUI.pushButton.setText("draw the graph")
        self.unitUI.pushButton_2.setText("clear the data frame")

        self.unitUI.checkBox_2.setText("x axis")
        self.unitUI.checkBox.setText("y axis")
        self.unitUI.checkBox_3.setText("size")
        self.unitUI.checkBox_4.setText("color")
        self.unitUI.checkBox_5.setText("marker")

    def addItem(self):

        self.graph_list = ["scatter plot"]
        self.unitUI.comboBox_6.addItems(self.graph_list)

    def addItem1(self):
       
        dfcolumns = self.df.columns
        self.comboBoxes = self.unitUI.verticalFrame_2.findChildren(QComboBox)
        for comboBox in self.comboBoxes:
            for collumn in dfcolumns:
                comboBox.addItem(collumn)


    def actionTriggered(self):

        self.unitUI.checkBox_2.setChecked(True)
        self.unitUI.checkBox.setChecked(True)
        self.unitUI.checkBox_2.setEnabled(False)
        self.unitUI.checkBox.setEnabled(False)

        self.unitUI.pushButton_4.clicked.connect(self.selectFile)
        self.unitUI.pushButton.clicked.connect(self.drawGraph)
        self.unitUI.pushButton_2.clicked.connect(self.clearDf)

        self.unitUI.pushButton.setEnabled(False)
        self.unitUI.pushButton_2.setEnabled(False)

    def selectFile(self):

        filter = "CSV Files (*.csv);;All Files (*)"
        url = QFileDialog.getOpenFileName(self, "select the file", "",filter)
        self.filePath = url[0]

        if os.path.isfile(self.filePath):
            self.unitUI.pushButton_4.setText("the file selected")
            self.unitUI.label_2.setText("loading the data frame")
            self.uploadFile()
        else:
            self.unitUI.label_2.setText("the selected file does not exist or is not a file")

    def uploadFile(self):

        self.df = pd.read_csv(self.filePath)
        self.addItem1()
        self.drawHeatMap()

        self.unitUI.pushButton_4.setEnabled(False)
        self.unitUI.pushButton.setEnabled(True)
        self.unitUI.pushButton_2.setEnabled(True)

        self.unitUI.checkBox_3.setEnabled(True)
        self.unitUI.checkBox_4.setEnabled(True)
        self.unitUI.checkBox_5.setEnabled(True)

        self.unitUI.label_2.setText("the data frame loaded")

    def drawGraph(self):
        
        self.clearLayout(self.unitUI.verticalLayout_11)
        self.clearLayout(self.unitUI.verticalLayout_10)

        custom_palette = ["#c3965f","#900c3f","#6f7275","#364a60","#3894a3"]
        sns.set_palette(custom_palette)

        b1 = self.unitUI.checkBox_3.isChecked()
        b2 = self.unitUI.checkBox_4.isChecked()
        b3 = self.unitUI.checkBox_5.isChecked()        
        countTrue = sum([b1,b2,b3])

        self.x = self.unitUI.comboBox.currentText()
        self.y = self.unitUI.comboBox_2.currentText()
        self.size = self.unitUI.comboBox_4.currentText()
        self.color = self.unitUI.comboBox_3.currentText()
        self.marker = self.unitUI.comboBox_5.currentText()

        plotType = self.unitUI.comboBox_6.currentText()

        if plotType == self.graph_list[0]:

            self.fig, ax = plt.subplots()

            if countTrue == 1:
                if b1 :
                    scatter = sns.scatterplot(data=self.df, x=self.x, y=self.y,size=self.size)
                elif b2 :
                    scatter = sns.scatterplot(data=self.df, x=self.x, y=self.y,hue=self.color)
                else:
                    scatter = sns.scatterplot(data=self.df, x=self.x, y=self.y,style=self.marker)
            elif countTrue == 2:
                if b1 and b2 :
                    scatter = sns.scatterplot(data=self.df, x=self.x, y=self.y,size=self.size,hue=self.color)
                elif b2 and b3 :
                    scatter = sns.scatterplot(data=self.df, x=self.x, y=self.y,hue=self.color,style=self.marker)
                else:
                    scatter = sns.scatterplot(data=self.df, x=self.x, y=self.y,hue=self.color,style=self.marker)
            elif countTrue == 3:
                    scatter = sns.scatterplot(data=self.df, x=self.x, y=self.y,size=self.size,hue=self.color,style=self.marker)
            else:
                scatter = sns.scatterplot(data=self.df, x=self.x, y=self.y)

            if countTrue != 0:
                ax.get_legend().remove()
                self.legend_fig, legend_ax = plt.subplots()
                handles, labels = scatter.get_legend_handles_labels()
                legend_ax.legend(handles, labels, loc='center')
                legend_ax.axis('off') 
                self.legend_widget = LegendWidget(self.legend_fig)
                self.unitUI.verticalLayout_10.addWidget(self.legend_widget)

            self.plot_widget = GraphWidget(self.fig)
            self.unitUI.verticalLayout_11.addWidget(self.plot_widget)

    def drawHeatMap(self):

        dfHeatMap = self.df.select_dtypes(include=['number'])

        colors = ["#f2ebe5", "#c3965f","#cad1ce"] 
        cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors)

        heatMap = sns.clustermap(
            dfHeatMap.corr(),
            annot=True,
            linewidths=0.5,
            linecolor="black",
            fmt='.3f',
            cbar=True,
            figsize=(6,6),
            row_cluster=False, 
            col_cluster=False, 
            cmap=cmap)

        heatMap.ax_heatmap.set_xticklabels(heatMap.ax_heatmap.get_xticklabels(), rotation=90)
        heatMap.ax_heatmap.set_yticklabels(heatMap.ax_heatmap.get_yticklabels(), rotation=0)

        self.fig = heatMap.fig
        self.ax = heatMap.ax_heatmap
        
        self.plot_widget = GraphWidget(self.fig)
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.unitUI.horizontalLayout_25.addWidget(self.plot_widget)

    def clearLayout(self,layout):

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def clearDf(self):

        self.filePath = ""

        self.clearLayout(self.unitUI.verticalLayout_10)
        self.clearLayout(self.unitUI.verticalLayout_11)
        self.clearLayout(self.unitUI.horizontalLayout_25)
        
        self.comboBoxes = self.unitUI.verticalFrame_2.findChildren(QComboBox)
        for comboBox in self.comboBoxes:
            for collumn in range(0,len(self.comboBoxes)):
                comboBox.clear()

        self.comboBoxes = []
        self.df = None

        self.x = ""
        self.y = ""
        self.size = ""
        self.color = ""
        self.marker = ""

        self.unitUI.label_2.setText("")
        self.unitUI.pushButton_4.setEnabled(True)
        self.unitUI.pushButton.setEnabled(False)
        self.unitUI.pushButton_2.setEnabled(False)

        self.unitUI.checkBox_3.setChecked(False)
        self.unitUI.checkBox_4.setChecked(False)
        self.unitUI.checkBox_5.setChecked(False)

        self.unitUI.checkBox_3.setEnabled(False)
        self.unitUI.checkBox_4.setEnabled(False)
        self.unitUI.checkBox_5.setEnabled(False)

        self.unitUI.pushButton_4.setText("select the file")
       

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

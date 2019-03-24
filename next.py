# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'next.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt 
import random
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from deap import creator, base, tools, algorithms
import sys
from PyQt4 import QtCore, QtGui


def avg(l):
    """
    Returns the average between list elements
    """
    return (sum(l)/float(len(l)))


def getFitness(individual, X, y):
    """
    Feature subset fitness function
    """

 #   print individual

    if(individual.count(0) != len(individual)):
        # get index with value 0
        cols = [index for index in range(
            len(individual)) if individual[index] == 0]

        # get features subset
        X_parsed = X.drop(X.columns[cols], axis=1)
        X_subset = pd.get_dummies(X_parsed)

        # apply classification algorithm
        clf = LogisticRegression()

        return (avg(cross_val_score(clf, X_subset, y, cv=5)),)
    else:
        return(0,)


def geneticAlgorithm(X, y, n_population, n_generation):
    """
    Deap global variables
    Initialize variables to use eaSimple
    """
    # create individual
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # create toolbox
    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat,
                     creator.Individual, toolbox.attr_bool, len(X.columns))
    toolbox.register("population", tools.initRepeat, list,
                     toolbox.individual)
    toolbox.register("evaluate", getFitness, X=X, y=y)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # initialize parameters
    pop = toolbox.population(n=n_population)
    hof = tools.HallOfFame(n_population * n_generation)
    stats = tools.Statistics(lambda ind: ind.fitness.values)

    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)




    # genetic algorithm
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2,
                                   ngen=n_generation, stats=stats, halloffame=hof,
                                   verbose=True)

    avrg= log.select("avg")
    print "avg", avrg
    
    # return hall of fame
    return hof


def bestIndividual(hof, X, y):
    """
    Get the best individual
    """
    maxAccurcy = 0.0
    for individual in hof:
        if(individual.fitness.values > maxAccurcy):
            maxAccurcy = individual.fitness.values
            _individual = individual

    _individualHeader = [list(X)[i] for i in range(
        len(_individual)) if _individual[i] == 1]
    return _individual.fitness.values, _individual, _individualHeader



try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


ac=""
class Ui_NextWindow(object):

    def __init__(self):
        self.d_val= ""
        self.p_val= 0
        self.g_val= 0


    def get_values(self, dataset_val, population_val, generation_val):
        self.d_val= dataset_val
        self.p_val= population_val
        self.g_val= generation_val
        print self.d_val, self.p_val, self.g_val
        dataframePath, n_pop, n_gen = str(self.d_val), int(self.p_val), int(self.g_val)
        print dataframePath
        df = pd.read_csv(dataframePath, sep=',')

        # encode labels column to numbers
        le = LabelEncoder()
        le.fit(df.iloc[:, -1])
        y = le.transform(df.iloc[:, -1])            # output labels
        X = df.iloc[:, :-1]                         # input features

        # get accuracy with all features
        individual = [1 for i in range(len(X.columns))]

        ac= str(getFitness(individual, X, y))

        print("Accuracy with all features: \t" +
              ac + "\n")



        # apply genetic algorithm
        hof = geneticAlgorithm(X, y, n_pop, n_gen)

        # select the best individual
        accuracy, individual, header = bestIndividual(hof, X, y)
        print('Best Accuracy: \t' + str(accuracy))
        print('Number of Features in Subset: \t' + str(individual.count(1)))
        print('Individual: \t\t' + str(individual))
        print('Feature Subset\t: ' + str(header))

        print('\n\ncreating a new classifier with the result')

        # read dataframe from csv one more time
        df = pd.read_csv(dataframePath, sep=',')

        # with feature subset
        X = df[header]

        clf = LogisticRegression()

        scores = cross_val_score(clf, X, y, cv=5)
        print("Accuracy with Feature Subset: \t" + str(avg(scores)) + "\n")

        

        #print "inside avrg", avrg




    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setFixedSize(656, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.iteration_tab = QtGui.QTableWidget(self.centralwidget)
        self.iteration_tab.setGeometry(QtCore.QRect(20, 60, 611, 191))
        self.iteration_tab.setObjectName(_fromUtf8("iteration_tab"))
        self.iteration_tab.setColumnCount(5)
        self.iteration_tab.setRowCount(10)
        self.iteration_tab.setHorizontalHeaderLabels("gen;nevals;avg;min;max;".split(";"))

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 10, 311, 51))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 270, 181, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(280, 270, 121, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(420, 270, 211, 31))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(50, 350, 131, 41))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(270, 350, 111, 41))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(420, 360, 211, 21))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.all_features = QtGui.QTextEdit(self.centralwidget)
        self.all_features.setGeometry(QtCore.QRect(70, 300, 101, 51))
        self.all_features.setObjectName(_fromUtf8("all_features"))
        

        self.best = QtGui.QTextEdit(self.centralwidget)
        self.best.setGeometry(QtCore.QRect(270, 300, 111, 51))
        self.best.setObjectName(_fromUtf8("best"))
        self.num_features = QtGui.QTextEdit(self.centralwidget)
        self.num_features.setGeometry(QtCore.QRect(470, 300, 91, 51))
        self.num_features.setObjectName(_fromUtf8("num_features"))
        self.individual = QtGui.QTextEdit(self.centralwidget)
        self.individual.setGeometry(QtCore.QRect(20, 390, 171, 51))
        self.individual.setObjectName(_fromUtf8("individual"))
        self.subset = QtGui.QTextEdit(self.centralwidget)
        self.subset.setGeometry(QtCore.QRect(240, 390, 181, 51))
        self.subset.setObjectName(_fromUtf8("subset"))
        self.acc_subset = QtGui.QTextEdit(self.centralwidget)
        self.acc_subset.setGeometry(QtCore.QRect(450, 390, 131, 51))
        self.acc_subset.setObjectName(_fromUtf8("acc_subset"))

        MainWindow.setCentralWidget(self.centralwidget)




        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Results in Every Generation", None))
        self.label_2.setText(_translate("MainWindow", "Accuracy With All Features", None))
        self.label_3.setText(_translate("MainWindow", "Best Accuracy", None))
        self.label_4.setText(_translate("MainWindow", "Number of Features in Subset", None))
        self.label_5.setText(_translate("MainWindow", "Individual Selected", None))
        self.label_6.setText(_translate("MainWindow", "Feature Subset", None))
        self.label_7.setText(_translate("MainWindow", "Accuracy with Feature Subset", None))




if __name__ == "__main__":
    global avrg

    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_NextWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()





# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GA.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import random
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from deap import creator, base, tools, algorithms
import sys

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

class Ui_MainWindow(object):

	d_val= ""
	p_val= 0
	g_val= 0
	ac=""
	accuracy=0



	def avg(self,l):
		return (sum(l)/float(len(l)))


	def getFitness(self,individual, X, y):
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

	        return (self.avg(cross_val_score(clf, X_subset, y, cv=5)),)
	    else:
	        return(0,)


	def geneticAlgorithm(self,X, y, n_population, n_generation):
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
	    toolbox.register("evaluate", self.getFitness, X=X, y=y)
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

	    self.table_display.append(str(log))

	    avrg= log.select("avg")
	    print "avg", avrg
	    l= [i for i in range(len(avrg))]
	    plt.plot(l, avrg)
	    plt.xlabel("Number of Generations")
	    plt.xlabel("Accuracy of generation")
	    plt.title("Accuracy VS Generation Graph")
	    plt.show()
	    
	    # return hall of fame
	    return hof


	def bestIndividual(self,hof, X, y):
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

	def get_values(self):

		self.table_display.clear()
		self.all_features.clear()
		self.best_acc.clear()
		self.num_of_features.clear()
		self.acc_feature_subset.clear()
		self.feature_subset.clear()
		self.ind_selected.clear()

		self.d_val= self.lv_dataset.currentItem().text()
		self.p_val= self.lv_population.currentItem().text()
		self.g_val=  self.lv_generation.currentItem().text()
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

		ac= str(self.getFitness(individual, X, y))

		print("Accuracy with all features: \t" +
		  ac + "\n")
		self.all_features.append(str(ac))



		# apply genetic algorithm
		hof = self.geneticAlgorithm(X, y, n_pop, n_gen)

		# select the best individual
		self.accuracy, individual, header = self.bestIndividual(hof, X, y)
		print('Best Accuracy: \t' + str(self.accuracy))
		self.best_acc.append(str(self.accuracy))




		print('Number of Features in Subset: \t' + str(individual.count(1)))
		self.num_of_features.append(str(individual.count(1)))
		print('Individual: \t\t' + str(individual))
		self.ind_selected.append( str(individual))
		print('Feature Subset\t: ' + str(header))
		self.feature_subset.append(str(header))

		print('\n\ncreating a new classifier with the result')

		# read dataframe from csv one more time
		df = pd.read_csv(dataframePath, sep=',')

		# with feature subset
		X = df[header]

		clf = LogisticRegression()

		scores = cross_val_score(clf, X, y, cv=5)
		print("Accuracy with Feature Subset: \t" + str(self.avg(scores)) + "\n")
		self.acc_feature_subset.append( str(self.avg(scores)))





	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(533, 553)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.Submit = QtGui.QPushButton(self.centralwidget)
		self.Submit.setGeometry(QtCore.QRect(210, 220, 111, 27))
		self.Submit.setObjectName(_fromUtf8("Submit"))
		self.dataset = QtGui.QLabel(self.centralwidget)
		self.dataset.setGeometry(QtCore.QRect(40, 30, 121, 21))
		self.dataset.setObjectName(_fromUtf8("dataset"))
		self.population = QtGui.QLabel(self.centralwidget)
		self.population.setGeometry(QtCore.QRect(220, 30, 101, 20))
		self.population.setObjectName(_fromUtf8("population"))
		self.generation = QtGui.QLabel(self.centralwidget)
		self.generation.setGeometry(QtCore.QRect(360, 30, 161, 20))
		self.generation.setObjectName(_fromUtf8("generation"))
		self.lv_dataset = QtGui.QListWidget(self.centralwidget)
		self.lv_dataset.setGeometry(QtCore.QRect(40, 60, 111, 131))
		self.lv_dataset.setProperty("hi", _fromUtf8(""))
		self.lv_dataset.setObjectName(_fromUtf8("lv_dataset"))
		self.lv_dataset.addItems(["iris.csv", "nuclear.csv"])
		self.lv_population = QtGui.QListWidget(self.centralwidget)
		self.lv_population.setGeometry(QtCore.QRect(210, 60, 101, 131))
		self.lv_population.setObjectName(_fromUtf8("lv_population"))
		self.lv_population.addItems(["5","10","15","20"])
		self.lv_generation = QtGui.QListWidget(self.centralwidget)
		self.lv_generation.setGeometry(QtCore.QRect(380, 60, 101, 131))
		self.lv_generation.setObjectName(_fromUtf8("lv_generation"))
		self.lv_generation.addItems(["1","2","3","4","5","6","7","8","9","10"])
		self.table_display = QtGui.QTextEdit(self.centralwidget)
		self.table_display.setGeometry(QtCore.QRect(40, 280, 451, 101))
		self.table_display.setObjectName(_fromUtf8("table_display"))
		self.all_features = QtGui.QTextEdit(self.centralwidget)
		self.all_features.setGeometry(QtCore.QRect(20, 420, 101, 51))
		self.all_features.setObjectName(_fromUtf8("all_features"))
		self.best_acc = QtGui.QTextEdit(self.centralwidget)
		self.best_acc.setGeometry(QtCore.QRect(210, 420, 101, 51))
		self.best_acc.setObjectName(_fromUtf8("best_acc"))
		self.num_of_features = QtGui.QTextEdit(self.centralwidget)
		self.num_of_features.setGeometry(QtCore.QRect(390, 420, 101, 51))
		self.num_of_features.setObjectName(_fromUtf8("num_of_features"))
		self.acc_feature_subset = QtGui.QTextEdit(self.centralwidget)
		self.acc_feature_subset.setGeometry(QtCore.QRect(390, 500, 101, 51))
		self.acc_feature_subset.setObjectName(_fromUtf8("acc_feature_subset"))
		self.feature_subset = QtGui.QTextEdit(self.centralwidget)
		self.feature_subset.setGeometry(QtCore.QRect(210, 500, 121, 51))
		self.feature_subset.setObjectName(_fromUtf8("feature_subset"))
		self.ind_selected = QtGui.QTextEdit(self.centralwidget)
		self.ind_selected.setGeometry(QtCore.QRect(20, 500, 101, 51))
		self.ind_selected.setObjectName(_fromUtf8("ind_selected"))
		self.label = QtGui.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(0, 400, 191, 20))
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(self.centralwidget)
		self.label_2.setGeometry(QtCore.QRect(210, 400, 111, 20))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.label_3 = QtGui.QLabel(self.centralwidget)
		self.label_3.setGeometry(QtCore.QRect(10, 480, 141, 20))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label_4 = QtGui.QLabel(self.centralwidget)
		self.label_4.setGeometry(QtCore.QRect(380, 400, 141, 20))
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.label_5 = QtGui.QLabel(self.centralwidget)
		self.label_5.setGeometry(QtCore.QRect(200, 480, 111, 20))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.label_6 = QtGui.QLabel(self.centralwidget)
		self.label_6.setGeometry(QtCore.QRect(330, 480, 201, 20))
		self.label_6.setObjectName(_fromUtf8("label_6"))
		MainWindow.setCentralWidget(self.centralwidget)


		self.Submit.clicked.connect(self.get_values)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
		self.Submit.setText(_translate("MainWindow", "Submit Values", None))
		self.dataset.setText(_translate("MainWindow", "Dataset Selection", None))
		self.population.setText(_translate("MainWindow", "Population No", None))
		self.generation.setText(_translate("MainWindow", " No. of Generations", None))
		self.label.setText(_translate("MainWindow", "Accuracy with All Features", None))
		self.label_2.setText(_translate("MainWindow", "Best Accuracy", None))
		self.label_3.setText(_translate("MainWindow", "Individual Selected", None))
		self.label_4.setText(_translate("MainWindow", "Number of Features", None))
		self.label_5.setText(_translate("MainWindow", "Feature Subset", None))
		self.label_6.setText(_translate("MainWindow", "Accuracy with Feature Subset", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



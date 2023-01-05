
from tkinter import *
from tkinter import messagebox
import pickle

class listObject():
    def __init__(self, name1, password1, balance1):
        self._name = name1
        self._password = password1
        self._balance = balance1
    def setBalance(self, balance1):
        self._balance=balance1
    def setName(self, name1):
        self._name=name1
    def addBalance(self, money):
        self._balance=self._balance+money
    def subBalance(self, money):
        self._balance=self._balance-money
    def setpassword(self, password1):
        self._password=password1
    def getBalance(self):
        return self._balance
    def getName(self):
        return self._name
    def getPassword(self):
        return self._password
    
classList = {}
window = Tk()
try:
    with open('database.pickle', 'rb') as fileIn:
        while True:
            try:
                classList = pickle.load(fileIn)
            except EOFError:
                break
        fileIn.close()
except OSError as e:
    pass
pickleFileOut = open('database.pickle', 'wb')

def saveDataOnExit():
    pickle.dump(classList, pickleFileOut)
    pickleFileOut.close()
    window.destroy()

window.protocol('WM_DELETE_WINDOW', saveDataOnExit) # root is your root window

def mainWindow():
    clearWindow()
    window.title("Welcome to EZTrade")
    window.geometry('100x350')
    btn1 = Button(window, text = "Sign in", command = signIn)
    btn2 = Button(window, text = "Add account", command = addAccount)
    btn3 = Button(window, text = "Delete account", command = deleteAccount)
    btn4 = Button(window, text = "Show accounts", command = showAccount)
    btn5 = Button(window, text = "Delete all accounts", command = destroyAll)
    btn1.grid(column=0, row=0)
    btn2.grid(column=0, row=1)
    btn3.grid(column=0, row=2)
    btn4.grid(column=0, row=3)
    btn5.grid(column=0, row=4)

def deleteAccount():
    print("Working?")
    clearWindow()
    lbl = Label(window, text = "Enter the username you want to delete:")
    txt = Entry(window, width=20)
    btn = Button(window, text = "Enter", command = lambda: deleted(txt.get()))
    btn2 = Button(window, text = "Main Menu", command = mainWindow)
    lbl.grid(column=0, row = 0)
    txt.grid(column=1, row = 0)
    btn.grid(column=0, row = 1)
    btn2.grid(column=1, row = 1)

def deleted(name):
    for k in classList.keys():
        if(name == classList[k].getName()):
            del classList[k]
            mainWindow()
            return
    messagebox.showinfo("Error", "No account exists")
    mainWindow()

def destroyAll():
    classList.clear()

def showAccount():
    clearWindow()
    #for k in list.items():
    textString=""
    for k in classList.keys():
        textString += classList[k].getName()+ "-" + str(classList[k].getBalance()) + "-" + classList[k].getPassword() + "\n"
        label = Label(window, text = textString)
        label2 = Label(window, text = "NAME - BALANCE - PASSWORD: ")
        label2.grid(column = 0, row = 0)
        label.grid(column = 0, row = 1)
        btn = Button(window, text = "Main menu", command = mainWindow)
        btn.grid(column = 1, row = 2)
            
def signIn():
    clearWindow()
    window.title("Welcome to ATM machine")
    window.geometry('350x200')
    lbl = Label(window, text="Username")
    lb2 = Label(window, text="Password")
    lbl.grid(column=0, row=0)
    lb2.grid(column=0, row=1)
    txt = Entry(window, width=20)
    txt2 = Entry(window, show='*', width=20)
    txt.grid(column=1, row=0)
    txt2.grid(column=1, row=1)
    button = Button(window, text = "Enter", command = lambda:signedIn(txt.get(), txt2.get()))
    button.grid(column=2, row=1)
    btn = Button(window, text="Main menu", command=mainWindow)
    btn.grid(column=1, row=2)

def signedIn(username, password):
    if(len(classList)==0):
        messagebox.showinfo("Error", "No accounts available")
        mainWindow()
        return
    else:
        for k in classList.keys():
            if(classList[k].getName() == username):
                if(classList[k].getPassword() != password):
                    signIn()
                    messagebox.showinfo("Error", "Wrong password, please try again")
                    return
            else:
                clearWindow()
                window.title("Welcome to ATM machine")
                window.geometry('350x200')
                bt1 = Button(window, text="Withdraw", command=lambda:withdraw(username))
                bt2 = Button(window, text="Balance inquiry", 
                command=lambda:balance(username))
                bt3 = Button(window, text="Deposit", 
                command=lambda:deposit(username))
                bt1.grid(column=0, row=0)
                bt2.grid(column=0, row=1)
                bt3.grid(column=0, row=2)
                btn = Button(window, text="Main menu", 
                command=mainWindow)
                btn.grid(column=1, row=2)
                return
            signIn()
            messagebox.showinfo("Error", "No username exists, please try again")

def withdraw(username):
    clearWindow()
    label = Label(window, text = "Amount:")
    txt = Entry(window, width= 20)
    label.grid(column=0, row=0)
    txt.grid(column=1, row=0)
    bt = Button(window, text = "Enter", command = lambda:withdrawMoney(username,txt))
    bt.grid(column = 1, row = 1)

def withdrawMoney(username, money):
    try:
        if(float(money.get()) == ''):
            withdraw(username)
        else:
            classList[username].subBalance(float(money.get()))
            mainWindow()
    except ValueError:
        withdraw(username)

def balance(username):
    clearWindow()
    label = Label(window, text="Amount:" + 
    str(classList[username].getBalance()))
    #txt = Entry(window, width=20)
    label.grid(column=0, row=0)
    #txt.grid(column=1, row=0)
    bt = Button(window, text="Main Menu", command=mainWindow)
    bt.grid(column=1, row=1)

def depositMoney(username, money):
    try:
        if (float(money.get()) == ''):
            deposit(username)
        else:
            classList[username].addBalance(float(money.get()))
            mainWindow()
    except ValueError:
        deposit(username)

def deposit(username):
    clearWindow()
    label = Label(window, text="Amount:")
    txt = Entry(window, width=20)
    label.grid(column=0, row=0)
    txt.grid(column=1, row=0)
    bt = Button(window, text="Enter", command=lambda:depositMoney(username, txt))
    bt.grid(column=1, row=1)

def addAccount():
    clearWindow()
    window.title("Welcome to ATM machine")
    window.geometry('350x200')
    lbl = Label(window, text="Please enter a username")
    lb2 = Label(window, text="Please enter a Password")
    lb3 = Label(window, text="Please reenter password")
    lb4 = Label(window, text="Please enter initial deposit")
    lbl.grid(column=0, row=0)
    lb2.grid(column=0, row=1)
    lb3.grid(column=0, row=2)
    lb4.grid(column=0, row=3)
    txt = Entry(window, width=20)
    txt2 = Entry(window, show='*', width=20)
    txt3 = Entry(window, show='*', width=20)
    txt4 = Entry(window, width=20)
    txt.grid(column=1, row=0)
    txt2.grid(column=1, row=1)
    txt3.grid(column=1, row=2)
    txt4.grid(column=1, row=3)
    btn = Button(window, text = "Enter", command = 
    lambda:addedAccount(txt,txt2,txt3, txt4))
    btn.grid(column=1, row=4)
    btn1 = Button(window, text = "Main Menu", command = mainWindow)
    btn1.grid(column=2, row =4)

def addedAccount(name, password, password1, amount):
    if(password.get() != password1.get()):
        messagebox.showinfo('Error', 'Passwords do not match, try again!')
        addAccount()
        return
    if(name.get()=='' or password.get()=='' or amount.get()==''):
        messagebox.showinfo('Error', 'Please try again! There is a blank entry.')
        addAccount()
        return
    for key, value in classList.items():
        print(key)
        if(key == name.get()):
            messagebox.showinfo("Error", "Account already exists, please try again!")
            addAccount()
            return
        else:
            try:
                p = listObject(name.get(),password.get(),float(amount.get()))
                classList[name.get()]=p
                #pickle.dump(classList, file)
                mainWindow()
            except ValueError:
                messagebox.showinfo("Error", "Sorry please only put numerical amount in initial deposit")
            addAccount()

def clearWindow():
    list=window.grid_slaves()
    for l in list:
        l.destroy()

mainWindow()
window.mainloop()







# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# import ntpath
# import matplotlib
# import matplotlib.pylab as plt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# import pandas as pd
# from scipy.signal import savgol_filter


# class Ui_MainWindow(object):

#     fileCounter = -1

#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(800, 600)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
#         self.gridLayout_2.setObjectName("gridLayout_2")
#         self.horizontalLayout = QtWidgets.QHBoxLayout()
#         self.horizontalLayout.setObjectName("horizontalLayout")
#         self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
#         self.groupBox.setObjectName("groupBox")
#         self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
#         self.gridLayout.setObjectName("gridLayout")
#         self.treeWidget = QtWidgets.QTreeWidget(self.groupBox)
#         self.treeWidget.setObjectName("treeWidget")
#         self.gridLayout.addWidget(self.treeWidget, 0, 0, 1, 1)
#         self.horizontalLayout.addWidget(self.groupBox)
#         self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
#         self.stackedWidget.setObjectName("stackedWidget")
#         self.page = QtWidgets.QWidget()
#         self.page.setObjectName("page")
#         self.gridLayout_3 = QtWidgets.QGridLayout(self.page)
#         self.gridLayout_3.setObjectName("gridLayout_3")
#         self.tabWidget = QtWidgets.QTabWidget(self.page)
#         self.tabWidget.setObjectName("tabWidget")
#         self.tab = QtWidgets.QWidget()
#         self.tab.setObjectName("tab")
#         self.gridLayout_4 = QtWidgets.QGridLayout(self.tab)
#         self.gridLayout_4.setObjectName("gridLayout_4")
#         self.stackedWidget_2 = QtWidgets.QStackedWidget(self.tab)
#         self.stackedWidget_2.setObjectName("stackedWidget_2")
#         self.page_3 = QtWidgets.QWidget()
#         self.page_3.setObjectName("page_3")
#         self.gridLayout_5 = QtWidgets.QGridLayout(self.page_3)
#         self.gridLayout_5.setObjectName("gridLayout_5")

#         # Added Matplotlib
#         self.plotter = plt.figure()
#         self.showPlot = FigureCanvas(self.plotter)
#         self.gridLayout_5.addWidget(self.showPlot, 0, 0, 1, 1)

#         self.stackedWidget_2.addWidget(self.page_3)
#         self.page_4 = QtWidgets.QWidget()
#         self.page_4.setObjectName("page_4")
#         self.stackedWidget_2.addWidget(self.page_4)
#         self.gridLayout_4.addWidget(self.stackedWidget_2, 0, 0, 1, 1)
#         self.tabWidget.addTab(self.tab, "")
#         self.tab_2 = QtWidgets.QWidget()
#         self.tab_2.setObjectName("tab_2")
#         self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_2)
#         self.gridLayout_6.setObjectName("gridLayout_6")
#         self.checkBox_2 = QtWidgets.QCheckBox(self.tab_2)
#         self.checkBox_2.setObjectName("checkBox_2")
#         self.gridLayout_6.addWidget(self.checkBox_2, 0, 0, 1, 1)
#         self.tabWidget.addTab(self.tab_2, "")
#         self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
#         self.stackedWidget.addWidget(self.page)
#         self.page_2 = QtWidgets.QWidget()
#         self.page_2.setObjectName("page_2")
#         self.stackedWidget.addWidget(self.page_2)
#         self.horizontalLayout.addWidget(self.stackedWidget)
#         self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
#         self.menubar.setObjectName("menubar")
#         self.menuFile = QtWidgets.QMenu(self.menubar)
#         self.menuFile.setObjectName("menuFile")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#         self.actionOpen_File = QtWidgets.QAction(MainWindow)
#         self.actionOpen_File.setObjectName("actionOpen_File")
#         self.menuFile.addAction(self.actionOpen_File)
#         self.menubar.addAction(self.menuFile.menuAction())

#         self.retranslateUi(MainWindow)
#         self.tabWidget.setCurrentIndex(0)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)

#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.groupBox.setTitle(_translate("MainWindow", "Files"))
#         self.treeWidget.headerItem().setText(0, _translate("MainWindow", "File Name"))
#         self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Last Updated"))
#         self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Plot"))
#         self.checkBox_2.setText(_translate("MainWindow", "Derivative"))
#         self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Data"))
#         self.menuFile.setTitle(_translate("MainWindow", "File"))
#         self.actionOpen_File.setText(_translate("MainWindow", "Open File"))

#         self.actionOpen_File.triggered.connect(self.addnewFile)
#         self.checkBox_2.stateChanged.connect(self.state_changed)

#         # TreeWidget Specifications
#         self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
#         self.treeWidget.customContextMenuRequested.connect(self.openMenu)
#         self.treeWidget.setColumnCount(2)
#         self.treedata = QTreeWidgetItem(self.treeWidget)
#         self.fileseqList = []
#         self.taskseqList = []

#     def addfileName(self, fileName):
#         self.treedata.setText(self.fileCounter,fileName)
#         self.fileseqList.append(fileName) # This is for creating a list which stores sequence of fileName

#     def addtaskName(self, taskName):
#         self.childItem = QTreeWidgetItem(self.treedata)
#         self.childItem.setText(self.fileCounter,taskName)

#     def delete(self):
#         print(self.treeWidget.currentIndex())
#         selectrows = []
#         selectcols = []
#         # if child, if parent delete that and change the initial list, update the model rendering

#         for i in self.treeWidget.selectionModel().selectedIndexes():
#             selectrows.append(i.row())
#             selectcols.append(i.column())

#         # Implement function for deleting selected parent,child

#     def addnewFile(self):

#         self.fileName, _ = QFileDialog.getOpenFileName(None, 'Open File', ".", "Files (*.*)", options=QFileDialog.DontUseNativeDialog)
#         self.FILENAMETREE = ntpath.basename(self.fileName)
#         self.fileCounter += 1
#         self.df = pd.read_csv(self.fileName)
#         self.addfileName(self.FILENAMETREE)
#         self.plotFunction(self.df.transpose())


#     def openMenu(self, position):

#         indexes = self.treeWidget.selectedIndexes()
#         if len(indexes) > 0:

#             level = 0
#             index = indexes[0]
#             while index.parent().isValid():
#                 index = index.parent()
#                 level += 1

#         menu = QMenu()
#         if level == 0:
#             menu.addAction("Delete File")
#         elif level == 1:
#             menu.addAction("Delete Task")

#         menu.exec_(self.treeWidget.viewport().mapToGlobal(position))

#     def plotFunction(self,df):

#         self.plotter.clear()
#         ax =  self.plotter.add_subplot(111) 
#         df.T.plot(ax=ax)
#         ax.get_legend().remove()
#         self.showPlot.draw()

#     def state_changed(self, int): # List of tasks
#         if self.checkBox_2.isChecked():
#             X = savgol_filter(self.df, 11, polyorder = 2, deriv=2)
#             self.plotFunction(pd.DataFrame(X))
#             self.addtaskName("Derivative")
#         else:
#             pass




# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
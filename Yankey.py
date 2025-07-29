from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QPushButton, 
    QLabel, 
    QTextEdit, 
    QLineEdit, 
    QVBoxLayout, 
    QHBoxLayout,
    QListWidget,
    QLineEdit,
    QInputDialog,
    QMessageBox,
    QAction,
    QMenuBar
)
from PyQt5 import QtGui
import json

with open('notes.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)

with open('notes.json', 'r', encoding='utf-8') as file:
    files = json.load(file)

application = QApplication([])
mainApplicationWindow = QWidget()
mainApplicationWindow.resize(1200, 700)
mainApplicationWindow.setWindowTitle('Yankey Nodle')
mainApplicationWindow.setWindowIcon(QtGui.QIcon('logo.png'))

viewer = QWidget(mainApplicationWindow)
viewer.setWindowTitle("License")

def saveNote():
    key = listNotes.selectedItems()[0].text()
    try:
        notes[key] = {"text": noteEdit.toPlainText(), "tags":notes[key]["tags"]}
        with open("notes.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True)
    except:
        print("Save failed!")

def newNote():
    name, submit = QInputDialog.getText(mainApplicationWindow, "Create new note", "Enter new note name:")
    if name != "" and submit:
        notes[name] = {"text":"", "tags":[]}
        listNotes.addItem(name)
        with open("notes.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True)
    elif name in notes.keys():
        errorDuplicate = QMessageBox(mainApplicationWindow)
        errorDuplicate.setWindowTitle("Error")
        errorDuplicate.setIcon(QMessageBox.Critical)
        errorDuplicate.setStandardButtons(QMessageBox.Ok)
        errorDuplicate.setText('Cannot create new note - note already exists!')
        errorDuplicate.show()
    else:
        errorEmptyName = QMessageBox(mainApplicationWindow)
        errorEmptyName.setWindowTitle("Error")
        errorEmptyName.setIcon(QMessageBox.Critical)
        errorEmptyName.setStandardButtons(QMessageBox.Ok)
        errorEmptyName.setText('Cannot create new note - note name cannot be empty!')
        errorEmptyName.show()

def deleteNote():
    if listNotes.selectedItems():
        confirmDelete = QMessageBox(mainApplicationWindow)
        confirmDelete.setWindowTitle("Confirm Note Deletion")
        confirmDelete.setIcon(QMessageBox.Warning)
        confirmDelete.setStandardButtons(QMessageBox.Ok)
        confirmDelete.addButton(QMessageBox.Cancel)
        confirmDelete.setText("Are you sure you want to delete this item?\nThe item will be deleted forever! (Forever is a very long time!)")
        confirmDelete.show()
        if confirmDelete.exec() == QMessageBox.Ok:
            if key != "Demofile" or key != "Tutorial":
                key = listNotes.selectedItems()[0].text()
                del notes[key]
                listNotes.clear()
                noteEdit.clear()
                listTags.clear()
                with open("notes.json", "w", encoding="utf-8") as file:
                    json.dump(notes, file, sort_keys=True)
                    listNotes.addItems(notes.keys())
            else:
                errorNOCB2 = QMessageBox(mainApplicationWindow)
                errorNOCB2.setWindowTitle("Error")
                errorNOCB2.setIcon(QMessageBox.Warning)
                errorNOCB2.setText("Cannot delete a system note!")
                errorNOCB2.setStandardButtons(QMessageBox.Ok)
                errorNOCB2.show()

def readLicense():
    textArea = QTextEdit()
    textArea.setReadOnly(True)
    try:
        with open("LICENSE", "r", encoding="utf-8") as file:
            licenseContents = file.read()
        textArea.setText(licenseContents)
        viewerLayout = QVBoxLayout()
        viewerLayout.addWidget(textArea)
        viewer.show()
    except:
        errorLicense = QMessageBox(mainApplicationWindow)
        errorLicense = QMessageBox(mainApplicationWindow)
        errorLicense.setWindowTitle("Error")
        errorLicense.setIcon(QMessageBox.Critical)
        errorLicense.setText("The license is not found")
        errorLicense.setStandardButtons(QMessageBox.Abort)
        errorLicense.show()

listNotesLabel = QLabel('Your notes:')
listNotes = QListWidget()
newNoteButton = QPushButton('New note')
deleteNoteButton = QPushButton('Delete note')
saveNoteButton = QPushButton('Save note')

listTagsLabel = QLabel('Your tags:')
listTags = QListWidget()
searchTagLine = QLineEdit()
createTagButton = QPushButton('Create tag')
untagButton = QPushButton('Untag from note')
deleteTagButton = QPushButton('Delete tag')
searchTagButton = QPushButton('Search note by tag')

menubar = QMenuBar()

fileMenu = menubar.addMenu("File")
tagMenu = menubar.addMenu("Tags")
helpMenu = menubar.addMenu("Help")

newAction = QAction("New", mainApplicationWindow)
saveAction = QAction("Save", mainApplicationWindow)
deleteAction = QAction("Save", mainApplicationWindow)
helpAction = QAction("Help", mainApplicationWindow)
exitAction = QAction("Exit", mainApplicationWindow)

newTagAction = QAction("New Tag", mainApplicationWindow)
deleteTagAction = QAction("Delete Tag", mainApplicationWindow)
helpTagAction = QAction("Help", mainApplicationWindow)

aboutAction = QAction("About", mainApplicationWindow)
licenseAction = QAction("License", mainApplicationWindow)

newAction.triggered.connect(newNote)
saveAction.triggered.connect(saveNote)
deleteAction.triggered.connect(deleteNote)
helpAction.triggered.connect(application.quit)
exitAction.triggered.connect(application.quit)

licenseAction.triggered.connect(readLicense)

fileMenu.addAction(newAction)
fileMenu.addAction(saveAction)
fileMenu.addSeparator()
fileMenu.addAction(helpAction)
fileMenu.addAction(exitAction)

tagMenu.addAction(newTagAction)
tagMenu.addAction(deleteTagAction)

helpMenu.addAction(aboutAction)
helpMenu.addAction(licenseAction)

col1 = QVBoxLayout()
listLayout = QVBoxLayout()

listLayout.addWidget(listNotesLabel)
listLayout.addWidget(listNotes)

hLine1 = QHBoxLayout()

hLine1.addWidget(newNoteButton)
hLine1.addWidget(deleteNoteButton)

listLayout.addLayout(hLine1)
listLayout.addWidget(saveNoteButton)

listLayout.addWidget(listTagsLabel)
listLayout.addWidget(listTags)

hLine2 = QHBoxLayout()
hLine2.addWidget(createTagButton)
hLine2.addWidget(untagButton)
hLine2.addWidget(deleteTagButton)
hLine2.addWidget(searchTagButton)

listLayout.addLayout(hLine2)
listLayout.addWidget(searchTagLine)

noteEdit = QTextEdit()
col1.addWidget(noteEdit)

mainLayout = QHBoxLayout()
mainLayout.addWidget(menubar)
mainLayout.addLayout(col1, stretch=8)
mainLayout.addLayout(listLayout, stretch=2)

mainApplicationWindow.setLayout(mainLayout)

listNotes.addItems(notes)
def selectNote():
    key = listNotes.selectedItems()[0].text()
    text = notes[key]["text"]
    tags = notes[key]["tags"]
    noteEdit.clear()
    noteEdit.setText(text)
    listTags.clear()
    listTags.addItems(tags)

def searchTag():
    listNotes.clear()
    noteEdit.clear()
    listNotes.clear()
    if searchTagButton.text() == "Search note by tag":
        tag = searchTagLine.text()
        filterNotes = {}
        for key in notes:
            if tag in notes[key]["tags"]:
                filterNotes[key] = notes[key]
        listNotes.addItems(filterNotes)
        searchTagButton.setText("Clear search")
    else:
        listNotes.addItems(notes)
        searchTagButton.setText("Search note by tag")


listNotes.itemClicked.connect(selectNote)
saveNoteButton.clicked.connect(saveNote)
newNoteButton.clicked.connect(newNote)
deleteNoteButton.clicked.connect(deleteNote)
searchTagButton.clicked.connect(searchTag)
searchTagLine.setPlaceholderText("Search tag (e. g. 'shopping', 'tutorial', 'important')")
mainApplicationWindow.show()
application.exec_()
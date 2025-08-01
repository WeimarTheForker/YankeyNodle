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
with open("LICENSE", "r", encoding="utf-8") as file:
    licenseContents = str(file.read())
with open("initial.txt", "r", encoding="utf-8") as file:
    initialContents = str(file.read())

application = QApplication([])
mainApplicationWindow = QWidget()
mainApplicationWindow.resize(1200, 700)
mainApplicationWindow.setWindowTitle('Yankey Nodle')
mainApplicationWindow.setWindowIcon(QtGui.QIcon('logo.png'))

viewer = QWidget()
viewer.setFixedSize(800, 680)
aboutviewer = QWidget()
aboutviewer.setFixedSize(600, 180)

def closeLicense():
    viewer.hide()

textArea = QTextEdit()
textArea.setReadOnly(True)
viewer.setWindowTitle("License")
textArea.setText(licenseContents)
viewerLayout = QVBoxLayout()
viewerLayout.addWidget(textArea)
viewerButtonLayout = QVBoxLayout()
viewerButtonLayout.addStretch(8)
understand = QPushButton("I Understand")
viewerButtonLayout.addWidget(understand)
mainLayout = QHBoxLayout()
mainLayout.addLayout(viewerLayout)
mainLayout.addLayout(viewerButtonLayout)
viewer.setLayout(mainLayout)
understand.clicked.connect(closeLicense)

textArea = QLabel()
textArea.setAlignment(Qt.AlignTop)
aboutviewer.setWindowTitle("About")
with open("aboutfile.txt", "r", encoding="utf-8") as file:
    aboutContents = file.read()
textArea.setText(aboutContents)
aboutviewerLayout = QVBoxLayout()
aboutviewerLayout.addWidget(textArea)
aboutviewer.setLayout(aboutviewerLayout)

def saveNote():
    key = listNotes.selectedItems()[0].text()
    try:
        notes[key] = {"text": noteEdit.toPlainText(), "tags":notes[key]["tags"]}
        with open("notes.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True)
    except Exception as exception:
        errorNOCB5 = QMessageBox(mainApplicationWindow)
        errorNOCB5.setWindowTitle("Error")
        errorNOCB5.setIcon(QMessageBox.Critical)
        errorNOCB5.setText(f"Try-catch error while saving note!\n{exception}")
        errorNOCB5.setStandardButtons(QMessageBox.Abort)
        errorNOCB5.show()

def newNote():
    try:
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
    except Exception as exception:
        errorNOCB5 = QMessageBox(mainApplicationWindow)
        errorNOCB5.setWindowTitle("Error")
        errorNOCB5.setIcon(QMessageBox.Critical)
        errorNOCB5.setText(f"Try-catch error while creating new note!\n{exception}")
        errorNOCB5.setStandardButtons(QMessageBox.Abort)
        errorNOCB5.show()
        

def deleteNote():
    try:
        if listNotes.selectedItems():
            confirmDelete = QMessageBox(mainApplicationWindow)
            confirmDelete.setWindowTitle("Confirm Note Deletion")
            confirmDelete.setIcon(QMessageBox.Warning)
            confirmDelete.setStandardButtons(QMessageBox.Ok)
            confirmDelete.addButton(QMessageBox.Cancel)
            confirmDelete.setText("Are you sure you want to delete this item?\nThe item will be deleted forever! (Forever is a very long time!)")
            confirmDelete.show()
            if confirmDelete.exec() == QMessageBox.Ok:
                key = listNotes.selectedItems()[0].text()
                del notes[key]
                listNotes.clear()
                noteEdit.clear()
                listTags.clear()
                with open("notes.json", "w", encoding="utf-8") as file:
                    json.dump(notes, file, sort_keys=True)
                    listNotes.addItems(notes.keys())
    except Exception as exception:
        errorNOCB4 = QMessageBox(mainApplicationWindow)
        errorNOCB4.setWindowTitle("Error")
        errorNOCB4.setIcon(QMessageBox.Critical)
        errorNOCB4.setText(f"Try-catch error while deleting note!\n{exception}")
        errorNOCB4.setStandardButtons(QMessageBox.Abort)
        errorNOCB4.show()

def readLicense():
    if initialContents == licenseContents:
        viewer.show()
    else:
        errorNOCB3 = QMessageBox(mainApplicationWindow)
        errorNOCB3.setWindowTitle("Error")
        errorNOCB3.setIcon(QMessageBox.Critical)
        errorNOCB3.setText("The license has been modified.")
        errorNOCB3.setStandardButtons(QMessageBox.Abort)
        errorNOCB3.show()

def closeAbout():
    aboutviewer.hide()

def readAbout():
    aboutviewer.show()

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

aboutAction.triggered.connect(readAbout)
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
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QInputDialog
import json


def show_note():
    name = list_note.selectedItems()[0].text()
    field_text.setText(notes[name]['текст'])
    list_tag.clear()
    list_tag.addItems(notes[name]['теги'])

def add_note():
    note_name, result = QInputDialog.getText(main_win, 'Добавить заметку', 'Название заметки')
    if note_name != '' and result:
        notes[note_name] = {'текст':'','теги':[]}
        list_note.addItem(note_name)

def del_note():
    if list_note.selectedItems():
        name = list_note.selectedItems()[0].text()
        del notes[name]
        list_note.clear()
        list_tag.clear()
        field_text.clear()
        list_note.addItems(notes)
        with open('note.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Заметка для удаления не выбрана')

def save_note():
    if list_note.selectedItems():
        name = list_note.selectedItems()[0].text()
        notes[name]['текст'] = field_text.toPlainText()
        with open('note.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Заметка для сохранения не выбрана')

def add_tag():
    if list_note.selectedItems():
        name = list_note.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[name]['теги']:
            list_tag.addItem(tag)
            notes[name]['теги'].append(tag)
        with open('note.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Заметка для добавления тега не выбрана')

def del_tag():
    if list_tag.selectedItems():
        name = list_note.selectedItems()[0].text()
        tag = list_tag.selectedItems()[0].text()
        notes[name]['теги'].remove(tag)
        list_tag.clear()
        list_tag.addItems(notes[name]['теги'])
        with open('note.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Заметка для открепление тега не выбрана')

def find_tag():
    tag = field_tag.text()
    if btn_find_tag.text() == 'Искать замиетки по тегу' and tag:
        notes_filter = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filter[note] = notes[note]
        btn_find_tag.setText('Сбросить поиск')
        list_note.clear()
        list_tag.clear()
        list_note.addItems(notes_filter)
    elif btn_find_tag.text() == 'Сбросить поиск':
        list_note.clear()
        list_tag.clear()
        field_tag.clear()
        list_note.addItems(notes)
        btn_find_tag.setText('Искать замиетки по тегу')
    else:
        pass


app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Умные заметки')
main_win.resize(900,600)

notes = {
    'Дорогой дневник':{
        'текст':'День первый: <3',
        'теги':['1','<3']
    }
}
# with open('note.json', 'w') as file:     добавили инфу из словаря в json
#     json.dump(notes, file)

# начинка
field_text = QTextEdit()  #текстовое поле / поле для заметок
lb_list_note = QLabel('Список заметок')  #Лабел список заметок
list_note = QListWidget() #список с названием заметок
btn_add_note = QPushButton('Создать заметку') #кнопка создать заметку
btn_del_note = QPushButton('Удалить заметку') #кнопка удалить заметку
btn_save_note = QPushButton('Сохранить заметку') #кнопка сохранить заметку
lb_list_tag = QLabel('Список тегов')   #надпись Список тегов
list_tag = QListWidget()  #список тегов
field_tag = QLineEdit()  #поле для тега
field_tag.setPlaceholderText('Введите тег...')
btn_add_tag = QPushButton('Добавить к заметке') #кнопка добавить тег
btn_del_tag = QPushButton('Открепить от заметки') #кнопка удалить тег
btn_find_tag = QPushButton('Искать замиетки по тегу') #кнопка искать по тегу



# Layouts
main_layout = QHBoxLayout()
vlt1 = QVBoxLayout()
vlt2 = QVBoxLayout()
hlt1 = QHBoxLayout()
hlt2 = QHBoxLayout()
hlt3 = QHBoxLayout()
hlt4 = QHBoxLayout()
vlt1.addWidget(field_text)
hlt1.addWidget(btn_add_note)
hlt1.addWidget(btn_del_note)
hlt2.addWidget(btn_save_note)
hlt3.addWidget(btn_add_tag)
hlt3.addWidget(btn_del_tag)
hlt4.addWidget(btn_find_tag)
vlt2.addWidget(lb_list_note)
vlt2.addWidget(list_note)
vlt2.addLayout(hlt1)
vlt2.addLayout(hlt2)
vlt2.addWidget(lb_list_tag)
vlt2.addWidget(list_tag)
vlt2.addWidget(field_tag)
vlt2.addLayout(hlt3)
vlt2.addLayout(hlt4)
main_layout.addLayout(vlt1,stretch=3)
main_layout.addLayout(vlt2,stretch=2)
main_win.setLayout(main_layout)

list_note.itemClicked.connect(show_note)
btn_add_note.clicked.connect(add_note)
btn_del_note.clicked.connect(del_note)
btn_save_note.clicked.connect(save_note)
btn_add_tag.clicked.connect(add_tag)
btn_del_tag.clicked.connect(del_tag)
btn_find_tag.clicked.connect(find_tag)



with open('note.json', 'r') as file:
    notes = json.load(file)
list_note.addItems(notes)

main_win.show()
app.exec_()
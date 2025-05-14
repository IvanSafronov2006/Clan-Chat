import sys
import sqlite3

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem


class Check_window(QMainWindow):  # Закончено
    def __init__(self):
        super().__init__()
        uic.loadUi('u_check_window.ui', self)
        self.check = 0
        self.pushButton_to_start.clicked.connect(self.start)
        self.radioButton_gateway.toggled.connect(self.onClicked)
        self.radioButton_registration.toggled.connect(self.onClicked)
        self.setWindowIcon(QtGui.QIcon('icon1.png'))
        

    def start(self):
        if self.check == 1:
            gateway_window.show()
            self.close()
        elif self.check == 2:
            regisration_window.show()
            self.close()

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            if str(radioButton.text()) == 'Войти':
                self.check = 1
            else:
                self.check = 2


class Choose_window(QMainWindow):  # Закончено
    def __init__(self, basa_d):
        super().__init__()
        uic.loadUi('u_choose_window.ui', self)
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        self.pushButton_to_gateway.clicked.connect(self.gateway)
        self.pushButton_to_create.clicked.connect(self.create)
        self.setWindowIcon(QtGui.QIcon('icon1.png'))

    def gateway(self):
        seek_window.show()
        self.close()

    def create(self):
        create_window.show()
        self.close()


class Group_window(QMainWindow):  # Закончено
    def __init__(self, basa_d):
        super().__init__()
        uic.loadUi('u_group_window.ui', self)
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        self.setWindowIcon(QtGui.QIcon('icon1.png'))
        self.id_people = 0
        self.gruppa_info = []
        self.pushButton_4.clicked.connect(self.edit)
        self.pushButton_3.clicked.connect(self.new_p)
        self.pushButton_2.clicked.connect(self.new_a)
        self.pushButton.clicked.connect(self.go_out)
        self.pushButton_5.clicked.connect(self.soxr)
        self.pushButton_6.clicked.connect(self.spis)

    def spis(self):
        uu.idd(self.gruppa_info[0][0])
        uu.show()

    def soxr(self):
        self.basa_d.commit()
        news1 = self.basa_cursor.execute('''SELECT * FROM news WHERE id_group = (?)''', (self.gruppa_info[0][0],)).fetchall()
        news = []
        for i in news1:
            id_name = news1[news1.index(i)][1]
            name = self.basa_cursor.execute('''SELECT * FROM people WHERE id = (?)''', (id_name,)).fetchall()
            news.append(str(name[0][1]) + ': ' + str(i[2]) + '\n\n')
        self.plainTextEdit.setPlainText(''.join(news))

    def id(self, id_p):
        self.id_people = id_p
        self.gruppa_info = self.basa_cursor.execute('''SELECT * FROM people_group WHERE id_people = (?)''', (self.id_people,)).fetchall()
        if self.gruppa_info[0][-2] == 0:
            self.pushButton_4.hide()
            self.pushButton_2.hide()
        else:
            self.pushButton_4.show()
            self.pushButton_2.show()
        self.lcdNumber.display(int(self.gruppa_info[0][-1]))
        news1 = self.basa_cursor.execute('''SELECT * FROM news WHERE id_group = (?)''', (self.gruppa_info[0][0],)).fetchall()
        news = []
        for i in news1:
            id_name = news1[news1.index(i)][1]
            name = self.basa_cursor.execute('''SELECT * FROM people WHERE id = (?)''', (id_name,)).fetchall()
            news.append(str(name[0][1]) + ': ' + str(i[2]) + '\n\n')
        self.plainTextEdit.setPlainText(''.join(news))

    def edit(self):
        edit_group_window.id_g(self.gruppa_info[0][0])
        edit_group_window.show()

    def new_p(self):
        if self.lineEdit.text().strip() != '':
            self.basa_cursor.execute('''INSERT INTO news (id_group, id_people, new) VALUES (?, ?, ?)''', (self.gruppa_info[0][0], self.id_people, self.lineEdit.text()))
            news1 = self.basa_cursor.execute('''SELECT * FROM news WHERE id_group = (?)''', (self.gruppa_info[0][0],)).fetchall()
            self.basa_d.commit()
            news = []
            for i in news1:
                id_name = news1[news1.index(i)][1]
                name = self.basa_cursor.execute('''SELECT * FROM people WHERE id = (?)''', (id_name,)).fetchall()
                news.append(str(name[0][1]) + ': ' + str(i[2]) + '\n\n')
            self.plainTextEdit.setPlainText(''.join(news))

    def new_a(self):
        if self.lineEdit.text().strip() != '':
            self.basa_cursor.execute('''INSERT INTO news (id_group, id_people, new) VALUES (?, ?, ?)''', (self.gruppa_info[0][0], 1, self.lineEdit.text()))
            news1 = self.basa_cursor.execute('''SELECT * FROM news WHERE id_group = (?)''', (self.gruppa_info[0][0],)).fetchall()
            self.basa_d.commit()
            news = []
            for i in news1:
                id_name = news1[news1.index(i)][1]
                name = self.basa_cursor.execute('''SELECT * FROM people WHERE id = (?)''', (id_name,)).fetchall()
                news.append(str(name[0][1]) + ': ' + str(i[2]) + '\n\n')
            self.plainTextEdit.setPlainText(''.join(news))

    def go_out(self):
        kolvo = self.basa_cursor.execute('''SELECT * FROM people_group WHERE id_group = (?)''', (self.gruppa_info[0][0],)).fetchall()
        result = self.basa_cursor.execute('''SELECT status FROM people_group WHERE id_group = (?)''', (self.gruppa_info[0][0],)).fetchall()
        r = []
        for i in result:
            r.append(i[0])
        if len(kolvo) != 1:
            if r.count(1) == 1:
                if self.gruppa_info[0][-2] == 0:
                    self.basa_cursor.execute('''UPDATE people SET gr = (?) WHERE id = (?)''', (0, self.id_people))
                    self.basa_d.commit()
                    self.basa_cursor.execute('''DELETE FROM people_group WHERE id_people = (?)''', (self.id_people,))
                    self.basa_d.commit()
                else:
                    self.basa_cursor.execute('''UPDATE people SET gr = (?) WHERE id = (?)''', (0, self.id_people))
                    self.basa_d.commit()
                    self.basa_cursor.execute('''DELETE FROM people_group WHERE id_people = (?)''', (self.id_people,))
                    self.basa_d.commit()
                    id_names = self.basa_cursor.execute('''SELECT * FROM people_group WHERE id_group = (?)''', (self.gruppa_info[0][0],)).fetchall()
                    self.basa_cursor.execute('''UPDATE people_group SET status = (?) WHERE id_people = (?)''', (1, id_names[0][1]))
                    self.basa_d.commit()
            else:
                self.basa_cursor.execute('''UPDATE people SET gr = (?) WHERE id = (?)''', (0, self.id_people))
                self.basa_d.commit()
                self.basa_cursor.execute('''DELETE FROM people_group WHERE id_people = (?)''', (self.id_people,))
                self.basa_d.commit()
        else:
            self.basa_cursor.execute('''UPDATE people SET gr = (?) WHERE id = (?)''', (0, self.id_people))
            self.basa_d.commit()
            self.basa_cursor.execute('''DELETE FROM people_group WHERE id_people = (?)''', (self.id_people,))
            self.basa_d.commit()
            self.basa_cursor.execute('''DELETE FROM gruppa WHERE id = (?)''', (self.gruppa_info[0][0],))
            self.basa_d.commit()
            self.basa_cursor.execute('''DELETE FROM news WHERE id_group = (?)''', (self.gruppa_info[0][0],))
            self.basa_d.commit()
        choose_window.show()
        seek_window.id(self.id_people)
        self.close()
        
            

        
class Edit_group_window(QMainWindow):  # Закончено
    def __init__(self, basa_d):
        super().__init__()
        uic.loadUi('u_edit_group_window.ui', self)
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        self.setWindowIcon(QtGui.QIcon('icon1.png'))
        self.id_group = 0
        self.pushButton.clicked.connect(self.vubr)
        self.pushButton_4.clicked.connect(self.admin)
        self.pushButton_3.clicked.connect(self.add_o)
        self.pushButton_2.clicked.connect(self.delet)
        self.pushButton_5.clicked.connect(self.chat)

    def chat(self):
        self.basa_cursor.execute('''DELETE FROM news WHERE id_group = (?)''', (self.id_group,))

    def delet(self):
        b = self.basa_cursor.execute('''SELECT * FROM people WHERE name = (?)''', (self.comboBox.currentText(),)).fetchall()
        c = self.basa_cursor.execute('''SELECT status FROM people_group WHERE id_people = (?)''', (b[0][0],)).fetchall()
        if b[0][0] != 1:
            self.basa_cursor.execute('''UPDATE people SET gr = (?) WHERE id = (?)''', (0, b[0][0]))
            self.basa_d.commit()
            self.basa_cursor.execute('''DELETE FROM people_group WHERE id_people = (?)''', (b[0][0],))
            self.basa_d.commit()
            self.close()

    def add_o(self):
        try:
            a = int(self.lineEdit.text())
            b = self.basa_cursor.execute('''SELECT id FROM people WHERE name = (?)''', (self.comboBox.currentText(),)).fetchall()
            c = self.basa_cursor.execute('''SELECT marks FROM people_group WHERE id_people = (?)''', (b[0][0],)).fetchall()
            if abs(c[0][0] + a) <= 9999:
                self.basa_cursor.execute('''UPDATE people_group SET marks = (?) WHERE id_people = (?)''', (c[0][0] + a, b[0][0]))
            b = self.basa_cursor.execute('''SELECT id FROM people WHERE name = (?)''', (self.comboBox.currentText(),)).fetchall()
            c = self.basa_cursor.execute('''SELECT marks FROM people_group WHERE id_people = (?)''', (b[0][0],)).fetchall()
            self.lcdNumber.display(int(c[0][0]))
            self.basa_d.commit()
        except:
            pass
        

    def vubr(self):
        b = self.basa_cursor.execute('''SELECT id FROM people WHERE name = (?)''', (self.comboBox.currentText(),)).fetchall()
        c = self.basa_cursor.execute('''SELECT marks FROM people_group WHERE id_people = (?)''', (b[0][0],)).fetchall()
        self.lcdNumber.display(int(c[0][0]))
        self.basa_d.commit()
        b = self.basa_cursor.execute('''SELECT id FROM people WHERE name = (?)''', (self.comboBox.currentText(),)).fetchall()
        c = self.basa_cursor.execute('''SELECT status FROM people_group WHERE id_people = (?)''', (b[0][0],)).fetchall()
        self.basa_d.commit()
        b = self.basa_cursor.execute('''SELECT id FROM people WHERE name = (?)''', (self.comboBox.currentText(),)).fetchall()
        c = self.basa_cursor.execute('''SELECT status FROM people_group WHERE id_people = (?)''', (b[0][0],)).fetchall()
        if c[0][0] == 0:
            self.pushButton_4.setText(' Назначить администратором ')
        else:
            self.pushButton_4.setText(' Сделать участником ')

    def admin(self):
        b = self.basa_cursor.execute('''SELECT id FROM people WHERE name = (?)''', (self.comboBox.currentText(),)).fetchall()
        c = self.basa_cursor.execute('''SELECT status FROM people_group WHERE id_people = (?)''', (b[0][0],)).fetchall()
        self.basa_cursor.execute('''UPDATE people_group SET status = (?) WHERE id_people = (?)''', (1 - c[0][0], b[0][0]))
        self.basa_d.commit()
        b = self.basa_cursor.execute('''SELECT id FROM people WHERE name = (?)''', (self.comboBox.currentText(),)).fetchall()
        c = self.basa_cursor.execute('''SELECT status FROM people_group WHERE id_people = (?)''', (b[0][0],)).fetchall()
        if c[0][0] == 0:
            self.pushButton_4.setText(' Назначить администратором ')
        else:
            self.pushButton_4.setText(' Сделать участником ')

    def id_g(self, id_group):
        self.id_group = id_group
        b = self.basa_cursor.execute('''SELECT id_people FROM people_group WHERE id_group = (?)''', (id_group,)).fetchall()
        c = []
        a = []
        for i in b:
            a.append(i[0])
        for i in a:
            d = self.basa_cursor.execute('''SELECT name FROM people WHERE id = (?)''', (i,)).fetchall()
            c.append(d[0][0])
        self.comboBox.clear()
        self.comboBox.addItems(c)
        self.basa_d.commit()


class Seek_window(QMainWindow): # Закончено
    def __init__(self, basa_d):
        super().__init__()
        uic.loadUi('u_window_for_seek.ui', self)
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        self.setWindowIcon(QtGui.QIcon('icon1.png'))
        self.pushButton_2.clicked.connect(self.poisk)
        self.pushButton_3.clicked.connect(self.info)
        self.pushButton.clicked.connect(self.add)
        result1 = self.basa_cursor.execute('''SELECT name FROM gruppa''').fetchall()
        result = []
        spisok = []
        for i in result1:
            i = list(i)
            result.append(''.join(i))
        for i in result:
            spisok.append(i)
        self.comboBox.addItems(spisok)
        self.id_people = 0

    def info(self):
        try:
            a = self.comboBox.currentText()
            result = self.basa_cursor.execute('''SELECT opisanie FROM gruppa WHERE name = (?)''', (a, )).fetchall()
            self.plainTextEdit.setPlainText(str(result[0][0]))
        except:
            self.plainTextEdit.setPlainText('Группа не выбрана')

    def poisk(self):
        a = self.lineEdit.text()
        self.comboBox.clear()
        result1 = self.basa_cursor.execute('''SELECT name FROM gruppa''').fetchall()
        result = []
        spisok = []
        for i in result1:
            i = list(i)
            result.append(str(i))
        for i in result:
            if (a in i) or (a == i):
                spisok.append(i)
        self.comboBox.addItems(spisok)

    def id(self, id_p):
        self.id_people = id_p

    def add(self):
        try:
            a = self.comboBox.currentText()
            self.basa_cursor.execute('''UPDATE people SET gr = (?) WHERE id = (?)''', (1, self.id_people))
            self.basa_d.commit()
            c = 0
            b = self.id_people
            result1 = self.basa_cursor.execute('''SELECT * FROM gruppa WHERE name = (?)''', (a,)).fetchall()
            self.basa_cursor.execute('''INSERT INTO people_group (id_group, id_people, status) VALUES (?, ?, ?)''', (result1[0][0], b, c))
            self.basa_d.commit()
            group_window.show()
            group_window.id(b)
            self.close()
        except:
            pass
        


class Create_window(QMainWindow):    # Закончено
    def __init__(self, basa_d):
        super().__init__()
        uic.loadUi('u_create_window.ui', self)
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        self.pushButton.clicked.connect(self.create)
        self.setWindowIcon(QtGui.QIcon('icon1.png'))
        self.id_people = 0


    def create(self):
        spis_with_names1 = self.basa_cursor.execute('''SELECT name FROM gruppa''').fetchall()
        spis_with_names = []
        for i in spis_with_names1:
            i = list(i)
            spis_with_names.append(''.join(i))
        if (self.lineEdit.text().strip().lower() not in spis_with_names) and (self.lineEdit.text().strip().lower() != ''):
            a = self.lineEdit.text()
            b = self.plainTextEdit.toPlainText()
            if b.strip() != '':
                self.basa_cursor.execute('''INSERT INTO gruppa (name, opisanie) VALUES (?, ?)''', (a, b))
            else:
                b = 'Просто группа'
                self.basa_cursor.execute('''INSERT INTO gruppa (name, opisanie) VALUES (?, ?)''', (a, b))
            self.basa_d.commit()
            grupa = self.basa_cursor.execute('''SELECT id FROM gruppa WHERE name = (?)''', (a,)).fetchall()
            peop = self.id_people
            a = grupa[0][0]
            b = peop
            c = 1
            self.basa_cursor.execute('''INSERT INTO people_group (id_group, id_people, status) VALUES (?, ?, ?)''', (a, b, c))
            self.basa_cursor.execute('''UPDATE people SET gr = (?) WHERE id = (?)''', (1, b))
            self.basa_d.commit()
            group_window.show()
            group_window.id(b)
            self.close()
        else:
            self.label.setText('Выберете другое название')

    def id(self, id_p):
        self.id_people = id_p


class Regisration_window(QMainWindow):   # Закончено
    def __init__(self, basa_d):
        super().__init__()
        self.state = -1
        uic.loadUi('u_window_of_registration.ui', self)
        self.pushButton.clicked.connect(self.go)
        self.basa_d = basa_d
        self.basa_cursor = self.basa_d.cursor()
        self.basa_d.commit()
        self.setWindowIcon(QtGui.QIcon('icon1.png'))

    def go(self):
        alf = 'qwertyuioplkjhgfdsazxcvbnmйцукенгшщзхъэждлорпавыфячсмитьбю'
        spis_with_niks1 = basa_cursor.execute('''SELECT name FROM people''').fetchall()
        spis_with_niks = []
        for i in spis_with_niks1:
            i = list(i)
            spis_with_niks.append(str(''.join(i)).lower())
        if self.lineEdit_for_nik.text().lower() not in spis_with_niks:
            if len(self.lineEdit_for_login.text()) >= 6:
                if ' ' not in self.lineEdit_for_login.text() and '\t' not in self.lineEdit_for_login.text():
                    if ' ' not in self.lineEdit_for_password.text() and '\t' not in self.lineEdit_for_password.text():
                        if self.lineEdit_for_password.text() != self.lineEdit_for_login.text():
                            if (self.lineEdit_for_password.text() != '') and self.lineEdit_for_login.text() != '' and self.lineEdit_for_nik.text() not in ['', ' ']:
                                spis_with_login1 = basa_cursor.execute('''SELECT login FROM people''').fetchall()
                                spis_with_login = []
                                for i in spis_with_login1:
                                    i = list(i)
                                    spis_with_login.append(''.join(i))
                                if self.lineEdit_for_login.text() not in spis_with_login:
                                    c1, c2, c3 = 0, 0, 0
                                    for i in str(self.lineEdit_for_nik.text()):
                                        if i in alf:
                                            c1 = 1
                                    for i in str(self.lineEdit_for_login.text()):
                                        if i in alf:
                                            c2 = 1
                                    for i in str(self.lineEdit_for_password.text()):
                                        if i in alf:
                                            c3 = 1
                                    if (c1 != 0) and (c2 != 0) and (c3 != 0):
                                        a, b, c = str(self.lineEdit_for_nik.text()), str(self.lineEdit_for_login.text()), str(self.lineEdit_for_password.text())
                                        self.basa_cursor.execute('''INSERT INTO people (name, login, password, gr) VALUES (?, ?, ?, ?)''', (a.strip(), b.strip(), c.strip(), 0))
                                        self.basa_d.commit()
                                        choose_window.show()
                                        spis = basa_cursor.execute('''SELECT * FROM people WHERE login = (?)''', (b.strip(),)).fetchall()
                                        create_window.id(spis[-1][0])
                                        seek_window.id(spis[-1][0])
                                        self.close()
                                    else:
                                        self.label_for_error.setText('В каждом поле должна быть хотябы одна буква русского или английского алфавита ')
                                else:
                                    self.label_for_error.setText('Ваш логин уже занят                                                           ')
                            else:
                                self.label_for_error.setText('Ваш логин/пароль/имя не может быть пустым                                     ')
                        else:
                            self.label_for_error.setText('Ваш логин не может быть равен паролю                                          ')
                    else:
                        self.label_for_error.setText('Ваш пароль содержит пробелы или табуляции                                     ')
                else:
                    self.label_for_error.setText('Ваш логин содержит пробелы или табуляции                                      ')
            else:
                self.label_for_error.setText('Ваш логин слишком короткий                                                    ')
        else:
            self.label_for_error.setText('Данное имя уже используется                                                   ')
        self.basa_d.commit()
                        

class Gateway_window(QMainWindow):   # Закончено
    def __init__(self, basa_d):
        super().__init__()
        uic.loadUi('u_window_of_gateway.ui', self)
        self.pushButton_go.clicked.connect(self.go)
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        self.setWindowIcon(QtGui.QIcon('icon1.png'))


    def go(self):
        spis_with_login1 = basa_cursor.execute('''SELECT login FROM people''').fetchall()
        spis_with_login = []
        if (self.lineEdit_for_login.text() == 'й') and (self.lineEdit_for_password.text() == 'й'):
            admin.show()
            self.close()
        else:
            for i in spis_with_login1:
                i = list(i)
                spis_with_login.append(''.join(i))
            if self.lineEdit_for_login.text() in spis_with_login or self.lineEdit_for_login.text() == 'й':   # Проверка не на новость
                password = self.basa_cursor.execute('''SELECT * FROM people WHERE login = (?)''', (self.lineEdit_for_login.text(),)).fetchall()
                if password[0][-2] == self.lineEdit_for_password.text():
                    if password[0][-1] == 0:
                        choose_window.show()
                        spis = self.basa_cursor.execute('''SELECT * FROM people''').fetchall()
                        create_window.id(spis[-1][0])
                        seek_window.id(spis[-1][0])
                        self.close()
                    else:
                        group_window.show()
                        group_window.id(password[0][0])
                        self.close()
                else:
                    self.label_for_error.setText('Неверный пароль')
            else:
                self.label_for_error.setText('Несуществующий логин')


class U(QMainWindow):   # Закончено
    def __init__(self, basa_d):
        super().__init__()
        uic.loadUi('u.ui', self)
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        self.iddd = 0
        self.setWindowIcon(QtGui.QIcon('icon1.png'))

    def idd(self, a):
        self.iddd = a
        b = self.basa_cursor.execute('''SELECT * FROM people_group WHERE id_group = (?)''', (self.iddd,)).fetchall()
        c = self.basa_cursor.execute('''SELECT * FROM gruppa WHERE id = (?)''', (self.iddd,)).fetchall()
        self.label.setText(c[0][2])
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Имя", "Очки", "Статус"])
        self.tableWidget.setRowCount(len(b))
        for i in range(len(b)):
            a1 = self.basa_cursor.execute('''SELECT * FROM people WHERE id = (?)''', (b[i][1],)).fetchall()
            b1 = self.basa_cursor.execute('''SELECT * FROM people_group WHERE id_people = (?)''', (b[i][1],)).fetchall()
            self.tableWidget.setItem(i, 0, QTableWidgetItem(a1[0][1]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(b1[0][3])))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(list(['Участник', 'Администратор'])[b1[0][2]]))


class Admin_window(QMainWindow):
    def __init__(self, basa_d):
        super().__init__()
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        uic.loadUi('u_admin_window.ui', self)
        self.initUI()
        
    def initUI(self):
        self.iddd = 0
        self.setWindowIcon(QtGui.QIcon('icon1.png'))
        self.pushButton.clicked.connect(self.del_group)
        self.pushButton_4.clicked.connect(self.info)
        self.pushButton_3.clicked.connect(self.mess)
        b = self.basa_cursor.execute('''SELECT * FROM gruppa''').fetchall()
        c = []
        for i in b:
            c.append(i[1])
        self.comboBox.addItems(c)

    def info(self):
        a = self.comboBox.currentText()
        b = self.basa_cursor.execute('''SELECT * FROM gruppa WHERE name = (?)''', (a,)).fetchall()[:]
        uu.idd(b[0][0])
        uu.show()

    def mess(self):
        a = self.lineEdit_2.text().upper().strip()
        b = self.basa_cursor.execute('''SELECT * FROM gruppa''').fetchall()
        for i in b:
            self.basa_cursor.execute('''INSERT INTO news (id_group, id_people, new) VALUES (?, ?, ?)''', (i[0], 1, a))
        self.basa_d.commit()
        
    def del_group(self):
        a = self.comboBox.currentText()
        b = self.basa_cursor.execute('''SELECT * FROM gruppa WHERE name = (?)''', (a,)).fetchall()[:]
        self.basa_cursor.execute('''DELETE FROM gruppa WHERE name = (?)''', (b[0][1],))
        self.basa_d.commit()
        c = self.basa_cursor.execute('''SELECT * FROM people_group WHERE id_group = (?)''', (b[0][0],)).fetchall()[:]
        for i in c:
            self.basa_cursor.execute('''UPDATE people SET gr = (?) WHERE id = (?)''', (0, i[1]))
        for i in c:
            self.basa_cursor.execute('''DELETE FROM people_group WHERE id_group = (?)''', (b[0][0],))
            self.basa_d.commit()
        for i in c:
            self.basa_cursor.execute('''DELETE FROM news WHERE id_group = (?)''', (b[0][0],))
            self.basa_d.commit()
        b = self.basa_cursor.execute('''SELECT * FROM gruppa''').fetchall()
        c = []
        for i in b:
            c.append(i[1])
        self.comboBox.clear()
        self.comboBox.addItems(c)    

            
if __name__ == '__main__':
    basa_d = sqlite3.connect('ClanChat.db')
    basa_cursor = basa_d.cursor()
    app = QApplication(sys.argv)
    check_window = Check_window()
    check_window.setObjectName("ClanChat")
    check_window.setStyleSheet("#ClanChat{border-image:url(1.jpg)}")
    check_window.show()
    gateway_window = Gateway_window(basa_d)
    gateway_window.setObjectName("Вход")
    gateway_window.setStyleSheet("#Вход{border-image:url(1.jpg)}")
    regisration_window = Regisration_window(basa_d)
    regisration_window.setObjectName("Регистрация")
    regisration_window.setStyleSheet("#Регистрация{border-image:url(1.jpg)}")
    choose_window = Choose_window(basa_d)
    choose_window.setObjectName("Choose")
    choose_window.setStyleSheet("#Choose{border-image:url(1.jpg)}")
    create_window = Create_window(basa_d)
    create_window.setObjectName("Create")
    create_window.setStyleSheet("#Create{border-image:url(1.jpg)}")
    seek_window = Seek_window(basa_d)
    seek_window.setObjectName("НайтиГруппу")
    seek_window.setStyleSheet("#НайтиГруппу{border-image:url(1.jpg)}")
    group_window = Group_window(basa_d)
    group_window.setObjectName("Группа")
    group_window.setStyleSheet("#Группа{border-image:url(1.jpg)}")
    edit_group_window = Edit_group_window(basa_d)
    edit_group_window.setObjectName("Группа")
    edit_group_window.setStyleSheet("#Группа{border-image:url(1.jpg)}")
    admin = Admin_window(basa_d)
    admin.setObjectName("Редактор")
    admin.setStyleSheet("#Редактор{border-image:url(1.jpg)}")
    uu = U(basa_d)
    uu.setObjectName("Список")
    uu.setStyleSheet("#Список{border-image:url(1.jpg)}")
    basa_d.commit()
    sys.exit(app.exec_())
    basa_d.commit()
    basa_d.close()
    basa_cursor.close()











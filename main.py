from PyQt5.QtWidgets import (
   QApplication, QWidget, QPushButton,
   QLabel, QVBoxLayout, QHBoxLayout,
   QListWidget, QFileDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
from PIL.ImageFilter import SHARPEN

app = QApplication([])
window = QWidget()
window.setWindowTitle('Easy Editor by Dewi Idda')
window.resize(700,500)

folder_button = QPushButton('Select Folder')
image_list = QListWidget()
image = QLabel()
left = QPushButton('Left')
right = QPushButton('Right')
mirror = QPushButton('Mirror')
sharp = QPushButton('Sharp')
bw = QPushButton('Black and White')

row = QHBoxLayout()
col1 = QVBoxLayout()
col1.addWidget(folder_button)
col1.addWidget(image_list)
col2 = QVBoxLayout()
col2.addWidget(image)
filter_row = QHBoxLayout()
filter_row.addWidget(left)
filter_row.addWidget(right)
filter_row.addWidget(mirror)
filter_row.addWidget(sharp)
filter_row.addWidget(bw)
col2.addLayout(filter_row)

row.addLayout(col1)
row.addLayout(col2)
window.setLayout(row)
window.setStyleSheet("background-color: #5C766D")
image_list.setStyleSheet("background-color: #EDE9E6")
folder_button.setStyleSheet("background-color: #5C4F4A")
left.setStyleSheet("background-color: #C9996B")
right.setStyleSheet("background-color: #C9996B")
mirror.setStyleSheet("background-color: #C9996B")
sharp.setStyleSheet("background-color: #C9996B")
bw.setStyleSheet("background-color: #C9996B")

import os

workdir = ''
def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result

def choose_workdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()

def show_filename_list():
   extensions = ['.jpg','.jpeg','.png','.gif','.svg','.bmp']
   choose_workdir()
   filenames = filter(os.listdir(workdir), extensions)
   image_list.clear()
   for filename in filenames:
       image_list.addItem(filename)

class ImageProcessor():
   def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

   def load_image(self, dir, filename):
       self.dir = dir
       self.filename = filename
       image_path = os.path.join(dir, filename)
       self.image = Image.open(image_path)
       
   def show_image(self, path):
       image.hide()
       pixmapimage = QPixmap(path)
       w, h = image.width(), image.height()
       pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
       image.setPixmap(pixmapimage)
       image.show()

   def do_bw(self):
       self.image = self.image.convert("L")
       self.save_image()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.show_image(image_path)

   def do_left(self):
       self.image = self.image.transpose(Image.ROTATE_90)
       self.save_image()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.show_image(image_path)

   def do_right(self):
       self.image = self.image.transpose(Image.ROTATE_270)
       self.save_image()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.show_image(image_path)

   def do_flip(self):
       self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
       self.save_image()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.show_image(image_path)

   def do_sharpen(self):
       self.image = self.image.filter(SHARPEN)
       self.save_image()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.show_image(image_path)
    
   def save_image(self):
       path = os.path.join(workdir, self.save_dir)
       if not(os.path.exists(path) or os.path.isdir(path)):
           os.mkdir(path)
       fullname = os.path.join(path, self.filename)
       self.image.save(fullname)

workimage = ImageProcessor()
def show_chosen_image():
    if image_list.currentRow() >= 0:
        filename = image_list.currentItem().text()
        workimage.load_image(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.show_image(image_path)
   
image_list.currentRowChanged.connect(show_chosen_image)
left.clicked.connect(workimage.do_left)
right.clicked.connect(workimage.do_right)
mirror.clicked.connect(workimage.do_flip)
sharp.clicked.connect(workimage.do_sharpen)
bw.clicked.connect(workimage.do_bw)

folder_button.clicked.connect(show_filename_list)
window.show()
app.exec()

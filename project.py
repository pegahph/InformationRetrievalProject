from __future__ import unicode_literals
from hazm import *
import os

path = r"D:/InformationRetrievalProject/txtfiles"
os.chdir(path)
normalizer = Normalizer()

def read_files(file_path):
   with open(file_path, 'r', encoding="utf-8") as file:
      normalize = normalizer.normalize(file.read())
      tokenize = word_tokenize(normalize)
      print(tokenize)

for file in os.listdir():
    file_path =f"{path}/{file}"

read_files(file_path)



  
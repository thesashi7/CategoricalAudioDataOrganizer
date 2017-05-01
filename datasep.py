import csv
import os
import glob
from shutil import copy2

dog_common_name = {"Coyote", "Dog (Domestic type)", "Gray Wolf", "Arctic Fox", "Red Fox", "African hunting dog",
"Black-backed Jackal","Swift Fox","Golden Jackal","Crab-eating Fox","Pampas Fox","Maned Wolf","common gray fox",
"Side-striped Jackal","Bush Dog","Culpeo"}
cat_common_name = {"Cat (Domestic type)","Cougar","Jaguar","Lion","Ocelot","Jaguarundi","Leopard","Tiger",
"Bobcat"}
category_map={"id_num":"label"}


def getCategory(common_name):
  if(common_name in dog_common_name):
    return "dog"
  elif(common_name in cat_common_name):
    return "cat"
  return "None"

def initCategoryMap(csv_file):
  with open(csv_file,'r') as csvfile:
    reader = csv.reader(csvfile)
    #skipping first row which is just the name of the colums
    reader.next()
    for row in reader:
      #print(row[0]+" "+row[3])
      current_cat = getCategory(row[3])
      if(current_cat == "cat" or current_cat == "dog"):
        category_map.__setitem__(row[0],current_cat)

def getAllWavInDir(dirName):
  types = ('*.wav')
  wavFilesList = []
  print("Dir with all Wav Files : "+dirName)
  for files in types:
    wavFilesList.extend(glob.glob(os.path.join(dirName, files)))
  return wavFilesList

##
# @return two wavFilesList conisiting of full path.
#  One contains cat wav files (full path) and the other contains dog wav files (full path).
#
def getCatAndDogWavFilesPathList(wavFilesList):
  cat_wav_files = []
  dog_wav_files = []

  for wavFile in wavFilesList:
    file_name = os.path.splitext(os.path.basename(wavFile))[0]
    file_id = file_name.split("_")[0]
    val = category_map.get(file_id)
    if(val == "cat"):
      cat_wav_files.append(wavFile)
    elif(val == "dog"):
      dog_wav_files.append(wavFile)

  return (cat_wav_files, dog_wav_files)


def copyCategoryWavFilesToCategoryDir(wavFilesList,category):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  categ_dir_path = dir_path+"/"+category
  if not os.path.exists(categ_dir_path):
    os.makedirs(categ_dir_path)
  for wavFiles in wavFilesList:
    copy2(wavFiles, categ_dir_path)

dirName = "/home/sashi/Documents/Spring2017/CS599/project/data/"
initCategoryMap("data-labels.csv")
wavFilesList = getAllWavInDir(dirName)
print("Toal Num Wav Files : " + str(len(wavFilesList)))
cat_wav_files, dog_wav_files = getCatAndDogWavFilesPathList(wavFilesList)
print("Total Num Cat Wav Files : "+str(len(cat_wav_files)))
print("Total Num Dog Wav Files : "+str(len(dog_wav_files)))
copyCategoryWavFilesToCategoryDir(cat_wav_files,"cat")
copyCategoryWavFilesToCategoryDir(dog_wav_files,"dog")





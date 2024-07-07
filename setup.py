#we do setup.py file to make our own library like pandas numpy
#we can use this library in other python file

from setuptools import find_packages,setup
#using typing we can read from requirements.txt in list

from typing import List

REQUIREMENT_FILE_NAME="requirements.txt"
HYPHEN_E_DOT = "-e ."

#usinf getrequiremnts to get all dependencies and install it except -e .

def get_requirements()->List[str]:
    
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
    
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list


#itis used to defing our own library named sensor,version 0.0.1 we can name it anyhing author is my name
#find packages is used to find packages in any foldser which contain __int__.py file
#we have to add -e. in requirements.txt to actiavte this in editorial format
setup(
    name="sensor",
    version="0.0.1",
    author="Harshit",
    author_email="Harshit00709@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements(),
)

#sensor.egg info will be craeted which will conatin sensor package and other dependency package list of folder which have __init__.py in it
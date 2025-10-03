from setuptools import find_packages, setup 
from typing import List 

HYPHEN_E_DOT = '-e .'
def getrequirements(file_path:str) -> List[str]:
  '''
  this function will return the list of requirement
  '''
  requirements_lst : List[str] = []
  try:
    with open(file_path) as file_obj:
      lines = file_obj.readlines() 
      for line in lines:
        requirement = line.strip()
        if requirement and requirement != HYPHEN_E_DOT:
          requirements_lst.append(requirement)
    return requirements_lst
  except FileNotFoundError as e: 
    print("File could not be located")


setup(
  name = "networksecurity",
  author = "Varun Goyal", 
  author_email = "varungoyal2006@outlook.com", 
  version = '0.0.0.1', 
  packages = find_packages(), 
  install_requires = getrequirements('requirements.txt')
)
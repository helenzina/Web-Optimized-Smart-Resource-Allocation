from setuptools import setup 
  
setup( 
    name="allocation", 
    version="1.1", 
    description="student allocation", 
    author="Helen Zina", 
    author_email="helenz1@windowslive.com", 
    packages=['allocation'], 
    install_requires=[ 
        "pandas", 
        "ortools",
        "openpyxl"
    ], 
) 
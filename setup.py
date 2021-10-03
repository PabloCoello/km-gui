from distutils.core import setup 
import py2exe 
 
setup(name="Kmeans", 
 version="1.0", 
 description="", 
 author="Pablo Coello Pulido", 
 author_email="pablo.coello@outlook.es", 
 url="https://github.com/PabloCoello/km-gui", 
 license="", 
 scripts=["main.py"], 
 console=["main.py"], 
 options={"py2exe": {"bundle_files": 1}}, 
 zipfile=None,
)
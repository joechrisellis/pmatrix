from setuptools import *

kwargs = {
	"author" : "Joe Ellis",
	"author_email" : "jce.devel@gmail.com",
	"description" : "A Python-implementation of the matrix falling text (like cmatrix).",
	"entry_points" : {"console_scripts" : ["pmatrix=pmatrix.pmatrix:start"]}
	"license" : "GPL v2",
	"name" : "pmatrix",
	"packages" : ["pmatrix"],
	"version" : "V0.0.1",
}

setup(**kwargs)

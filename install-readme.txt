How to Install our project:
add the file setup.py to the same folder as the others,
before installetion you must perform the preperations:
1. Verify you have the right packages:
	run pip install pandas \
		   matplotlib \
		   numpy \
		   pathlib \
		   xlswriter \
		   tkinter \
		   xlrd==1.2
2. run pip install cx_Freeze and idna.
3. change the version number in install.py .
4. run "python install.py build"
5. hope there will be no errors. Good luck !

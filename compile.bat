pyinstaller -i resources/icon.ico --onefile --noconsole game.py 
rmdir /Q /S build
rmdir /Q /S __pycache__
del tic_tac_toe_gui.spec


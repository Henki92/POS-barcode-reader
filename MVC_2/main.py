# Use Tkinter for python 2, tkinter for python 3
from controller import Controller

if __name__ == '__main__':
    print("RUNNING BARCODE READER AS MVC")
    c = Controller()
    c.run()
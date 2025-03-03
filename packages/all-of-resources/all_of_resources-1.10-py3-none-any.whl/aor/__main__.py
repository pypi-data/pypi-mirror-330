from .version import version
__version__ = version
import sys
def main():
    if len(sys.argv)>=2 and (sys.argv[1]=="--flutter" or sys.argv[1]=="-f"):
        from . import fletgui
        fletgui.main()
    else:
        from. import tkgui
        tkgui.main()
if __name__=="__main__":
    main()
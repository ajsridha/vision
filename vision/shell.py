from vision.commands import commands
from vision.console import HistoryConsole

if __name__ == '__main__':
    BANNER='''
    Welcome to Vision. You can interact with the library using the
    following command:

    scan("http://www.example.com/image.jpg")
    '''

    console = HistoryConsole(locals=commands)
    console.interact(banner=BANNER)

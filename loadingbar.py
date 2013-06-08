#! /usr/bin/env python
# Filename: ConsoleUtils.py

import sys

__version__ = "v1.0a"
__author__ = "Ki113d"
__maintainer__ = "Ki113d"
__email__ = "ki113d.69@gmail.com"
__status__ = "Development"

class ProgressBar():
    """
        A console based progress bar.
        Used to give a visual representation on the progress of an
        opperation.
    """
    
    def __init__(self, message="", fillChar='-'):
        """
            Constructor.
            Params:
                message: A string describing the current opperation or nothing.
                fillChar: The character used to display progress on the bar.
        """
        self.char = fillChar
        self.message = message
        self.bar = ''
        self.length = 20
        self.createBar()
                
    def updateBar(self, percentage):
        """
            This method should be called by the user to update the progress bar.
            When the threaded version is released it will be more efficient.
        """
        if not isinstance(percentage, int):
            raise ValueError("Percentage must be of type int!")
            
        if percentage > -1 and percentage < 101:
            self.calculateBar(percentage)
            self.write("{0}[{1}]{2:4}%".format(self.message + " ", self.bar, percentage))
        else:
            if percentage < 0:
                raise ValueError("Percentage must never be lower then 0!")
            elif percentage > 100:
                raise ValueError("Percentage must never be greater then 100!")
    
    def write(self, line):
        """
            Writes the given line to stdout.
            May support other outputs later.
        """
        sys.stdout.write("{0}\r".format(line))
        sys.stdout.flush()
        
    def calculateBar(self, percent):
        """
            Changes the state of the progress bar according to the given
            percentage.
            Will be worked on later to support different sized progress bars.
        """
        i = 0
        parts = list(self.bar)
        while i < (percent/5):
            parts[i] = self.char
            i += 1
        self.bar = "".join(parts)
    
    def createBar(self):
        """
            Constructs the progress bar.
            Will be used in the future to enable different sized progress bars.
        """
        i = 0
        while i < self.length:
            self.bar += " "
            i += 1
            
    def close(self):
        """
            Prints a new line to close off use of stdout.
            This method must be called or any output from your
            application may cause trouble.
        """
        print

class LoadingLabel():
    """
        A LoadingLabel (for lack of a better name).
        Used to give a nice visual representation that your program is
        doing something.
    """
    
    def __init__(self, message=("Loading", "Loading.", "Loading..", "Loading..."), closingString="Done!"):
        """
            Constructor.
            Params:
                message: A tuple containing strings to be displayed.
        """
        if not isinstance(message, tuple):
            raise ValueError("Message must be of type tuple!")
        self.message = message
        self.closingString = closingString
        self.currentIndex = 0
        self.lastIndex = 0
    
    def write(self, line):
        """
            Writes the given line to stdout.
            May support other outputs later.
        """
        sys.stdout.write("{0}\r".format(line))
        sys.stdout.flush()
        
    def update(self):
        """
            Updates the LoadingLabel and moves to the next indexed string in the tuple.
        """
        self.write("{0:{1}}".format(self.message[self.currentIndex], len(self.message[self.lastIndex])))
        self.lastIndex = self.currentIndex
        if self.currentIndex == len(self.message)-1:
            self.currentIndex = 0
        else:
            self.currentIndex += 1
        
    def close(self):
        """
            Prints closing string and a new line to close off use of stdout.
            This method must be called or any output from your
            application may cause trouble.
        """
        self.write("{0:{1}}".format(self.closingString, len(self.message[self.currentIndex])))
        print
            
if __name__ == '__main__':
    import time
    print "ProgressBar and LoadingLabel example."
    print
    print
    
    i = 0
    
    # Create a progress bar with custom message and fill character.
    progress = ProgressBar("Downloading something", '=')
    while i <= 100:
        # In a while loop update the bar every 300 milliseconds.
        # What ever you pass to the updateBar method is divided by 5 so
        # it may never be larger then 100, at least untill I fix it :P
        progress.updateBar(i)
        i += 1
        time.sleep(0.3)
    progress.close()
    
    i = 0
    # Pretty much the same structure for the LoadingLabel.
    loadBar = LoadingLabel(("Loading", "Loading.", "Loading..", "Loading...", "Loading...."), "Complete!")
    while i <= 20:
        # Only difference here is that we don't have to pass an integer to the update method.
        loadBar.update()
        i += 1
        time.sleep(0.4)
    loadBar.close()
7

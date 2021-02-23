import traceback
import sys


def printException(Exception ,msg):
    print("Exception at " + msg)
    print(traceback.format_exc())
    # or
    print(sys.exc_info()[2])
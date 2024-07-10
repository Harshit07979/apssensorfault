#we want exception message in particular format so thats why this model
import sys
import os

def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info() #It extracts information about the error (file name, line number, and error message) using exc_info().
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message



class SensorException(Exception):

    def __init__(self,error_message, error_detail:sys):
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail)
        
    def __str__(self):
        return self.error_message 
    

#file_name = exc_tb.tb_frame.f_code.co_filename:
#exc_tb refers to the traceback object (part of the exception information).
#tb_frame represents the current frame (i.e., the function or method where the exception occurred).
#f_code contains information about the code (e.g., filename, line number) associated with the frame.
#co_filename is the filename where the code is located.
#So, this line assigns the filename (path) of the Python script where the error occurred to the variable file_name.
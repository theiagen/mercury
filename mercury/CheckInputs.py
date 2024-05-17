import os
import argparse

def is_table_valid(filename):
  """
  Checks if the input TSV file is valid
  """
  if not os.path.exists(filename) and filename != "-":
    raise argparse.ArgumentTypeError("{0} cannot be accessed".format(filename))
  return filename

def is_comma_delimited_list(string):
  """
  Checks if the input string is a list
  """
  if string is not None:
    return string.split(",")
  else:
    raise argparse.ArgumentTypeError("{0} is not a valid list".format(string))

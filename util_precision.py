####################################################################
# This small utility read labels true value the test set input file
# and the predicted score from logistic regression output and
# calculate accuracy, recall and precision
####################################################################

import sys
import string
import numpy as np
from sklearn.metrics import precision_score,recall_score,accuracy_score

def main():
  if len(sys.argv) != 3:
    print 'usage: ./util.py file'
    sys.exit(1)
    
  filename = sys.argv[1]
  filename1 = sys.argv[2]
  
  input_file = open(filename, 'r')
  input_file1 = open(filename1, 'r')
  
  y_true = []
  i = 0
  for line in input_file:
    click = int(line.split(',')[1])
    y_true.append(click)
    i = i + 1
  print "read",i,"lines"
  y_trueA = np.array(y_true) 

  y_pred = []
  i = 0
  for line in input_file1:
    click = int(float(line.split(',')[1])/0.5)
    y_pred.append(click)
    i = i + 1
  print "read",i,"lines"
  y_predA = np.array(y_pred)
  
  print "precision score is:"
  print precision_score(y_trueA, y_predA)
  print "recall score is:"
  print recall_score(y_trueA, y_predA)
  print "accuracy score is:"
  print accuracy_score(y_trueA, y_predA)
  
if __name__ == '__main__':
  main()

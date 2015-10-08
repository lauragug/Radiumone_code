#
#  This small utility read spark notebook output, add headers 
#  line number and label, 1 for converters, 0 for users
#

import sys
import string

def main():
  if len(sys.argv) != 2:
    print 'usage: ./util.py file'
    sys.exit(1)
    
  filename = sys.argv[1]
  filename_out = filename + ".csv"
  
  input_file = open(filename, 'r')
  output_file = open(filename_out,'w')
  
  stringa = ','.join(['id','click','userid','siteid','timestamp','visit','clusters','p0','p1','p2','p3','p4'])
  output_file.write(stringa+'\n')  
  i = 0
  for line in input_file:
    stringa1 = ','.join([str(i),'0',line])
    output_file.write(stringa1)
    i = i + 1
  print "copied to file",i,"lines"
	
if __name__ == '__main__':
  main()

# replaces null bytes in a csv file so that it can be read/processed by python (run once)
import sys
if len(sys.argv) < 3:
  print len(sys.argv)
  print """USAGE: python removeNull.py [input_file] [output_file]"""
  sys.exit()
fi = open(sys.argv[1], 'rb')
data = fi.read()
fi.close()
fo = open(sys.argv[2], 'wb')
fo.write(data.replace('\x00', '').replace('\n', '').replace('\\\\\\\r', '\\\\\\'))
fo.close()
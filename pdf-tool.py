#!/usr/bin/python
import sys
import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter

CPURP = '\033[95m'
CGREEN = '\033[92m'
CRED = '\033[91m'
CEND = '\033[0m'

parser = argparse.ArgumentParser(usage='%(prog)s [-h] [-e file -p password] [-d file -w wordlist]')
parser.add_argument('-e','--encrypt',metavar='file', help='Encrypt PDF',default=None)
parser.add_argument('-p','--password',metavar='password', help='Password to encrypt PDF',default=None)
parser.add_argument('-d','--decrypt',metavar='file',help='Brute force PDF',default=None)
parser.add_argument('-w','--wordlist',metavar='wordlist',help='Wordlist to brute force',default=None)
ns = parser.parse_args()

#Validations

if (len(sys.argv) != 5):
        print "Print -h for usage"
        sys.exit()

if len([x for x in (ns.encrypt,ns.password) if x is not None]) == 1:
	parser.error('encryption and password options must be given together')
	sys.exit()

if len([x for x in (ns.decrypt,ns.wordlist) if x is not None]) == 1:
	parser.error('decryption and wordlist options must be given together')
	sys.exit()

# Encrypt

if(str(ns.encrypt) != "None" and str(ns.password) != "None"):
	try:
		filename = ns.encrypt
		password = ns.password
		ofilename = "encrypted_{}".format(filename)

		input_pdf = PdfFileReader(open(ns.encrypt,"rb"))
		out = PdfFileWriter()
		out.appendPagesFromReader(input_pdf)
		out.encrypt(password)
		out.write(open(ofilename,"wb"))
		print "{}[*]{} Saved to '{}'".format(CGREEN,CEND,ofilename)
	except:
		print "{}[*]{} Error".format(CRED,CEND)

# Brute force

if(str(ns.decrypt) != "None" and str(ns.wordlist) != "None"):
	pdf = PdfFileReader(open(ns.decrypt,"rb"))

	if pdf.isEncrypted:
		print "{}[*]{} File '{}' is encrypted. Brute forcing...".format(CPURP,CEND,ns.decrypt)

		for i in open(ns.wordlist,"r"):
			password = i.rstrip()

			try:
				if(pdf.decrypt(password) == 1):
					print "{}[*]{} Password is: {}".format(CGREEN,CEND,password)
					break
			except:
				print "{}[*]{} Error".format(CRED,CEND)
	else:
		print "{}[*]{} File '{}' is not password protected!".format(CRED,CEND,ns.decrypt)

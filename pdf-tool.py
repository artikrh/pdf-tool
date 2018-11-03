#!/usr/bin/python
import sys
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
from os import _exit
import argparse
import getpass
from PyPDF2 import PdfFileReader, PdfFileWriter

CPURP = '\033[95m'
CGREEN = '\033[92m'
CRED = '\033[91m'
CEND = '\033[0m'

parser = argparse.ArgumentParser(usage='%(prog)s [-h] [-e file -p password] [-d file -w wordlist]')
parser.add_argument('-e','--encrypt',metavar='file', help='Encrypt PDF',default=None)
parser.add_argument('-p','--password',metavar='password',nargs='?', help='Password to encrypt PDF',default=None)
parser.add_argument('-d','--decrypt',metavar='file',help='Brute force PDF',default=None)
parser.add_argument('-w','--wordlist',metavar='wordlist',help='Wordlist to brute force',default=None)
ns = parser.parse_args()

def encrypt():
	try:
		filename = ns.encrypt
		if(str(ns.password) != "None"):
			password = ns.password
		else:
			password = getpass.getpass()

		ofilename = "{}-encrypted".format(filename)
		input_pdf = PdfFileReader(open(ns.encrypt,"rb"))
		out = PdfFileWriter()
		out.appendPagesFromReader(input_pdf)
		out.encrypt(password)
		out.write(open(ofilename,"wb"))
		print "{}[*]{} Saved to '{}'".format(CGREEN,CEND,ofilename)
	except:
		print "{}[*]{} Error".format(CRED,CEND)

def brute(passwords):
	pdf = PdfFileReader(open(ns.decrypt,"rb"))
	try:
		if(pdf.decrypt(passwords) == 1):
			print "{}[*]{} Password is: {}".format(CGREEN,CEND,passwords)
			_exit(0)
	except:
		print "\n{}[*]{} Exiting...".format(CRED,CEND)

def threading():
        passwords = []

	for pwds in open(ns.wordlist,"r"):
		passwords.append(pwds.rstrip())

	pool = ThreadPool(multiprocessing.cpu_count())
	pool.map(brute, passwords)
	pool.close()
	pool.join()

if __name__ == "__main__":

	# Validations
	if (len(sys.argv) != 5 and len(sys.argv) != 4):
        	print "Print -h for usage"
        	sys.exit()

	if(str(ns.password) != "None"):
	        if len([x for x in (ns.encrypt,ns.password) if x is not None]) == 1:
        	        parser.error('encryption and password options must be given together')
                	sys.exit()

	if len([x for x in (ns.decrypt,ns.wordlist) if x is not None]) == 1:
        	parser.error('decryption and wordlist options must be given together')
        	sys.exit()

	# Process
	if(str(ns.encrypt) != "None"):
		encrypt()

        if(str(ns.decrypt) != "None" and str(ns.wordlist) != "None"):
		pdf = PdfFileReader(open(ns.decrypt,"rb"))

		if pdf.isEncrypted:
                	print "{}[*]{} File '{}' is encrypted. Brute forcing...".format(CPURP,CEND,ns.decrypt)
			threading()
		else:
                	print "{}[*]{} File '{}' is not password protected!".format(CRED,CEND,ns.decrypt)

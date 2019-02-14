# pdf-tool [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
A tool which offers PDF file encryption in command line and brute forcing them using a local wordlist.

    usage: pdf-tool.py [-h] [-e file -p password] [-d file -w wordlist]

    optional arguments:
      -h, --help            show this help message and exit
      -e file, --encrypt file
                        Encrypt PDF
      -p password, --password password
                        Password to encrypt PDF
      -d file, --decrypt file
                        Brute force PDF
      -w wordlist, --wordlist wordlist
                        Wordlist to brute force  
                        
 ## Requirement
 [PyPDF2](https://pythonhosted.org/PyPDF2/) library (case sensitive) is required for standard PDF operations.
 
     $ sudo pip2 install PyPDF2
 ## To Do
 - Support more options

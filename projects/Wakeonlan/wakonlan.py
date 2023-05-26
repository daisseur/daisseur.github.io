from wakeonlan import send_magic_packet
from sys import argv
import re

if len(argv) > 1:
    addr = argv[1]
else:
    addr = input("mac addr : ")

ex = '6a-94-ec-53-5b-27'
pattern = r'\w\w-\w\w-\w\w-\w\w-\w\w-\w\w'

if re.match(pattern, addr) or re.match(pattern.replace("-", ":"), addr):
    send_magic_packet(addr)
    print("paquet envoyé !")
else:
    print("mauvais format d'addresse")


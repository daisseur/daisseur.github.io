from time import sleep
def calc(notes):
	notes = [float(i) for i in notes.split()]
	total = 0
	for i in notes:
		total += i
	print(total/len(notes))
calc(input("Entrez vos notes séparé par un espace : "))
sleep(10)
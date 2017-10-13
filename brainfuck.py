# encoding=utf8
import sys
SIZE 	= 30000
MAX		= 128
kod 	= []
kodit 	= 0
out 	= []
tab 	= [0 for i in range(SIZE)]
it		= 0
SIZE 	= 30000
MAX		= 128
kod 	= []
kodit 	= 0
out 	= []
tab 	= [0 for i in range(SIZE)]
it 		= 0
def dodaj():		# -
	global it, tab, MAX
	tab[it]+=1
	tab[it]%=MAX
	return True
def odejmij():		# +
	global tab, it, MAX
	tab[it]+= (MAX-1)
	tab[it]%=MAX
	return True
def prawo():		# >
	global it, SIZE
	it+=1
	it%=SIZE
	return True
def lewo():			# <
	global it, SIZE
	it+=(SIZE-1)
	it%=SIZE
	return True
def pisz():			# .
	global out, tab, it
	out.append(chr(tab[it]))
	return True
def czyt():			# ,
	global tab, it
	wejscie=input("Proszę podać jeden znak:")
	tab[it] = ord(wejscie[0])
	return True
def petlapocz():	# ]
	global kod, kodit
	ile=1		
	kodit-=1
	while ile!=0:
		if kodit<0:
			return False
		if kod[kodit]==']':
			ile+=1
		if kod[kodit]=='[':
			ile-=1
		kodit-=1
	return True
def petlakon():	# [
	global kod, kodit, tab, it
	if tab[it]==0:
		ile=-1
		kodit+=1
		while ile!=0:
			if kodit>=len(kod):
				return False
			if kod[kodit]==']':
				ile+=1
			if kod[kodit]=='[':
				ile-=1
			kodit+=1
		kodit-=1
	return True
def main():
	kod = input("Proszę podać kod programu (bez spacji na końcu i początku):\n")
	pom = True
	while kodit < len(kod):
		if kod[kodit]=='>':
			pom = prawo()
		elif kod[kodit]=='<':
			pom = lewo()
		elif kod[kodit]=='+':
			pom = dodaj()
		elif kod[kodit]=='-':
			pom = odejmij()
		elif kod[kodit]=='.':
			pom = pisz()
		elif kod[kodit]==',':
			pom = czyt()
		elif kod[kodit]=='[':
			pom = petlakon()
		elif kod[kodit]==']':
			pom = petlapocz()
		else:
			pom = False
			print("Błędny kod programu!!!\nNieobsługiwany znak!!!")
			break
		if not pom:
			print("Błędny kod programu!!!\nZłe ustawienie pętli!!!")
			break
		kodit+=1
	if pom:
		print("Wyjście programu:")
		print(''.join(out))
# wywołanie main
if __name__ == '__main__':
	main()

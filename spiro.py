# coding=utf-8
import sys, random, argparse
import numpy as np
import math
import turtle
import random
from PIL import Image
from datetime import datetime
from fractions import gcd

# klasa rysująca spirograf
class Spiro:
	# konstruktor
	def __init__(self, xc, yc, col, R, r, l):
		# tworzenie obiektu turtle
		self.t = turtle.Turtle()
		# ustawianie kształtu kursora
		self.t.shape("turtle")
		self.t.hideturtle()
		# ustawianie kroku w stponiach
		self.step = 5
		
		# ustawianie flagi zakończenia rysowania
		self.drawingComplete = False
		
		# ustawianie parametrów
		self.setparams(xc, yc, col, R, r, l)
		
		# inicjowanie rywowania
		self.restart()
	# ustawianie parametrów
	def setparams(self, xc, yc, col, R, r, l):
		# parametry spirografu
		self.xc = xc
		self.yc = yc
		self.r = int(r)
		self.R = int(R)
		self.l = l
		self.col = col
		# zredukownie r/R do naimniejszej postaci podzielnej przez NWD
		gcdVal = gcd(self.r, self.R)
		self.nRot = self.r//gcdVal
		# ustawianie stosunków promieni
		self.k = self.r/float(self.R)
		# ustawianie koloru
		self.t.color(*col)
		# zapisanie bierzącego kąta
		self.a = 0
	# restartowanie rysowania
	def restart(self):
		# ustawianie flagi
		self.drawingComplete = False
		# pokazywanie żółwia
		# self.t.showturtle()
		# przejście do pierwszego punktu
		self.t.up()
		R, k, l = self.R, self.k, self.l
		a = 0.0
		x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
		y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
		self.t.setpos(self.xc + x, self.yc + y)
		self.t.down()
	# rysowanie całości
	def draw(self):
		# rysowanie reszty punktów
		R, k, l = self.R, self.k, self.l
		for i in range(0,360*self.nRot+1,self.step):
			a = math.radians(i)
			x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
			y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
			self.t.setpos(self.xc + x, self.yc + y)
		#rysownie ukończone, więc ukrywamy żółwia
		self.t.hideturtle()
	# aktualizowanie o jeden krok
	def update(self):
		# pominięcie reszty kroków, jeśli zrobione
		if self.drawingComplete:
			return
		# inkrementowanie kąta
		self.a += self.step
		# rywowanie kroku
		R, k, l = self.R, self.k, self.l
		# ustawianie kąta
		a = math.radians(self.a)
		x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
		y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
		self.t.setpos(self.xc + x, self.yc + y)
		# jeśli rysowanie zakończone, ustawianie flagi
		if self.a >= 360*self.nRot:
			self.drawingComplete = True
			# rysowanie ukończone, więc ukrywamy żółwia
			self.t.hideturtle()
# klasa do animowania spirografów
class SpiroAnimator:
	# konstruktor
	def __init__(self,N):
		# ustawianie wartości licznika w milisekundach
		self.deltaT = 0
		# uzyskiwanie rozmiarów okna
		self.width = turtle.window_width()
		self.height = turtle.window_height()
		# tworzenie obiektów spiro
		self.spiros = []
		for i in range(N):
			# generowanie losowych parametrów
			rparams = self.genRandomParams()
			# ustawianie parametrów spiro
			spiro = Spiro(*rparams)
			self.spiros.append(spiro)
		# wywołanie timera
		turtle.ontimer(self.update, self.deltaT)
	# generowanie losowych parametrów
	def genRandomParams(self):
		width, height = self.width, self.height
		R = random.randint(250, min(width, height)//2)
		r = random.randint(10, 9*R//10)
		l = random.uniform(0.1, 0.9)
		# xc = random.randint(-width//2, width//4)
		# yc = random.randint(-height//2, height//4)
		xc = 0
		yc = 0
		col = (random.random(),
		random.random(),
		random.random())
		return (xc, yc, col, R, r, l)
	# restartowanie programu
	def restart(self):
		for spiro in self.spiros:
			# czyszczenie
			spiro.t.clear()
			# generowanie losowych parametrów
			rparams = self.genRandomParams()
			# ustawianie parametrów spiro
			spiro.setparams(*rparams)
			# zrestartowanie rysowania
			spiro.restart()
	def update(self):
		# aktuwalizowanie wszystkich krzywych spiro
		nComplete = 0
		for spiro in self.spiros:
			# aktualizowanie
			spiro.update()
			# zliczanie ukończonych krzywych
			if spiro.drawingComplete:
				nComplete += 1
		# jeśli wszytkie krzywa spiro są ukończone, restartowanie
		if nComplete == len(self.spiros):
			self.restart()
		# wywyłanie timera
		turtle.ontimer(self.update, self.deltaT)
	# włączanie i wyłączanie kursora żółwia
	def toggleTurtles(self):
		for spiro in self.spiros:
			if spiro.t.isvisible():
				spiro.t.hideturtle()
			else:
				spiro.t.showturtle()
# zapisywanie rysunków jako plików PNG
def saveDrawing():
	# ukrycie kursora żółwia
	turtle.hideturtle()
	# generowanie unikatowej nazwy pliku
	dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
	fileName = 'spiro-' + dateStr
	print('zapisanie rysunku w pliku %s.eps/png' % fileName)
	# uzyskiwanie canvas modułu tkinter
	canvas = turtle.getcanvas()
	# zapisywanie rysunku jako obrazu postscript
	canvas.postscript(file = fileName + '.eps')
	# użycie modułu Pillow do konwersji pliku obrazu postscript na PNG
	img = Image.open(fileName + '.eps')
	img.save(fileName + '.png', 'png')
	# pokazywanie kursora żółwia
# funkcja main()
def main():
	# użycie sys.argv w razie potrzeby
	print('generowanie spirografu...')
	# tworzenie parsera
	descStr = """Ten progeam rysuje krzywe spiro, używając modułu turtle.
	Program uruchomiony bez żadnych argumentów rysuje losowe krzywe spiro.
	
	Terminologia:
	R: promień zewnętrznego okręgu.
	r: promień wewnętrznego okręgu.
	l: stoeunek odcinka poprowadzonego ze środka mniejszego okręgu do punktu umieszczenia końcówki pióra do promienia r.
	"""
	parser = argparse.ArgumentParser(description=descStr)
	
	# dodanie oczekiwanych argumentów
	parser.add_argument('--sparams', nargs=3, dest='sprams', required=False, help="Trzy argumenty w sparams: R, r, l.")
	
	#parsowanie args
	args = parser.parse_args()
	
	# ustawianie szerokości okna rysowania na 80% szerokości ekranu
	turtle.setup(width=500)
	turtle.setup(height=900)
	# ustawianie kształtu żółwia jako kształtu kursora
	turtle.shape('turtle')
	
	# ustawianie tytułu
	turtle.title("Spirografy!")
	# dodanie procedury obsługi przycisku dla zapisywania rysunków
	turtle.onkey(saveDrawing, "s")
	# rozpoczęcie nasłuchiwania
	turtle.listen()
	
	# ukrycie kursora turtle dunkcji main
	turtle.hideturtle()
	
	# sprawdzanue wszystkich argumentów wysłanych do --sparams i rysownie spirografu
	if args.sprams:
		params = [float(x) for x in args.sprams]
		# rysowanie spirografu z danymi parametrami
		col = (0.0, 0.0, 0.0)
		spiro = Spiro(0, 0, col, *params)
		spiro.t.hideturtle()
		spiro.draw()
	else:
		#tworzenie obiektu animatora
		spiroAnim = SpiroAnimator(1)
		# dodanie procedury obsługi przycisku dla włączania i wyłączania kursora żółwia
		turtle.onkey(spiroAnim.toggleTurtles, "t")
		# dodanie procedury obsługi dla restartowania animacji
		turtle.onkey(spiroAnim.restart, "space")
	# rozpoczęcie głównej pętli turtle
	turtle.mainloop()
# wywyłanie main
if __name__ == '__main__':
	main()
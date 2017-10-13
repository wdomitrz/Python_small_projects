import sys, random, argparse
import numpy as np
import math

from PIL import Image

# 70 poziomów szarości
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale1 = gscale1[::-1]
# gscale1 = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
# 10 poziomów szarości
gscale2 = " .:-=+*#%@"
# gscale2 = "@%#*+=-:. "

def getAverageL(image):
	# uzyskanie obrazu jako tabliczy numpy
	im = np.array(image)
	# uzyskanie wymiarów
	w,h=im.shape
	# uzyskanie średniej
	return np.average(im.reshape(w*h))
	
def convertImageToAscii(fileName, cols, scale, moreLevels):
	"""
	Dla danego obiektu Image i wymiarów (rows, cols) zwraca listę m*n obiektów Image
	"""
	# deklarowanie zmiennych globalnyuch
	global gscale1, gscale2
	# otwarcie obrazu i konwetsja na skalę szarości
	image = Image.open(fileName).convert('L')
	# zapisywanie wymiarów
	W, H = image.size[0], image.size[1]
	print("wprowadź wymiry obrazu: %d x %d" % (W, H))
	# obliczanie szerokości kafelka
	w = W/cols
	# oblicznajie wysokości kafekla na podstawie współczynnika proporcji i skali czcionki
	h = w/scale
	# oblicznanie liczby wierszy
	rows = int(H/h)
	ma, mi = 0, 256
	for j in range(rows-1):
		y1 = int(j*h)
		for i in range(cols-1):
			x1 = int(i*w)
			img = image.crop((x1, y1, x1+1, y1+1))
			avg = int(getAverageL(img))
			mi = min(mi, int(avg) )
			ma = max(ma, int(avg) )
			
	print("kolumn: %d, wierszy %d" % (cols, rows))
	print("wymiary kafekla: %d x %d" %(w, h))
	if cols > W or rows > H:
		print("Obraz jest za mały dla podanej liczby kolumn!")
		exit(0)
	# obraz ASCII jest listą łańcuchów znaków
	aimg = []
	# generowanie listy wymiarów kafelków
	for j in range(rows):
		y1 = int(j*h)
		y2 = int((j+1)*h)
		# korygowanie ostatniego kafelka
		if j == rows-1:
			y2 = H
		# załączanie pustego łańcucha
		aimg.append("")
		for i in range(cols):
			x1 = int(i*w)
			x2 = int((i+1)*w)
			# korygowanie ostatniego kafekla
			if i == cols-1:
				x2 = W
			# przycinanie obrazu w celu wyodrębnienia kafelka do kolejnego obiektu Image
			img = image.crop((x1, y1, x2, y2))
			# uzyskanie średniej luinacji
			avg = int(getAverageL(img))
			# wyszukiwanie znaku ASCII dla wartości skali szarości (avg)
			if moreLevels:
				gsval = gscale1[int(((ma-avg)*69)/(ma-mi+1))]
			else:
				gsval = gscale2[int(((ma-avg)*9)/(ma-mi+1))]
			# dodawnie znaku ascii do łańcucha
			aimg[j] += gsval
	
	# zwracanie obrazu w formacie txt
	return aimg

# funkcja main
def main():
	# tworzenie parsera
	descStr = "Ten program konwertuje obraz na sztukę ASCII."
	parser = argparse.ArgumentParser(description=descStr)
	# dodawnie oczekiwanych argumentów
	parser.add_argument('--file', dest='imgFile', required=True)
	parser.add_argument('--scale', dest='scale', required=False)
	parser.add_argument('--out', dest='outFile', required=False)
	parser.add_argument('--cols', dest='cols', required=False)
	parser.add_argument('--morelevels', dest='moreLevels', action='store_true')
	
	# parsowanie args
	args = parser.parse_args()
	
	imgFile = args.imgFile
	#konfigurowanie pliku wyjściowego
	outFile = 'out.txt'
	if args.outFile:
		outFile = args.outFile
	# ustawianie domyślnej wartości skali jako 0.43, co jest odpowiednie dla czcionki Courier
	scale =  0.43
	if args.scale:
		scale = float(args.scale)
	# ustawianie liczby kolumn
	cols = 80
	if args.cols:
		cols = int(args.cols)
	print('generowanie sztuki ASCII...')
	
	aimg = convertImageToAscii(imgFile, cols, scale, args.moreLevels)
	
	# otwieranie nowego pliku tekstowego
	f = open(outFile, 'w')
	# zapisywanie w nowym pliku każdego łańcucha znaków z listy
	for row in aimg:
		f.write(row + '\n')
	# czyszczenie
	f.close()
	print("sztuka ASCII zostałą zapisana w pliku %s" % outFile)

# wywołanie main
if __name__ == '__main__':
	main()
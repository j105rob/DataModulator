#Main Source: http://www.iamit.org/blog/2012/01/advanced-data-exfiltration/
#Code Help: http://milkandtang.com/blog/2013/02/16/making-noise-in-python/
import math
import sys
import numpy
import os
import pyaudio

CHANNELS = 1
FORMAT = pyaudio.paFloat32
RATE = 44100


def convertToBinary(preFileName): #exports to file
	try:
		postFileName = 'modBinary.txt'
		preFileOpen = open(preFileName, 'rb')
		postFileOpen = open(postFileName, 'w')
		for data in [line.strip() for line in preFileOpen]:
			hexData = data.encode('hex')
			binData = bin(int('1'+hexData, 16))[3:]
			linebreak = '0000110100001010'
			postFileOpen.write(binData+linebreak) #this number is to add in the line break
	except:
		print "Error in convertToBinary function"
	finally:
		return postFileName
		preFileOpen.close()
		postFileOpen.close()



#creates the nibble from the earlier created file and sends it into playSound
def createNibble(binFileName):
	try: 
		openBinaryTxt = open(binFileName, 'r')
		readBinaryTxt = ' '
		nibbleArray = []
		while readBinaryTxt != '':
			readBinaryTxt = openBinaryTxt.read(1)
			if len(nibbleArray) == 4:
				nibble = ''.join(nibbleArray)
				playSound(nibble)
				del nibbleArray[:]
				nibbleArray.append(readBinaryTxt)
			else:
				nibbleArray.append(readBinaryTxt)
	except:
		pass		
		


def playSound(nibble):
	print 'Current Nibble: ',nibble
	frequency = 0;
	#key	
	aLo = '0000'
	bLo = '0001'
	cLo = '0010'
	dLo = '0011'
	eLo = '0100'
	fLo = '0101'
	gLo = '0110'
	hLo = '0111'
	aHi = '1000'
	bHi = '1001'
	cHi = '1010'
	dHi = '1011'
	eHi = '1100'
	fHi = '1101'
	gHi = '1110'
	hHi = '1111'

	if nibble == aLo:
		frequency=1300
	elif nibble == bLo:
		frequency=1400
	elif nibble == cLo:
		frequency=1500
	elif nibble == dLo:
		frequency=1600
	elif nibble == eLo:
		frequency=1700
	elif nibble == fLo:
		frequency=1800
	elif nibble == gLo:
		frequency=1900
	elif nibble == hLo:
		frequency=2000
	elif nibble == aHi:
		frequency=2100
	elif nibble == bHi:
		frequency=2200
	elif nibble == cHi:
		frequency=2300
	elif nibble == dHi:
		frequency=2400
	elif nibble == eHi:
		frequency=2500
	elif nibble == fHi:
		frequency=2600
	elif nibble == gHi:
		frequency=2700
	elif nibble == hHi:
		frequency=2800

	createSound(sound, frequency)



'''	 original sequence of frequencies
	if nibble == aLo:
		frequency=400
	elif nibble == bLo:
		frequency=600
	elif nibble == cLo:
		frequency=800
	elif nibble == dLo:
		frequency=1000
	elif nibble == eLo:
		frequency=1200
	elif nibble == fLo:
		frequency=1400
	elif nibble == gLo:
		frequency=1600
	elif nibble == hLo:
		frequency=1800
	elif nibble == aHi:
		frequency=2000
	elif nibble == bHi:
		frequency=2200
	elif nibble == cHi:
		frequency=2400
	elif nibble == dHi:
		frequency=2600
	elif nibble == eHi:
		frequency=2800
	elif nibble == fHi:
		frequency=3000
	elif nibble == gHi:
		frequency=3200
	elif nibble == hHi:
		frequency=3400
'''
	

	

#method to actually play the sound: length = how long it plays, rate=sample rate of device
def createSound(sound, frequency, length=0.2, rate=RATE): 
	chunk = createSineWave(frequency, length, rate)
	#print 'Chunk: ', chunk
	#print 'chunk size: ', len(chunk)
	sound.write(chunk.astype(numpy.float32).tostring()) #adds the chunks to the sound variable in 32bit format
	


#method to create the sine wave
def createSineWave(frequency, length, rate):
	length = int(length * rate)
	factor = float(frequency)*(math.pi*2)/rate 
	sineWave = numpy.sin(numpy.arange(length)*factor) #this uses numpy to create the sine wave
	return sineWave 



os.system("clear")
if len(sys.argv) != 2:
	print 
	print "********************************************************"
	print "* Incomplete command.  See examples below for usage:   *"
	print "*                                                      *"           
	print "*                   Standard Use                       *"
	print "*                                                      *"
	print "* From a text file:                                    *"
	print "* python modulator.py filename.txt                     *"
	print "********************************************************"  
	print 
	raw_input("Hit Enter To Return")
	quit()

p = pyaudio.PyAudio()
os.system('clear')
sound = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
binFileCheck = os.system("ls | grep 'modBinary.txt'")
if binFileCheck == 0:
	print "Do you want to delete previous binary.txt file"
	answer = raw_input("(Enter : Yes, CTRL-C : no) >")
	if answer == 'Yes' or answer == 'yes':
		os.system('clear')
		print "Successfully removed previous modBinary.txt file. Starting Modulation"
		os.system("rm modBinary.txt")
	else:
		print 'Exiting...'
		quit()
	 
fileName = sys.argv[1]
binaryFileName = convertToBinary(fileName) 
createNibble(binaryFileName)


sound.close()
p.terminate()




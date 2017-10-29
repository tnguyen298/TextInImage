#========================================================#
#	Thao Nguyen											 #
# 	CWID: 890848781										 #
#	CPSC 351 - Project 1: Text in Image				  	 #
#	Description: This program uses steganography to hide #
#	data from a text file to an image file. User can 	 #
# 	choose to embed or extract text from an image using  #
#	this program.										 #
#========================================================#


import sys
import os
from PIL import Image


#===========Declare all global variables here============#

imgFileName = ""
textFileName = ""


#========Declare and implement all functions here========#

# Function to extract an image
def extract_Image(imgFileName):
	# Open the image file
	img = openImageFileName(imgFileName)
	
	# If image cannot be opened
	if img == False:
		return 0
		

	# Test if image is in RGB mode
	if (img.mode == 'RGB'):
		width, height = img.size	# width and height of the image
		msgLen = 0					# length of the embedded message
		row = height - 1;			# start with the bottom row of the image
		lsb = ""					# string of all the retrieved LSBs 
		length = 0					# length of the LSB string
		
		# Retrieve the LSB of RGB for the first 11 pixels
		for col in range (width - 1, width - 12, -1):
			r, g, b = img.getpixel((col, row))
			lsb += (bin(r))[-1]		# append the LSB of R to LSB string
			lsb += (bin(g))[-1]		# append the LSB of G to LSB string
			lsb += (bin(b))[-1]		# append the LSB of B to LSB string
		
		# Store length of LSB string
		length = len(lsb)
		
		# Ignore the 33rd bit
		lsb = (lsb)[0:length-1]
		
		# Convert LSB string into integer, store it as length of message
		msgLen = int(lsb, 2)
					
		# Print the length of message extracted from the bottom right 11 pixels
		print ('Length of message is {} bits'.format(msgLen))
		
		# If the length is 0 
		if msgLen == 0:
			print ('No message is embedded.')
			return 0
		
		# Read the LSB of RGB for the next pixels
		index = 0		# index to iterate through the pixels
		lsb = ""		# reset the LSB string
		msg = ""		# store extracted message
		
		# Continue reading from the 12th pixel, bottom row
		for col in range (width - 12, 0, -1):
			r, g, b = img.getpixel((col, row))
			lsb += (bin(r))[-1]		# append the LSB of R to LSB string
			msgLen -= 1				# decrement the length of remaining message
			# Check if there is no more message to read
			if msgLen == 0: 
				break
				
			lsb += (bin(g))[-1]		# append the LSB of B to LSB string
			msgLen -= 1				# decrement the length of remaining message
			# Check if there is no more message to read
			if msgLen == 0: 
				break
				
			lsb += (bin(b))[-1]		# append the LSB of G to LSB string
			msgLen -= 1				# decrement the length of remaining message
			# Check if there is no more message to read
			if msgLen == 0: 
				break

		# At the end of bottom row, if there is still remaining message to read
		if msgLen > 0:
			# Continue reading from the remaining rows
			for row in range (height - 2, 0, -1):
				for col in range (width - 1, 0, -1):
					r, g, b = img.getpixel((col, row))
					lsb += (bin(r))[-1]		# append the LSB of R to LSB string
					msgLen -= 1				# decrement the length of remaining message
					# Check if there is no more message to read
					if msgLen == 0: 
						break
				
					lsb += (bin(g))[-1]		# append the LSB of B to LSB string
					msgLen -= 1				# decrement the length of remaining message
					# Check if there is no more message to read
					if msgLen == 0: 
						break
				
					lsb += (bin(b))[-1]		# append the LSB of G to LSB string
					msgLen -= 1				# decrement the length of remaining message
					# Check if there is no more message to read
					if msgLen == 0: 
						break
						
				# At the end of a row, check if there is no more message to read		
				if msgLen == 0: 
					break						
		# Update the length of the LSB string		
		length = len(lsb)
		
		# Iterate through the LSB string
		while index < length:
			# Store every 8 bits into temp
			temp = lsb[index : index + 8]
			
			# Convert temp from binary string to integer
			tempInt = int(temp, 2)
			
			# Convert tempInt from interger to char
			tempChar = chr(tempInt)
			
			# Append to tempChar extracted message
			msg += tempChar
			
			# Go to the next 8 bits
			index += 8
		
		# Print out the extracted message	
		print ('Embedded message is:')
		print ()
		print ('{}'.format(msg))
						
	else:
		# If the image is not in RGB mode, print error
		print ('{} is not in RGB mode. Cannot extract image.'.format(imgFileName))

	return 0

# Function to embed an image
def embed_Image(textFileName, imgFileName):
	# Open the image file
	img = openImageFileName(imgFileName)
	
	# If image cannot be opened
	if img == False:
		return False
	
	# Open text file and input text to embed from file
	text = inputTextFromFile(textFileName)
	
	# If text file can be opened
	if text:
		# Print string found from text file
		print ('String to embed is: ')
		print ()
		print ('{}'.format(text))
	# If text file cannot be opened, print error
	else:
		print ('Please try again with a valid text file name.')
		return False
	
	# Make a copy of the original file	
	embedded = img.copy()
	
	# If original file is jpg
	if imgFileName.lower().endswith('.jpg'):
		# Convert to png
		embeddedImgFileName = "embedded_" + imgFileName[0:-4] + ".png"	
	elif imgFileName.lower().endswith('.jpeg'):
		# Convert to png
		embeddedImgFileName = "embedded_" + imgFileName[0:-5] + ".png"	
	else:
		# Keep it png and prepend new name
		embeddedImgFileName = "embedded_" + imgFileName
	
	# Convert text to string of binary
	strBin = ""			# store text as a binary string
	# Iterate through every character in text
	for c in text:
		# Convert character to ASCII code, then to binary
		temp = bin(ord(c))[2:]		# ignoring the first 2 characters ('0b')
		tempLen = len(temp)			# store length of temp
		prependTemp = ""		# store prepending string
		
		# Loop until temp is 8 bits
		while tempLen < 8:
			# Keep prepending 0 until temp is 8 bits long
			prependTemp += '0'
			tempLen += 1
		# Add prepending 0's to temp
		tempStr = str(prependTemp) + temp
		
		# Check again to see if tempStr is 8 bits
		if len(tempStr) == 8:
			# Add to string of binary to embed
			strBin += tempStr
		else:
			# If not 8 bits, print error
			print('{} is not an ASCII char, binary is {}, of {} bits'.format(c, tempStr, len(tempStr)))

	# Get the length of string of binary to embed
	msgLenInBits = len(strBin)
	# Convert length to string of binary
	msgLenBin = (bin(msgLenInBits))[2:] # ignoring the first 2 characters ('0b')
	
	# If the length in binary is less than 32 bits long
	if len(msgLenBin) < 32:
		temp = msgLenBin
		prependMsgLen = ""
		# Prepend 0's until it is 32 bits long
		for i in range (0, 32 - len(msgLenBin)):
			prependMsgLen += '0'
		msgLenBin = prependMsgLen
		msgLenBin += temp
	# If the length in binary is more than 32 bits long
	elif len(msgLenBin) > 32:
		print ('String is too long. Cannot embed.')
		return False
		
	# Print the length in binary
	print ('String length is {} bits'.format(msgLenInBits))
	
	# Start embedding the length in binary
	# Check if the image is in RGB mode
	if (img.mode == 'RGB'):
		width, height = img.size	# width and height of the image
		index = 0					# index to iterate through the image
		row = height - 1;			# start with the bottom row

		# Embed length of message into the LSB of 
		# RGB for the first 11 pixels
		# Iterate through the bottom right 10 pixels
		for col in range (width - 1, width - 11, -1):
			r, g, b = img.getpixel((col, row))
			# Get all the bits of R except the LSB, store to newR
			newR = (bin(r))[0:len(bin(r)) - 1]
			# Append the LSB from msgLenBin to newR
			newR += msgLenBin[index]
			# Convert newR back to int and place back into R
			r = int(newR, 2)
			# Go to the next bit in msgLenBin
			index += 1
			
			# Get all the bits of G except the LSB, store to newG
			newG = (bin(g))[0:len(bin(g)) - 1]
			# Append the LSB from msgLenBin to newG
			newG += msgLenBin[index]
			# Convert newG back to int and place back into G
			g = int(newG, 2)
			# Go to the next bit in msgLenBin
			index += 1
			
			# Get all the bits of B except the LSB, store to newB
			newB = (bin(b))[0:len(bin(b)) - 1]
			# Append the LSB from msgLenBin to newB
			newB += msgLenBin[index]
			# Convert newB back to int and place back into B
			b = int(newB, 2)
			# Go to the next bit in msgLenBin
			index += 1
			
			# Place the new RGB values back into the pixel
			embedded.putpixel((col, row), (r, g, b))
		
		# For the bottom right 11th pixel, manually add the last 2 bits of msgLenBin 
		# to LSB of R and G, ignoring the last bit of B
		r, g, b = img.getpixel((width - 12, row))
		
		newR = (bin(r))[0:len(bin(r)) - 1]
		newR += msgLenBin[index]
		r = int(newR, 2)
		index += 1
			
		newG = (bin(g))[0:len(bin(g)) - 1]
		newG += msgLenBin[index]
		g = int(newG, 2)
		index += 1
		# Place the new RGB values back into the bottom right 11th pixel
		embedded.putpixel((width - 12, row), (r, g, b))
		
		# Embed the strBin into the next pixels' LSB
		index = 0		# reset index
		
		# Embed the message strBin starting with the 12th pixel, bottom row
		for col in range (width - 12, 0, -1):
			r, g, b = img.getpixel((col, row))

			newR = (bin(r))[0:len(bin(r)) - 1]
			newR += strBin[index]
			r = int(newR, 2)
			index += 1
			# Check if there is any more message to embed
			if index >= len(strBin):
				embedded.putpixel((col, row), (r, g, b))
				break;
			
			newG = (bin(g))[0:len(bin(g)) - 1]
			newG += strBin[index]
			g = int(newG, 2)
			index += 1
			if index >= len(strBin):
				embedded.putpixel((col, row), (r, g, b))
				break;
			
			newB = (bin(b))[0:len(bin(b)) - 1]
			newB += strBin[index]
			b = int(newB, 2)
			index += 1
			if index >= len(strBin):
				embedded.putpixel((col, row), (r, g, b))
				break;
			
			embedded.putpixel((col, row), (r, g, b))
		
		# By the end of bottom row, if there is still message to embed:
		if index < len(strBin):		
			# Iterate from the second bottom row to top
			for row in range (height - 2, 0, -1):
				# Iterate from right to left
				for col in range (width - 1, 0, -1):
					r, g, b = img.getpixel((col, row))
					
					# Embedding the bits from strBin to LSB of RGB
					newR = (bin(r))[0:len(bin(r)) - 1]
					newR += strBin[index]
					r = int(newR, 2)
					index += 1
					if index >= len(strBin):
						embedded.putpixel((col, row), (r, g, b))
						break;
			
					newG = (bin(g))[0:len(bin(g)) - 1]
					newG += strBin[index]
					g = int(newG, 2)
					index += 1
					if index >= len(strBin):
						embedded.putpixel((col, row), (r, g, b))
						break;
			
					newB = (bin(b))[0:len(bin(b)) - 1]
					newB += strBin[index]
					b = int(newB, 2)
					index += 1
					if index >= len(strBin):
						embedded.putpixel((col, row), (r, g, b))
						break;
 	
					embedded.putpixel((col, row), (r, g, b))
 				# At the end of a row, check if there is still message to embed
				if index == len(strBin):
					break;
		
		# After done embedding, save the embedded image
		embedded.save(embeddedImgFileName)
		return embedded
	# If the image is not in RGB mode, print error
	else:
		print ('{} is not in RGB mode. Cannot embed image.'.format(imgFileName))
		return False
	

# Function to open text file and input text to embed
def inputTextFromFile(textFileName):
	try:
		# Opening the file
		fileObj = open(textFileName, 'r')
		
	except IOError:
		# If unable to open file
		print ('Could not open file {} to read.'.format(textFileName))
		return False	
		
	# Get file size
	fileSize = (os.stat(textFileName)).st_size
	
	# Input text to embed
	text = fileObj.read(fileSize)
	
	return text

# Opens the image file
def openImageFileName(fileName):
	try:
		# Opening the image file
		img = Image.open(fileName)
		return img
		
	except IOError:
		# If unable to open file
		print ('Could not open file {} to read.'.format(fileName))
		return False

# Prints instruction on how to call program
def printInstructions():
	print ('USAGE: "python textInImage.py extract <IMAGE_FILE>"')
	print ('    or "python textInImage.py embed <IMAGE_FILE> <TEXT_FILE_TO_EMBED>"')
	print ('For python3: "python3 textInImage.py extract <IMAGE_FILE>"')
	print ('   	      or "python3 textInImage.py embed <IMAGE_FILE> <TEXT_FILE_TO_EMBED>"')
	print ('<IMAGE_FILE> to embed must be in RGB mode, of .png, .jpg, or .jpeg type;')
	print ('<IMAGE_FILE> to extract must be in RGB mode, of .png type;')
	print ('<TEXT_FILE_TO_EMBED> must be of .txt type and contains ASCII characters only.')
	

#======================Main Program=========================#
# Check user syntax
# If there are not enough arguments
if len(sys.argv) < 3:
	print ('Not enough arguments.')
	printInstructions()

# If user wants to extract
elif sys.argv[1] == "extract":
	# Input image file name
	imgFileName = sys.argv[2]
	# Check if file is .png type
	if imgFileName.lower().endswith('.png'):
		print ('Extracting image {}...'.format(imgFileName))
		extract_Image(imgFileName)
	else:
		print ('Image file is not a .png type.')
		print ('Please try again with the correct image file type.')

# If user wants to embed
# Check if there are enough arguments
elif sys.argv[1] == "embed" and len(sys.argv) < 4:
	print ('Not enough arguments.')
	printInstructions()

# If there are enough arguments for embed	
elif sys.argv[1] == "embed" and len(sys.argv) == 4:
	# Input text file name and image file name
	textFileName = sys.argv[3]
	imgFileName = sys.argv[2]
	# Check if file type is .png, .jpg, or .jpeg
	if imgFileName.lower().endswith(('.png', '.jpg', '.jpeg')):
		print ('Embedding {} into {}...'.format(textFileName, imgFileName))
		embed_Image(textFileName, imgFileName)
	else:
		print ('Image file is not a .png or .jpg type.')
		print ('Please try again with the correct image file type.')
		
else:
	print ('Wrong syntax.')
	printInstructions()
 

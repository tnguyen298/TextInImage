1/ Name:
	Thao Nguyen
	CWID: 890848781
	CPSC 353 - Project 1: Text in Image
	October 27, 2017

2/ Brief Description of Project:
	Using the art of steganography, this project hides text in an image
	by translating the text into binary bits, then store these bits into
	the least significant bits of each RGB value in each pixel of the
	image. The program uses the bottom right 11 pixels of the image to
	hide the text length, then continues using the remaining pixels to
	hide the actual text, following the order from right to left, bottom
	to top.
	The program is written using Python 3 and Pillow, a fork of the Python
	Imaging Library (PIL https://python-pillow.org/).
	It can consume a png or jpeg image, hide a txt text file to it, and
	produces an embedded png image. It can also extract text from an
	embedded png image. The text to be used for embedding and extracting
	needs to be in form of standard ASCII characters only (the character
	ASCII code does not exceed 8 bits).
	
3/ How to execute the program:
	a) Prerequisites:
		+ Linux OS (preferrably Ubuntu)
		+ Python 3
		+ Pillow (please follow the steps listed in this link and install
		Pillow onto your computer: 
		https://pillow.readthedocs.io/en/latest/installation.html)
	
	b) How to execute:
		+ Please download the source code textInImage.py from: 
		https://github.com/tnguyen298/TextInImage
		
		+ On a terminal, please navigate to where the downloaded 
		textInImage.py file is.
		
		+ To embed a text file (.txt) into an image file, please make 
		sure you have the control access to text file and image file,
		the image file needs to be in RGB mode, and is a png or a jpeg
		file. Type the following command to start embedding:
		
		$ python3 textInImage.py embed <IMAGE_FILE_NAME> <TEXT_FILE_NAME>
			
			<IMAGE_FILE_NAME> can be the name of the image file in the current
			directory, or a path to it.
			<TEXT_FILE_NAME> can be the name if the text file in the current
			directory, or a path to it.
			
		+ To extract text from an embedded image, please make sure you have
		the control access to the image file. The image also needs to be in
		RGB mode, and it is a png file. Type the following command to start
		extracting:
		
		$ python3 textInImage.py extract <IMAGE_FILE_NAME>
			
			<IMAGE_FILE_NAME> can be the name of the image file in the current
			directory, or a path to it.

4/ Files included in this submission:
	+ Documented source code: textInImage.py
	+ Image with embedded source code: Image_with_Source_Code.png
	+ A README file: README.txt
	+ Testing image files:
		a) Given testing image file: testImage.png
		b) RGB jpeg files: testImage1.jpg, tacocat.jpg
		c) RGB png file: testImage1.png
		d) Grayscale file (program will not embed/extract): testImageGray.png
	+ Testing text files:
		a) A short text file: textTest.txt
		b) A long text file: LongTextTestFile.txt
	+ Screenshots:
		a) Screenshot of extracting testImage.png
		b) Screenshot of embedding and extracting tacocat.jpg with testText.txt
		c) Screenshot of some user input error checkings
	
		
	

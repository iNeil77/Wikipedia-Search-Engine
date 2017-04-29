import re
import matplotlib.pyplot as plt
import operator
import required_data

def add_element(element):
	'''
		Add element to the list of tokens
	'''
	if element != ' ':
		element = element.lower()
		tokens.append(element)
		if element in tokendictionary:
			tokendictionary[element] += 1
		else:
			tokendictionary[element] = 1

def sort_dictionary(dictionary):
	return sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)

def process_main_string(textinput):
	'''
		Add space before and after special characters
	'''
	for i in gapsadder:
		textinput = textinput.replace(i, ' ' + i + ' ')
	return textinput

def handle_gaps(textinput):
	'''
		Remove extra spaces
	'''
	pattern = re.compile(r"\s+")
	textinput = re.sub(pattern, " ", textinput)
	return textinput

def preprocess(textinput):
	'''
		Handle spacing
	'''
	textinput = process_main_string(textinput)
	textinput = handle_gaps(textinput)
	return textinput

def check_for_abbreviations(inputtext):
	'''
		Add abbreviations like Mr. etc to the list of tokens
	'''
	if flag == 0
		if inputtext in abr:
			add_element(inputtext)
			return 1
		return 0
	return 1

def check_for_shortforms(inputtext, inputtextnext, i, flag):
	if flag == 0:
		pattern = re.compile(r"^([A-Z]\.)+$")
		if re.match(pattern, inputtext):
			if inputtextnext in dictionary or inputtextnext in stopwords:
				add_element(inputtext)
			else:
				newtokens = inputtext.split('.')
				for j in range(0,len(newtokens)-1):
					appendtext = newtokens[j]+'.'
					add_element(appendtext)
			return 1
		return 0
	return 1

def check_for_special_inverted_commas(inputtext, flag):
	if flag == 0:
		pattern = re.compile("(\w+n't)$")
		pattern1 = re.compile("(\w+'\w+)$")
		if inputtext.startswith("'") and inputtext.endswith("'"):
			inputtext = inputtext.split("'")[1]
			add_element(inputtext)
			return 1
		elif inputtext.endswith("n't"):
			inputtext = inputtext[0:-3]
			add_element(inputtext)
			inputtext = "n't"
			add_element(inputtext)
			return 1
		elif re.match(pattern1, inputtext):
			inputtext = inputtext.split("'")
			add_element(inputtext[0])
			inputtext[1] = "'" + inputtext[1]
			add_element(inputtext[1])
			return 1
		return 0
	return 1

def check_for_full_stops(inputtext, flag):
	if flag == 0:
		pattern = re.compile(r'[.]+$')
		if(re.search(pattern, inputtext)):
			inputtext = inputtext.replace(re.search(pattern, inputtext).group(), ' '+ re.search(pattern, inputtext).group())
			inputtext = inputtext.split()
			for i in range(0,len(inputtext)):
				add_element(inputtext[i])
			return 1
		return 0
	return 1

def check_for_slashes(inputtext, flag):
	if flag == 0:
		if "/" in inputtext:
			pattern = re.compile("[0-9]+/[0-9]+")
			if re.match(pattern, inputtext):
				add_element(inputtext)
			else:
				inputtext = inputtext.split("/")
				add_element(inputtext[0])
				add_element(inputtext[1])
			return 1
		return 0
	return 1

def check_for_operands(textinput, flag):
	if flag == 0:
		if re.search(r">|<|>=|<=|=|==|===", textinput):
			textreq = textinput.split(re.search(r">|<|>=|<=|=|==|===", textinput).group())
			for i in textreq:
				if i != '':
					add_element(i)
			return 1
		return 0
	return 1

def check_for_dashes(inputtext, flag):
	if flag == 0:
		if re.match(r"^(\w+-)+\w+$", inputtext):
			inputtext = inputtext.split("-")
			for i in range(0, len(inputtext)-1):
				add_element(inputtext[i])
				add_element("-")
			add_element(inputtext[len(inputtext)-1])
			return 1
		return 0
	return 1

def check_for_date(textinput, flag):
	#TODO change data regex
	if flag == 0:
		if re.match(r"\d{1,2}/\d{1,2}/\d{2,4}", textinput) or re.match(r"\d{1,2}-\d{1,2}-\d{2,4}", textinput):
			add_element(textinput)
			return 1
		return 0
	return 1

def process(textinput):
	'''
		Perform the main task
	'''
	textinput = textinput.split(" ")
	for i in range(0,len(textinput)):
		if(len(textinput[i]) > 0):
			flag = 0
			flag = check_for_abbreviations(textinput[i])
			flag = check_for_date(textinput[i], flag)
			flag = check_for_dashes(textinput[i], flag)
			try:
				flag = check_for_shortforms(textinput[i],textinput[i+1],i,flag)
			except:
				flag = check_for_shortforms(textinput[i],"is",i,flag)
			flag = check_for_operands(textinput[i],flag)
			#flag = check_for_special_inverted_commas(textinput[i],flag)
			flag = check_for_slashes(textinput[i],flag)
			flag = check_for_full_stops(textinput[i],flag)
			if(flag == 0):
				add_element(textinput[i])

def write_output():
	reqdictionary = sort_dictionary(tokendictionary)
	f1=open("unigram_english_output.txt", "w")
	for key in reqdictionary:
		f1.write(key[0]+"\t\t:\t"+str(key[1])+"\n")
	f1.close()

def plot():
	reqvalues = tokendictionary.values()
	reqvalues.sort(reverse = True)
	plt.plot(reqvalues[:1000])
	plt.xlabel('rank')
	plt.ylabel('frequency')
	plt.show()

def tokenise():
	global tokens
	global tokendictionary
	tokens = []
	tokendictionary = dict()
	lines = [line.rstrip('\n') for line in open('English.txt')]
	for line in lines:
		if len(line)!= 0:
			line = preprocess(line)
			process(line)
	return [tokens, sort_dictionary(tokendictionary)]

def rot(c,n):
	""" Will shift the letter by n in the alphabet
	"""
	val = ord(c)
	newVal = val + n%26
	if val >= 65 and val <= 90:
		if newVal > 90:
			return chr(newVal-26)
		else:
			return chr(newVal)
	if val >= 97 and val <= 122:
		if newVal > 122:
			return chr(newVal-26)
		else:
			return chr(newVal)
	else:
		return chr(val)








def encipher(string, n):
	encipherString = ""
	for letter in string:
		encipherString += rot(letter,n)
	return encipherString
import plex

class ParseError(Exception):
	pass

class ParseRun(Exception):
	pass

class MyParser:
	def __init__(self):
		papaki = plex.Str('(',')') # parentheseis
		letter = plex.Range('azAZ') # kathorismos oriou timwn gia grammata
		digit = plex.Range('09') # kathorismos oriou timwn gia arithmous
		name = letter+plex.Rep(letter|digit) # onoma metavlitis gia anathesi
		keyword = plex.Str('print','PRINT') # diavasma PRINT kai print gia ektipwsi
		space = plex.Any(" \n\t") # ti tha agnoei
		operator=plex.Str('AND','OR','XOR','=') # bitwise operators kai = gia anathesi
		bit = plex.Range('01') # kathorismos oriou timwn gia bit
		bits = plex.Rep1(bit) # 1 i parapanw bits
		self.st = {} # arxikopoiw to leksiko
		self.lexicon = plex.Lexicon([ 
			(operator,plex.TEXT), # plex.TEXT gia na epistrefei san string ton operator
			(bits,'BIT_TOKEN'), # epestrepse BIT_TOKEN otan diavaseis bits
			(keyword,'PRINT'), # epestrepse PRINT meta apo to diavasma print i PRINT
			(papaki,plex.TEXT), # epestrepse san string tin parenthesi
			(name,'IDENTIFIER'), # epestrepse IDENTIFIER otan diavazeis onoma_metavlitis
			(space,plex.IGNORE) # agnoise 
			])

	def create_scanner(self,fp):
		self.scanner = plex.Scanner(self.lexicon,fp)
		self.la,self.text=self.next_token()

	def next_token(self):
		return self.scanner.read()

	def match(self,token):
		if self.la==token:
			self.la,self.text=self.next_token()
		else:
			raise ParseError("den leitoyrgei swsta giati leipei ! ? (")

	def parse(self,fp):
		self.create_scanner(fp)
		self.stmt_list()
		
	def stmt_list(self):
		if self.la=='IDENTIFIER' or self.la=='PRINT':
			self.stmt()
			self.stmt_list()
		elif self.la==None:
			return
		else:
			raise ParseError("den leitoyrgei swsta giati leipei IDENTIFIER h Print")
	def stmt(self):
		if self.la=='IDENTIFIER':
			varname= self.text
			self.match('IDENTIFIER')
			self.match('=')
			e=self.expr()
			self.st[varname]= e
		elif self.la=='PRINT':
			self.match('PRINT')
			e=self.expr()
			print('{:b}'.format(e))
		else:
			raise ParseError("den leitoyrgei swsta giati leipei IDENTIFIER h PRINT")
	def expr(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BIT_TOKEN':	
			t=self.term() # aristera meros toy XOR
			while self.la=='XOR' :
				self.match('XOR')
				t2=self.term() # deksi meros toy Xor
				t ^= t2
			if self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
				return t
			else:
				raise ParseError("den leitoyrgei swsta giati leipei + h -")
		else:
			raise ParseError("den leitoyrgei swsta giati leipei ( or IDENTIFIER h bit h )")
	
	def term(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BIT_TOKEN':	
			t=self.factor()
			while self.la=='OR' :
				self.match('OR')
				t2=self.factor()
				t |= t2
			if self.la=='XOR' or self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
				return t
			else:
				print(self.la)
				raise ParseError("den leitoyrgei swsta giati leipei (h IDENTIFIER h bit h )")
		else:
			raise ParseError("den leitoyrgei swsta giati leipei * or /")
	def factor(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BIT_TOKEN':	
			t=self.atom()
			while self.la=='AND' :
				self.match('AND')
				t2=self.atom()
				t &= t2
			if self.la=='XOR'or self.la=='OR' or self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
				return t
			else:
				print(self.la)
				raise ParseError("den leitoyrgei swsta giati leipei (h IDENTIFIER h bit h )")
		else:
			raise ParseError("den leitoyrgei swsta giati leipei * or /")
	def atom(self):
		if self.la=='(':
			self.match('(')
			e=self.expr()
			self.match(')')
			return e
		elif self.la=='IDENTIFIER':
			varname = self.text
			self.match('IDENTIFIER')
			if varname in self.st:
				return self.st[varname]
			raise ParseRun("den leitoyrgei swsta giati leipei id poy exei arxikopoih8h")
		elif self.la=='BIT_TOKEN':
			value=int(self.text,2)
			self.match('BIT_TOKEN')
			return value
		else:
			raise ParseError("den leitoyrgei swsta giati leipei id bit h (")

parser = MyParser()
with open('dikom.txt','r') as fp:
	parser.parse(fp)

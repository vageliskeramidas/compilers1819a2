import plex

class ParseError(Exception):
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
			raise ParseError("den leitoyrgei swsta giati leipei )")

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
			self.match('IDENTIFIER')
			self.match('=')
			self.expr()
		elif self.la=='PRINT':
			self.match('PRINT')
			self.expr()
		else:
			raise ParseError("den leitoyrgei swsta giati leipei IDENTIFIER h PRINT")
	def expr(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BIT_TOKEN':	
			self.term()
			self.term_tail()
		else:
			raise ParseError("den leitoyrgei swsta giati leipei ( h IDENTIFIER h BIT h )")
	def term_tail(self):
		if self.la=='XOR':
			self.match('XOR')
			self.term()
			self.term_tail()
		elif self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("den leitoyrgei swsta giati leipei + h -")
	def term(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BIT_TOKEN' or self.la==')':	
			self.factor()
			self.factor_tail()
		else:
			raise ParseError("den leitoyrgei swsta giati leipei ( h IDENTIFIER h bit h )")
	def factor_tail(self):
		if self.la=='OR' :
			self.match('OR')
			self.factor()
			self.factor_tail()
		elif self.la=='XOR' or self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("den leitoyrgei swsta giati leipei * or /")
	def factor(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='BIT_TOKEN' or self.la==')':	
			self.atom()
			self.atom_tail()
		else:
			raise ParseError("den leitoyrgei swsta giati leipei ( h IDENTIFIER h bit h )")
	def atom_tail(self):
		if self.la=='AND' :
			self.match('AND')
			self.atom()
			self.atom_tail()
		elif self.la=='XOR' or self.la=='OR' or self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("den leitoyrgei swsta giati leipei * or /")
	def atom(self):
		if self.la=='(':
			self.match('(')
			self.expr()
			self.match(')')
		elif self.la=='IDENTIFIER':
			self.match('IDENTIFIER')
		elif self.la=='BIT_TOKEN':
			self.match('BIT_TOKEN')
		else:
			raise ParseError("den leitoyrgei swsta giati leipei id bit h (")

parser = MyParser()
with open('dikom.txt','r') as fp:
	parser.parse(fp)

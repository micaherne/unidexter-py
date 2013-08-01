class Engine():

	r = None
	f = None # file
	d1 = None # diagonals a1h8 
	d2 = None # diagonals a8h1
	set = None
	wtm = None
	castling = None
	halfmove = None
	fullmove = None
	
	# d1
	# 01234567
	# 12345678
	# 23456789
	# 3456789A
	# 456789AB
	# 56789ABC
	# 6789ABCD
	# 789ABCDE
	
	# diagonal = 7 + f - r
	# pos 0-7 = f
	# pos 8 - 15 = r
	
	# d2
	# 789ABCDE
	# 6789ABCD
	# 56789ABC
	# 456789AB
	# 3456789A
	# 23456789
	# 12345678
	# 01234567
	
	# diagonal = f + r
	# pos 0 - 7 = f
	# pos 7 - 15 = (7 - r)
	
	def __init__(self):
		self.set = Set()
		self.r = [[None for _ in range(8)] for _ in range(8)] # rank
		self.f = [[None for _ in range(8)] for _ in range(8)] # file
		self.d1 = [[None for _ in range(8)] for _ in range(16)] # diagonals a1h8 
		self.d2 = [[None for _ in range(8)] for _ in range(16)] # diagonals a8h1
		self.wtm = None
		self.castling = [None for _ in range(4)]
		self.halfmove = None
		self.fullmove = None
		
		
	def generatePseudoLegalMoves(self):
		result = []
		return result
		for p in self.set.pieces:
			if p.r == None or p.f == None:
				continue # it's not in play any more
			if p.pieceType == Piece.PAWN:
				continue # TODO: do pawn moves (KEEP continue!)
			if p.pieceType == Piece.KNIGHT:
				continue # TODO: do knight moves (KEEP continue!)
			
			assert p.pieceType > 3
			
			# Do sliders
			maxMoves = 8
			if p.pieceType == Piece.KING:
				maxMoves = 1
			if p.pieceType & 2: # linear slider
				pass
			if p.pieceType & 1: # diagonal slider
				pass
				
		return result
			
	def fromFEN(self, fen):
		self.set.resetPieces()
		
		fenParts = fen.split(" ")
		boardParts = fenParts[0].split("/")

		if len(boardParts) != 8:
			raise Exception("FEN must have 8 parts for board")

		for i in range(8):
			r = 7 - i
			f = 0
			for ch in boardParts[i]:
				if ord(ch) in range(ord('1'), ord('9')):
					f += int(ch)
				else:
					piece = self.set.getUnusedPiece(Piece.NOTATIONREPRESENTATION[ch.upper()], Piece.WHITE if ch.isupper() else Piece.BLACK)
					self.placePiece(piece, f, r)
					f += 1

		# Colour to move
		self.wtm = (fenParts[1] == 'w')
		
		# Castling rights
		self.castling = ['KQkq'[i] in fenParts[2] for i in range(4)]
		
		# En passent
		if (fenParts[3] != '-'):
			f, r = self.parseSquare(fenParts[3])
			self.placePiece(self.set.epmarker, f, r)
			
		if len(fenParts) > 4:
			self.halfmove = int(fenParts[4])
			
		if len(fenParts) > 5:
			self.fullmove = int(fenParts[5])
				
	def startPos(self):
		return self.fromFEN('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
	
	def parseSquare(self, square):
		''' Parse an algebraic square into a (file, rank) tuple '''
		return (ord(square[0]) - ord('a'), int(square[1]) - 1)
	
	def placePiece(self, piece, f, r):
		piece.r = self.r[r]
		piece.f = self.f[f]
		# 7 + f - r is the diagonal in both cases
		piece.d1 = self.d1[7 + f - r]
		piece.d2 = self.d2[f + r]
		
		self.f[f][r] = piece
		self.r[r][f] = piece
		
		piece.fIndex = r
		piece.rIndex = f
		
		# algorithm for position along d1 diagonal:
		# diagonal number: 0-7 = f, (7)8-15 = r
		if (7 + f - r < 8):
			self.d1[7 + f - r][f] = piece
			piece.d1Index = f
		else:
			piece.d1Index = r
			self.d1[7 + f - r][r] = piece

		# algorithm for position along d2 diagonal:
		# diagonal number: 0-7 = f, (7)8-15 = (7 - r)
		if (f + r < 8):
			piece.d2Index = f
			self.d2[f + r][f] = piece
		else:
			piece.d2Index = 7 - r
			self.d2[f + r][7-r] = piece
			
	def positionToString(self):
		separator = "+-" * 8 + "+"
		lines = []
		for rank in range(7, -1, -1):
			lines.append(separator)
			r = self.r[rank]
			row = []
			for file in range(8):
				piece = r[file]
				if piece == None:
					rep = ' '
				else:
					rep = Piece.REPRESENTATION[piece.pieceType]
					if piece.colour == Piece.BLACK:
						rep = rep.lower()
				row.append(rep)
			lines.append("|" + "|".join(row) + "|")
		lines.append(separator)
		return "\n".join(lines)
		
class Set():
	
	pieces = [None] * 32
	epmarker = None
	space = None
	
	def __init__(self):
		self.resetPieces()
	
	def getUnusedPiece(self, pieceType, colour):
		for p in self.pieces:
			if p.pieceType == pieceType and p.colour == colour:
				if p.f == None:
					return p
				# TODO: Return promoted pawns if necessary
		raise Exception("No unused piece found")
		
	def resetPieces(self):
		self.pieces = []
		for i in range(2):
			for pc in [6, 2, 5, 7, 3, 5, 2, 6, 1, 1, 1, 1, 1, 1, 1, 1]:
				p = Piece(pc, i)
				self.pieces.append(p)
		self.epmarker = Piece(Piece.EPMARKER, None)
		self.space = Piece(Piece.EMPTY, None)
		
class Piece():
	
	pieceType = None
	colour = None
	r = None
	f = None
	d1 = None
	d2 = None
	
	rIndex = None
	fIndex = None
	d1Index = None
	d2Index = None
	
	promotedType = None
	
	PAWN = 1
	KNIGHT = 2
	KING = 3
	BISHOP = 5
	ROOK = 6
	QUEEN = 7
	
	EMPTY = 16
	EPMARKER = 17
	
	BLACK = 0
	WHITE = 1
	
	REPRESENTATION = { 0: " ", 1: "P", 2: "N", 3: "K", 5: "B", 6: "R", 7: "Q", 16: ' ', 17: ' '}
	NOTATIONREPRESENTATION = {v:k for k, v in REPRESENTATION.items()} # flip keys and values
	
	def __init__(self, pieceType, colour, r=None, f=None, d1=None, d2=None):
		self.pieceType = pieceType
		self.colour = colour
		self.r = r
		self.f = f  
		self.d1 = d1  
		self.d2 = d2
		
	def __str__(self):
		if self.colour == Piece.BLACK:
			return self.REPRESENTATION[self.pieceType].lower()
		else:
			return self.REPRESENTATION[self.pieceType]
		
		
		
if __name__ == '__main__':
	e = Engine()
	e.startPos()
	for i in e.set.pieces:
		print(i, i.f, i.r)
		
		

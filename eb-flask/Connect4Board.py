# Hw 10, pr2 for CS 5 gold, 2009
#
# The Board class from CS 5 Hw #10
# for use as a starting point for
# Hw#11, the Player class (and AI)
#

import random

class Board:
    """ a datatype representing a C4 board
        with an arbitrary number of rows and cols
    """

    def __init__( self, width=7, height=6 ):
        """ the constructor for objects of type Board """
        self.width = width
        self.height = height
        self.data = [ [' ']*width for row in range(height) ]
        # do not need to return inside a constructor!
        

    def __repr__(self):
        """ this method returns a string representation
            for an object of type Board
        """
        s = ''   # the string to return
        for row in range( self.height ):
            s += '|'   # add the spacer character
            for col in range( self.width ):
                s += self.data[row][col] + '|'
            s += '\n'

        s += '--'*self.width    # add the bottom of the board
        s += '-\n'
        
        for col in range( self.width ):
            s += ' ' + str(col%10)

        s += '\n'
        return s       # the board is complete, return it


    def set_board( self, LoS ):
        """ sets the board to the characters in the
            list of strings named LoS
        """
        for row in range( self.height ):
            for col in range( self.width ):
                self.data[row][col] = LoS[row][col]
                

    def setBoard( self, moves, show=True ):
        """ sets the board according to a string
            of turns (moves), starting with 'X'
            if show==True, it prints each one
        """
        nextCh = 'X'
        for move in moves:
            col = int(move)
            if self.allowsMove(col):
                self.addMove( col, nextCh )
            if nextCh == 'X': nextCh = 'O'
            else: nextCh = 'X'
            if show: print self


    def set( self, moves, show=True ):
        """ sets the board according to a string
            of turns (moves), starting with 'X'
            if show==True, it prints each one
        """
        nextCh = 'X'
        for move in moves:
            col = int(move)
            if self.allowsMove(col):
                self.addMove( col, nextCh )
            if nextCh == 'X': nextCh = 'O'
            else: nextCh = 'X'
            if show: print self

    def clear( self ):
        """ the software version of the little
            blue slider that releases all of the checkers!
        """
        for row in range(self.height):
            for col in range(self.width):
                self.data[row][col] = ' '

    def addMove( self, col, ox ):
        """ adds checker ox into column col
            does not need to check for validity...
            allowsMove will do that.
        """
        row = self.height - 1
        while row >= 0:
            if self.data[row][col] == ' ':
                self.data[row][col] = ox
                return
            row -= 1
        
    def addMove2( self, col, ox ):
        """ adds checker ox into column col
            does not need to check for validity...
            allowsMove will do that.
        """
        for row in range( self.height ):
            # look for the first nonempty row
            if self.data[row][col] != ' ':
                # put in the checker
                self.data[row-1][col] = ox
                return
        self.data[self.height-1][col] = ox

    def delMove( self, col ):
        """ removes the checker from column col """
        for row in range( self.height ):
            # look for the first nonempty row
            if self.data[row][col] != ' ':
                # put in the checker
                self.data[row][col] = ' '
                return
        # it's empty, just return
        return
        
    def allowsMove( self, col ):
        """ returns True if a move to col is allowed
            in the board represented by self
            returns False otherwise
        """
        if col < 0 or col >= self.width:
            return False
        return self.data[0][col] == ' '

    def isFull( self ):
        """ returns True if the board is completely full """
        for col in range( self.width ):
            if self.allowsMove( col ):
                return False
        return True

    def gameOver( self ):
        """ returns True if the game is over... """
        if self.isFull() or self.winsFor('X') or self.winsFor('O'):
            return True
        return False

    def isOX( self, row, col, ox ):
        """ checks if the spot at row, col is legal and ox """
        if 0 <= row < self.height:
            if 0 <= col < self.width: # legal...
                if self.data[row][col] == ox:
                    return True
        return False

    def winsFor( self, ox ):
        """ checks if the board self is a win for ox """
        for row in range( self.height ):
            for col in range( self.width ):
                if self.isOX( row, col, ox ) and \
                   self.isOX( row+1, col, ox ) and \
                   self.isOX( row+2, col, ox ) and \
                   self.isOX( row+3, col, ox ):
                    return True
                if self.isOX( row, col, ox ) and \
                   self.isOX( row, col+1, ox ) and \
                   self.isOX( row, col+2, ox ) and \
                   self.isOX( row, col+3, ox ):
                    return True
                if self.isOX( row, col, ox ) and \
                   self.isOX( row+1, col+1, ox ) and \
                   self.isOX( row+2, col+2, ox ) and \
                   self.isOX( row+3, col+3, ox ):
                    return True
                if self.isOX( row, col, ox ) and \
                   self.isOX( row+1, col-1, ox ) and \
                   self.isOX( row+2, col-2, ox ) and \
                   self.isOX( row+3, col-3, ox ):
                    return True
        return False

    def hostGame( self ):
        """ hosts a game of Connect Four """

        nextCheckerToMove = 'X'
        
        while True:
            # print the board
            print self

            # get the next move from the human player...
            col = -1
            while not self.allowsMove( col ):
                col = input('Next col for ' + nextCheckerToMove + ': ')
            self.addMove( col, nextCheckerToMove )

            # check if the game is over
            if self.winsFor( nextCheckerToMove ):
                print self
                print '\n' + nextCheckerToMove + ' wins! Congratulations!\n\n'
                break
            if self.isFull():
                print self
                print '\nThe game is a draw.\n\n'
                break

            # swap players
            if nextCheckerToMove == 'X':
                nextCheckerToMove = 'O'
            else:
                nextCheckerToMove = 'X'

        print 'Come back soon 4 more!'

        

    
    
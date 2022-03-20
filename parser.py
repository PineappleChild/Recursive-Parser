#Alexander Paulus
#This project turns a string formatted to be a certain grammar into an indented output of the same string following the ebnf grammar


class Token: #token class stores a catagory and value for each token
    def __init__ (self, tokenCat, tokenVal): #assigns token catagory and value to type and val, initializes type and val aswell
        self.type = tokenCat
        self.val = tokenVal
    def getTokenCatagory(self):#gets a token catagory
        return self.type
    def getTokenValue(self):#gets a token value
        return self.val
    def __repr__(self):
        if (self.type in ["INT", "FLOAT", "ID"]):#represents token as a string
            return self.val
        elif (self.type == "BODY"):
            return "body"
        elif (self.type == "B"):
            return "b"
        elif (self.type == "I"):
            return "i"
        elif (self.type == "UL"):
            return "ul"
        elif (self.type == "LI"):
            return "li"
        elif (self.type == "/BODY"):
            return "/body"
        elif (self.type == "/B"):
            return "/b"
        elif (self.type == "/I"):
            return "/i"
        elif (self.type == "/UL"):
            return "/ul"
        elif (self.type == "/LI"):
            return "/li"
        elif (self.type == "EOI"):
            return ""
        elif (self.type == "KINVALID"):
            return "invalid keyword"
        else:
            return "invalid string"

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"

class Lexer:# lexer class reads a string and converts the inputs into tokens, following the assigned grammar
    def __init__ (self, s):#assigns the inputted string to a newly initialized stmt and intializes index, calls nextchar to move index to first char
        self.stmt = s
        self.index = 0
        self.nextChar()
    def nextToken(self):#checks for keywords and strings and returns them as tokens
        while True:
            if self.ch == "<": #checks for keywords
                self.nextChar()
                value = self.consumeChars(LETTERS)
                self.nextChar()
                if self.checkIfKey(value.upper()):
                    return Token(value.upper(), value)
                else:
                    return Token("KINVALID", value)
            elif self.ch == ' ': #handles spaces
                self.nextChar()
            elif self.ch.isalpha(): # is a letter
                id = self.consumeChars(LETTERS+DIGITS)
                return Token("ID", id)
            elif self.ch.isdigit(): # is an int or float
                num = self.consumeChars(DIGITS)
                if self.ch != ".":
                    return Token("INT", num)
                num += self.ch
                self.nextChar()
                if self.ch.isdigit():
                    num += self.consumeChars(DIGITS)
                    return Token("FLOAT", num)
                else:
                    return Token("INVALID", num)
            elif self.ch =='$': #handles end of input
                return Token("EOI","")
            else: #handles invalid inputs
                return Token("INVALID", self.ch)

    def checkIfKey(self, value): #checks to see if value is a keyword
        if value in ["B", "BODY", "I", "UL", "LI", "/B", "/BODY", "/I", "/UL", "/LI"]:
            return True
        return False

    def nextChar(self): #increases the index of the string you are reading
        self.ch = self.stmt[self.index]
        self.index = self.index + 1

    def consumeChars (self, charSet): #reads over string and returns a string defined by a charset
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            if self.ch == ">": #checks for end of keyword
                return r
            r = r + self.ch
            self.nextChar()
        return r


class Parser:

    def __init__(self, s):#creates and assigns a lexer object, which appends an EOI symbol, and initializes a token to the first token
        self.lexer = Lexer(s+"$")
        self.token = self.lexer.nextToken()
    def run(self): #runs the program
        self.statement()
    def statement(self): #calls the first method to begin program
        spaceCounter = 0
        self.webpage(spaceCounter)

    def webpage(self, indent):#method for webpage following the webpage ebnf grammar
        print("<body>")
        self.token = self.lexer.nextToken()
        indent+=1
        self.text(indent)

    def text(self, indent):#method for text following the text ebnf grammar
        if self.token.getTokenCatagory() == "INVALID" or self.token.getTokenCatagory() == "KINVALID": #handles invalid tokens
            if self.token.getTokenCatagory() == "INVALID":
                print("Syntax error: expecting STRING; saw " + self.token.getTokenValue())
            else:
                print("Syntax error: expecting KEYWORD; saw <" + self.token.getTokenValue() + ">")
            exit(1)
        elif self.token.getTokenCatagory() in ["INT", "FLOAT", "ID"]: #letters and digits
            print(self.addSpace(indent) + self.token.getTokenValue())
        elif self.token.getTokenCatagory() in ["/B", "/BODY", "/I", "/UL", "/LI"]: #closing keywords
            indent -= 1
            print(self.addSpace(indent) + "<" + self.token.getTokenValue() + ">")
        elif self.token.getTokenCatagory() == "UL": #handles unordered lists
            print(self.addSpace(indent) + "<ul>")
            self.listItem(indent)
        elif self.token.getTokenCatagory() != "EOI": #handles end of input
            print(self.addSpace(indent) + "<" + self.token.getTokenValue() + ">")
            indent += 1;
        self.token = self.lexer.nextToken()
        if self.token.getTokenCatagory() != "EOI":
            self.text(indent)

    def addSpace(self, value):#adds a two spaces for each increment of value, returns a string of spaces
        newStr = ""
        for i in range(value):
            newStr += "  "
        return newStr

    def listItem(self, indent):#method for listItem following the listItem ebnf grammar
        print(self.addSpace(indent) + "<li>")
        self.token = self.lexer.nextToken()
        indent+=1
        self.text(indent)
        indent-=1

# print("<body> google <b><i><b> yahoo</b></i></b></body>\n\n")

parser = Parser ("<body> google <b><i><b> yahoo</b></i></b></body>");

# parser = Parser ("<body> google @ <b><i><b> yahoo</b></i></b></body>"); #testing error

# parser = Parser ("<body> google <b><i><b><ul><li>22.5</li>hello<li>hellotwo</li></ul>yahoo</b></i></b></body>"); #testing ul and li
#
# parser = Parser ("<body><b></b><i></i><b></b></body>"); #testing no string between keywords
#
# parser = Parser ("<body>one two three four five</body>"); #testing multiple strings without any keywords separating them
#
# parser = Parser ("<body><fakekey></fakekey></body>"); #checks if error message detects invalid keyword

parser.run();
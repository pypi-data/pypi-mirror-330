import typer
from pathlib import Path

app = typer.Typer(no_args_is_help=True)

import re
import sys

Priority = {
    'PROG'        : 1,
    'ASSIGNMENT'  : 2,
    'EXECUTABLE'  : 3,
    'CONDITIONAL' : 3,
    'LOGICAL'     : 4,
    'COMPARISON'  : 5,
    'SUM'         : 6,
    'PRODUCT'     : 7,
    'EXPONENT'    : 8,
    'PREFIX'      : 9,
    'POSTFIX'     : 10,
    'CALL'        : 11,
    'INCONTEXT'   : 12,
}
TokenTypes = {
    'BEGIN': 'BEGIN', 
    '(': 'LEFT_PAREN', 
    ')': 'RIGHT_PAREN',  
    ';': 'SEMICOLON', 
    ',': 'COMMA', 
    '::': 'DoubleColon',
    '.':  'DoubleColon',
    '{': 'LEFT_CURLY_PAREN', 
    '}': 'RIGHT_CURLY_PAREN', 
    'EOF ': 'EOF', 
    '=>': 'PROCESSOR',
    ':': 'COLON', 
    '?': 'QUESTION',
    'if': 'IF',
    'for': 'FOR',
    'while': 'WHILE',
    '=':  'ASSIGN',
    '+=': 'ASSIGN',
    '-=': 'ASSIGN',
    '*=': 'ASSIGN',
    '/=': 'ASSIGN',
    '%=': 'ASSIGN', 
    '&&': 'LOGICAL',
    '||': 'LOGICAL',
    '>>': 'LOGICAL',
    '<<': 'LOGICAL',
    '&':  'LOGICAL',
    '==': 'COMPARISON',
    '!=': 'COMPARISON',
    '<': 'COMPARISON',
    '>': 'COMPARISON',
    '<=': 'COMPARISON',
    '>=': 'COMPARISON',
    '+': 'PLUS', 
    '-': 'MINUS', 
    '*': 'ASTERISK', 
    '/': 'SLASH',
    '%': 'PRECENT', 
    '^': 'CARET', 
    '~': 'TILDE', 
    '!': 'BANG', 
    '++': 'INCREMENT',
    '--': 'DECREMENT',
}
TokenNames = {
    '+': '_add',
    '-': '_sub',
    '*': '_mul',
    '/': '_div',
    '>>': '_rsh',
    '<<': '_lsh',
    '%': '_mod',
    '=': '_eqs',
    '+=': '_adeq',
    '-=': '_sbeq',
    '*=': '_mleq',
    '/=': '_dveq',
    '%=': '_mdeq',
    '^': '_exp'
}
class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find(self, var):
        if self.outer == None: return self if (var in self) else None
        else: return self if (var in self) else self.outer.find(var)
class PrefixParselet:
    def Parse(self, parser, token):
        raise NotImplementedError("Class %s doesn't implement Parse()" % (self.__class__.__name__))
class InfixParselet:
    def Parse(self, parser, left, token):
        raise NotImplementedError("Class %s doesn't implement Parse()" % (self.__class__.__name__))
class PrefixOperatorParselet(PrefixParselet):
    def __init__(self, precedence, lambdafunc):
        self.precedence = precedence
        self.lambdafunc = lambdafunc
    def Parse(self, parser, token):
        right = parser.ParseExpression(self.precedence)
        return PrefixExpression(token, right, self.lambdafunc)
class PostfixOperatorParselet(InfixParselet):
    def __init__(self, precedence, lambdafunc):
        self.precedence = precedence
        self.lambdafunc = lambdafunc
    def Parse(self, parser, left, token):
        return PostfixExpression(left, token, self.lambdafunc)
    def GetPrecedence(self):
        return self.precedence
class ValueParselet(PrefixParselet):
    def Parse(self, parser, token):
        return ValueExpression(token)
class IfParselet(PrefixParselet):
    def Parse(self, parser, token):
        condition = parser.ParseExpression(0)
        consequence = parser.ParseExpression(0)
        elsewise = parser.ParseExpression(0)
        return IfExpression(condition, consequence, elsewise)
class ForParselet(PrefixParselet):
    def Parse(self, parser, token):
        range = parser.ParseExpression(0)
        each = parser.ParseExpression(0)
        return ForExpression(range, each)
class WhileParselet(PrefixParselet):
    def Parse(self, parser, token):
        condition = parser.ParseExpression(0)
        consequence = parser.ParseExpression(0)
        return WhileExpression(condition, consequence)
class GroupParselet(PrefixParselet):
    def Parse(self, parser, token):
        args = []
        if token.getType() == "LEFT_CURLY_PAREN":
            if not parser.match('RIGHT_CURLY_PAREN'):
                args.append(parser.ParseExpression())
                while parser.lookahead(1).getType() != "RIGHT_CURLY_PAREN" and parser.match("SEMICOLON"):
                    args.append(parser.ParseExpression())
            parser.consume("SEMICOLON")
            parser.consume("RIGHT_CURLY_PAREN")
            return GroupExpression(args, True)
        else:
            if not parser.match('RIGHT_PAREN'):
                args.append(parser.ParseExpression())
                while parser.match("COMMA"):
                    args.append(parser.ParseExpression())
                parser.consume("RIGHT_PAREN")
            return GroupExpression(args, False)
class ConditionalParselet(InfixParselet):
    def Parse(self, parser, left, token):
        thenArm = parser.ParseExpression()
        elseArm = parser.ParseExpression(1)
        return ConditionalExpression(left, thenArm, elseArm)
    def GetPrecedence(self):
        return 3
class CallParselet(InfixParselet):
    def Parse(self, parser, left, token):
        args = []
        if not parser.match('RIGHT_PAREN'):
            args.append(parser.ParseExpression())
            while parser.match("COMMA"):
                args.append(parser.ParseExpression())
            parser.consume("RIGHT_PAREN")
        return CallExpression(left, args)
    def GetPrecedence(self):
        return Priority['CALL']
class BinaryOperatorParselet(InfixParselet):
    def __init__(self, precedence, isright, lambdafunc):
        self.precedence = precedence
        self.isRight = isright
        self.lambdafunc = lambdafunc
    def Parse(self, parser, left, token):
        right = parser.ParseExpression(self.precedence - (1 if self.isRight else 0))
        return OperatorExpression(left, token, right, self.lambdafunc)
    def GetPrecedence(self):
        return self.precedence
class ProgramParselet(PrefixParselet):
    def Parse(self, parser, token):
        args = []
        args.append(parser.ParseExpression())
        while parser.lookahead(1).getType() != "EOF" and parser.match("SEMICOLON"):
            args.append(parser.ParseExpression())
        parser.read = []
        return ProgramExpression(args)
    def GetPrecedence(self):
        return Priority['PROG']
class Expression:
    def __str__(self):
        raise NotImplementedError("Class %s doesn't implement Print()" % (self.__class__.__name__))
class CallExpression(Expression):
    def __init__(self, function, args):
        self.function = function
        self.args = args
    def __str__(self):
        a = ""
        for i in range(0, len(self.args)):
            a += str(self.args[i])
            if i < len(self.args) - 1: a += ', '
        return str(self.function) + '(' + a + ')'
    def __call__(self, env):
        if str(self.function) == 'import': 
            if str(self.args[0]).endswith('.lc'):
                env['ExecFile'](str(self.args[0]))
            exec(open(str(self.args[0])).read())
        else: return self.function(env)(*(i(env) for i in self.args))
class GroupExpression(Expression):
    def __init__(self, args, isCurrlyParren):
        self.args = args
        self.isCurrlyParren = isCurrlyParren
    def __str__(self):
        a = ""
        for i in range(0, len(self.args)):
            a += ('    ' if self.isCurrlyParren else '') + str(self.args[i]).replace('\n','\n    ') + ((';') if self.isCurrlyParren else '')
            if i < len(self.args) - 1: a += ('\n' if self.isCurrlyParren else ', ')
        return ('{\n' if self.isCurrlyParren else '(') + a + ('\n}' if self.isCurrlyParren else ')')
    def __call__(self, env):
        try: return list(i(env) for i in self.args)[-1]
        except IndexError: return []
class ConditionalExpression(Expression):
    def __init__(self, cond, left, right):
        self.cond = cond
        self.left = left
        self.right = right
    def __str__(self):
        return '(' + str(self.cond) + ' ? ' + str(self.left) + ' : ' + str(self.right) + ')'
    def __call__(self, env):
        return self.left(env) if self.cond(env) else self.right(env)
class ValueExpression(Expression):
    def __init__(self, name):
        self.name = name
    def getName(self):
        return self.name
    def __str__(self):
        if str(self.name).startswith('"'):
            return str(self.name).lstrip('"').rstrip('"')
        return str(self.name)
    def __call__(self, env):
        try: return int(str(self.name))
        except ValueError:
            try: return float(str(self.name))
            except ValueError:
                if str(self.name).startswith('"'): return str(self.name).lstrip('"').rstrip('"')
                else:
                    if str(self.name) == 'this': return env
                    elif env.find(str(self.name)): return env.find(str(self.name))[str(self.name)]
                    else: return str(self.name)
class OperatorExpression(Expression):
    def __init__(self, left, op, right, lambdafunc):
        self.left = left
        self.op = op
        self.right = right
        self.lambdafunc = lambdafunc
    def __str__(self):
        return '(' + str(self.left) + ' ' + str(self.op) + ' ' + str(self.right) + ')'
    def __call__(self, env):
        if isinstance(self.left(env), Env):
            try: return self.left(env)[TokenNames[str(self.op)]](self.right(env))
            except KeyError: pass
        self.env = (a := self.lambdafunc(env, self.left, self.op, self.right))[1]
        return a[0]
class PostfixExpression(Expression):
    def __init__(self, left, op, lambdafunc):
        self.left = left
        self.op = op
        self.lambdafunc = lambdafunc
    def __str__(self):
        return '(' + str(self.left) + str(self.op) + ')'
    def __call__(self, env):
        self.env = (a := self.lambdafunc(env, self.left, self.op))[1]
        return a[0]
class PrefixExpression(Expression):
    def __init__(self, op, right, lambdafunc):
        self.op = op
        self.right = right
        self.lambdafunc = lambdafunc
    def __str__(self):
        return '(' + str(self.op) + str(self.right) + ')'
    def __call__(self, env):
        self.env = (a := self.lambdafunc(env, self.op, self.right))[1]
        return a[0]
class ProgramExpression(Expression):
    def __init__(self, args):
        self.args = args
    def __str__(self):
        a = ""
        for i in range(0, len(self.args)):
            a += str(self.args[i]) + ';'
            a += '\n'
        return a
    def __call__(self, env):
        return list(i(env) for i in self.args)[-1]
class IfExpression(Expression):
    def __init__(self, condition, consequence, elsewise):
        self.condition = condition
        self.consequence = consequence
        self.elsewise = elsewise
    def __str__(self):
        return '(If ' + str(self.condition) + ' ' + str(self.consequence) + ')'
    def __call__(self, env):
        if self.condition(env):
            self.consequence(env)
        else:
            self.elsewise(env)
class ForExpression(Expression):
    def __init__(self, range, each):
        self.range = range
        self.each = each
    def __str__(self):
        return '(For ' + str(self.range) + ' ' + str(self.each) + ')'
    def __call__(self, env):
        for i in range(self.range.args[0](env), self.range.args[1](env) + 1):
            env.update({"_index":i})
            self.each(env)
class WhileExpression(Expression):
    def __init__(self, condition, consequence):
        self.condition = condition
        self.consequence = consequence
    def __str__(self):
        return '(While ' + str(self.condition) + ' ' + str(self.consequence) + ')'
    def __call__(self, env):
        while self.condition(env):
            self.consequence(env)
        return None
class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        return self.body(Env(self.parms, args, self.env))
global_env = Env()
class Token:
    def __init__(self, value):
        self.type = TokenTypes[value] if value in TokenTypes.keys() else 'Value'
        try: self.value = int(value)
        except ValueError:
            try: self.value = float(value)
            except ValueError: self.value = str(value)
    def getType(self):
        return self.type
    def getValue(self):
        return self.value
    def __str__(self):
        return str(self.value)
class Lexer:
    def __init__(self, text):
       self.index = -1
       text = re.sub(r'#[^\n]+','', text)
       self.thingy = ['BEGIN'] + re.findall(r'#[^\n]+|\"[^\n]+\"|\'\'\'[^\0]+\'\'\'|\d+\.\d+|\+\=|\-\=|\*\=|\/\=|\%\=|\&\&|\|\|\>\>|\<\<|\=\=|\!\=|\<\=|\>\=|\+\+|\-\-|[^\n({}) ,!\-~+;:.]+|[\(\)\{\},!\-~+;.]', text)
       self.punctuators = {}
    def hasNext(self):
       return self.index < len(self.thingy)
    def next(self):
       self.index += 1
       return Token((self.thingy[self.index]) if self.index < len(self.thingy) else 'EOF ')
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.prefixParselets = {}
        self.infixParselets = {}
        self.read = []
    def register(self, token, parselet):
        if isinstance(parselet, PrefixParselet):
            self.prefixParselets.update({token:parselet})
        else:
            self.infixParselets.update({token:parselet})
    def ParseExpression(self, precedence=0):
        token = self.consume()
        prefix = self.prefixParselets[token.getType()]

        if (prefix == None):
            return SyntaxError(f"Could not parse \"{str(token)}\".")
        
        left = prefix.Parse(self, token)

        while (precedence < self.GetPrecedence()):
            token = self.consume()
            
            infix = self.infixParselets[token.getType()]
            left = infix.Parse(self, left, token)
        
        return left
    def match(self, expected):
        token = self.lookahead(0)
        if token.getType() != expected:
            return False
        self.consume()
        return True
    def consume(self, expected=None):
        token = self.lookahead(0)
        if token.getType() != expected and expected != None:
            raise SyntaxError(f"Expected token of type {expected} at \"{str(token)}\" but recieved token of type {token.getType()}")
        return self.read.pop(0)
    def lookahead(self, distance):
        while distance >= len(self.read):
            self.read.append(self.lexer.next())
        return self.read[distance]
    def GetPrecedence(self):
        parser = self.infixParselets[self.lookahead(0).getType()] if self.lookahead(0).getType() in self.infixParselets.keys() else None
        if parser != None:
            return parser.GetPrecedence()
        return 0
class BantamParser(Parser):
    def __init__(self, lexer):
        self.lexer = lexer
        self.prefixParselets = {}
        self.infixParselets = {}
        self.read = []

        self.register("Value", ValueParselet())
        self.register("QUESTION", ConditionalParselet())
        self.register("LEFT_PAREN", GroupParselet())
        self.register("LEFT_CURLY_PAREN", GroupParselet())
        self.register("LEFT_PAREN", CallParselet())
        self.register("BEGIN", ProgramParselet())
        self.register("IF", IfParselet())
        self.register("FOR", ForParselet())
        self.register("WHILE", WhileParselet())

        self.prefix("PLUS", Priority['PREFIX'], lambda env, _, x: [+x(env), env])
        self.prefix("MINUS", Priority['PREFIX'], lambda env, _, x: [-x(env), env])
        self.prefix("TILDE", Priority['PREFIX'], lambda env, _, x: [int(x(env)), env])
        self.prefix("BANG", Priority['PREFIX'], lambda env, _, x: [not x(env), env])
        self.prefix("INCREMENT", Priority['PREFIX'], lambda env, _, x: [x(env) + 1, env])
        self.prefix("DECREMENT", Priority['PREFIX'], lambda env, _, x: [x(env) - 1, env])

        self.postfix("BANG", Priority['POSTFIX'], lambda env, x, _: [(fact := fact * i for i in range(1, x(env)+1)), env])
        self.postfix("INCREMENT", Priority['POSTFIX'], lambda env, x, _: [x(env) + 1, env])
        self.postfix("DECREMENT", Priority['POSTFIX'], lambda env, x, _: [x(env) - 1, env])

        self.infixLeft("PLUS", Priority['SUM'], lambda env, x, _, y: [x(env) + y(env), env])
        self.infixLeft("MINUS", Priority['SUM'], lambda env, x, _, y: [x(env) - y(env), env])
        self.infixLeft("ASTERISK", Priority['PRODUCT'], lambda env, x, _, y: [x(env) * y(env), env])
        self.infixLeft("SLASH", Priority['PRODUCT'], lambda env, x, _, y: [x(env) / y(env), env])
        self.infixLeft("PRECENT", Priority['PRODUCT'], lambda env, x, _, y: [x(env) % y(env), env])
        self.infixLeft("PROCESSOR", Priority['EXECUTABLE'], lambda env, x, _ , y: [Procedure(list(i(env) for i in x.args), y, env), env])
        self.infixLeft("COMPARISON", Priority['COMPARISON'], lambda env, x, op, y: [x(env) == y(env) if str(op) == '==' else (x(env) != y(env) if str(op) == '!=' else (x(env) > y(env) if str(op) == '>' else (x(env) < y(env) if str(op) == '<' else (x(env) >= y(env) if str(op) == '>=' else (x(env) <= y(env) if str(op) == '<=' else None))))), env])
        self.infixLeft("LOGICAL", Priority['LOGICAL'], lambda env, x, op, y: [x(env) >> y(env) if str(op) == '>>' else (x(env) << y(env) if str(op) == '<<' else (x(env) and y(env) if str(op) == '&&' else (x(env) or y(env) if str(op) == '||' else (x(env) & y(env) if str(op) == '&' else None)))), env])

        self.infixRight("DoubleColon", Priority['INCONTEXT'], lambda env, x, _, y: [x(env).find(str(y))[str(y)], env])
        self.infixRight("ASSIGN", Priority['ASSIGNMENT'], lambda env, x, _, y: [None, env := (a if (a := env.find(str(x(env)))) != None else env).update({str(x):y(env)})])
        self.infixRight("CARET", Priority['EXPONENT'], lambda env, x, _, y: [x(env) ** y(env), env])
    def postfix(self, token, precedence, lambdafunc):
        self.register(token, PostfixOperatorParselet(precedence, lambdafunc))
    def prefix(self, token, precedence, lambdafunc):
        self.register(token, PrefixOperatorParselet(precedence, lambdafunc))
    def infixLeft(self, token, precedence, lambdafunc):
        self.register(token, BinaryOperatorParselet(precedence, False, lambdafunc))
    def infixRight(self, token, precedence, lambdafunc):
        self.register(token, BinaryOperatorParselet(precedence, True, lambdafunc))

Passed = 0
Failed = 0

def TestExpr(source, expected):
    global Failed
    global Passed
    lexer = Lexer(source)
    parser = BantamParser(lexer)

    try:
        result = str(parser.ParseExpression()).rstrip('\n')

        if expected == result:
            Passed += 1
            print(result)
        else:
            Failed += 1
            print("[FAIL] Expected: " + expected)
            print("         Actual: " + result)
    except(SyntaxError) as e:
        Failed += 1
        print("[FAIL] Expected: " + expected)
        print("          Error: " + str(e))

def UnitTests():
    # Function call.
    print("\nFunction calls:")
    TestExpr("a();", "a();")
    TestExpr("a(b);", "a(b);")
    TestExpr("a(b, c);", "a(b, c);")
    TestExpr("a(b)(c);", "a(b)(c);")
    TestExpr("a(b) + c(d);", "(a(b) + c(d));")
    TestExpr("a(b ? c : d, e + f);", "a((b ? c : d), (e + f));")
    print("")

    # Unary precedence.
    print("Unary precedence:")
    TestExpr("~!-+a;", "(~(!(-(+a))));")
    TestExpr("a!!!;", "(((a!)!)!);")
    print("")
    
    # Unary and binary predecence.
    print("Unary and binary precedence:")
    TestExpr("-a * b;", "((-a) * b);")
    TestExpr("!a + b;", "((!a) + b);")
    TestExpr("~a ^ b;", "((~a) ^ b);")
    TestExpr("-a!;",    "(-(a!));")
    TestExpr("!a!;",    "(!(a!));")
    print("")
    
    # Binary precedence.
    print("Binary precedence:")
    TestExpr("a = b + c * d ^ e - f / g;", "(a = ((b + (c * (d ^ e))) - (f / g)));")
    print("")
    
    # Binary associativity.
    print("Binary associativity:")
    TestExpr("a = b = c;", "(a = (b = c));")
    TestExpr("a + b - c;", "((a + b) - c);")
    TestExpr("a * b / c;", "((a * b) / c);")
    TestExpr("a ^ b ^ c;", "(a ^ (b ^ c));")
    print("")
    
    # Conditional operator.
    print("Conditional operator:")
    TestExpr("a ? b : c ? d : e;", "(a ? b : (c ? d : e));")
    TestExpr("a ? b ? c : d : e;", "(a ? (b ? c : d) : e);")
    TestExpr("a + b ? c * d : e / f;", "((a + b) ? (c * d) : (e / f));")
    print("")
    
    # Grouping.
    print("Grouping:")
    TestExpr("a + (b + c) + d;", "((a + ((b + c))) + d);")
    TestExpr("a ^ (b + c);", "(a ^ ((b + c)));")
    TestExpr("(!a)!;",    "(((!a))!);")
    print("")

    #value type coersion
    print("Value type coersion:")
    TestExpr("a(1);", "a(1);")
    TestExpr("a(1.0);", "a(1.0);")
    TestExpr("a(\"Me SMH\");", "a(Me SMH);")
    print("")

    if Failed == 0:
        print(f"Passed all {Passed} tests.")
    else:
        print("----")
        print(f"Failed {Failed} out of {Failed + Passed} tests.")

@app.command()
def test():
    UnitTests()

@app.command()
def run(filename: Path):
    BantamParser(Lexer(filename.open().read())).ParseExpression()(global_env)

@app.command()
def bruh():
    typer.echo("nah")
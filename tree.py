# tree4.py

"""
Parse trees for a C++-like language.
"""

def error(msg):
    raise RuntimeError(msg)

def prec(op):
    """Returns the precedence of op.
    """
    if op in '*/%':
        return 5
    elif op in '+-':
        return 6
    else:
        error('unknown opertor "%s"' % op)

##############################################################

class Node(object):
    pass

class Literal(Node):
    def __init__(self, val, kind):
        self.val = val
        self.kind = kind

    def __repr__(self):
        return 'Literal("%s", "%s")' % (self.val, self.kind)

class Var(Node):
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    def __repr__(self):
        return 'Var("%s", "%s")' % (self.name, self.kind)

class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'BinOp("%s", %s, %s)' % (self.op, self.left, self.right)

class VarOp(Node): pass

class PreInc(VarOp):
    def __init__(self, vble):
        self.vble = vble

    def __repr__(self):
        return 'PreInc(%s)' % (self.vble)

class PostInc(VarOp):
    def __init__(self, vble):
        self.vble = vble

    def __repr__(self):
        return 'PostInc(%s)' % (self.vble)

class PreDec(VarOp):
    def __init__(self, vble):
        self.vble = vble

    def __repr__(self):
        return 'PreDec(%s)' % (self.vble)

class PostDec(VarOp):
    def __init__(self, vble):
        self.vble = vble

    def __repr__(self):
        return 'PostDec(%s)' % (self.vble)

class DefineVar(Node):
    def __init__(self, vble, init_expr):
        self.vble = vble
        self.init_expr = init_expr

    def __repr__(self):
        return 'DefineVar(%s, %s)' % (self.vble, self.init_expr)

class Assign(Node):
    def __init__(self, op, lhs_vble, rhs_expr):
        self.op = op
        self.vble = lhs_vble
        self.expr = rhs_expr

    def __repr__(self):
        return 'Assign("%s", %s, %s)' % (self.op, self.lhs_vble, self.rhs_expr) 

class Seq(Node):
    def __init__(self, *kids):
        self.kids = kids
        self.comment = ''

    def __repr__(self):
        return 'Seq(%s)' % (', '.join(str (k) for k in self.kids))

class Loop(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def __repr__(self):
        return 'Loop(%s, %s)' % (self.cond, self.body)   

class Print(Node):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return 'Print(%s)' % (self.expr)  

######################################################################

def eval_expr(e, env={}):
    if e == None:
        return None
    elif isinstance(e, Literal):
        return e.val
    elif isinstance(e, Var):
        return env[e.name]
    elif isinstance(e, BinOp):
        left, right = eval_expr(e.left, env), eval_expr(e.right, env)
        return eval('%s %s %s' % (left, e.op, right)) # hack!
    else:
        error('unknown eval expression e=%s' % e)

# Returns a list of the names of all the variables in expression e. Duplicate
# names are preserved, e.g. the expression i + i returns ['i', 'i'].
# def get_vars(e):
#     if e == None:
#         return None
#     elif isinstance(e, Literal):
#         return []
#     elif isinstance(e, Var):
#         return [e.name]
#     elif isinstance(e, BinOp):
#         return get_vars(e.left) + get_vars(e.right)
#     elif isinstance(e, VarOp):
#         return [e.vble.name]
#     elif isinstance(e, DefineVar):
#         return [e.vble.name] + get_vars(e.init_expr)
#     elif isinstance(e, Assign):
#         return get_vars(e.lhs_vble) + get_vars(e.rhs_expr)
#     elif isinstance(e, Seq):
#         result = []
#         for s in e.kids:
#             result.extend(get_vars(s))
#         return result
#     else:
#         error('unknown expression e=%s' % e)

def infix_str(e):
    if e == None:
        pass
    elif isinstance(e, Literal):
        return str(e.val)
    elif isinstance(e, Var):
        return str(e.name)
    elif isinstance(e, BinOp):
        result = ''
        if isinstance(e.left, BinOp) and prec(e.op) < prec(e.left.op):
            result += '(%s)' % infix_str(e.left)
        else:
            result += infix_str(e.left)
        result += ' %s ' % str(e.op)
        if isinstance(e.right, BinOp) and prec(e.op) < prec(e.right.op):
            result += '(%s)' % infix_str(e.right)
        else:
            result += infix_str(e.right)
        return result
    elif isinstance(e, PreInc):
        return '++%s;' % e.vble.name
    elif isinstance(e, PostInc):
        return '%s++;' % e.vble.name
    elif isinstance(e, PreDec):
        return '--%s;' % e.vble.name
    elif isinstance(e, PostDec):
        return '%s--;' % e.vble.name
    elif isinstance(e, DefineVar):
        return '%s %s = %s;' % (e.vble.kind, e.vble.name, infix_str(e.init_expr))
    elif isinstance(e, Assign):
        return '%s %s %s;' % (e.vble.name, e.op, infix_str(e.expr))
    elif isinstance(e, Seq):
        result = [infix_str(s) for s in e.kids]
        if e.comment != '':
            result.insert(0, '// %s' % e.comment)
        return '\n'.join(result)
    elif isinstance(e, Loop):
        return 'while (%s) {\n%s\n}\n' % (infix_str(e.cond), infix_str(e.body))
    elif isinstance(e, Print):
        return 'print(%s);' % infix_str(e.expr)
    else:
        error('unknown infix_str expression e=%s' % e)

######################################################################

def test2():
    a = DefineVar(Var('a', 'int'), Literal('2', 'int'))
    print a
    print infix_str(a)
    # print get_vars(a)
    b = DefineVar(Var('b', 'int'), Literal('2', 'int'))
    print b
    print infix_str(b)
    print get_vars(b)
    i1 = PreInc(Var('a', 'int'))
    d1 = PostDec(Var('b', 'int'))
    frag = Seq(a, b, i1, d1)
    frag.comment = 'a fragment of code'
    print frag
    print infix_str(frag)
    # print get_vars(frag)

def test3():
    ivar = Var('i', 'int')
    init = DefineVar(ivar, Literal('1', 'int'))
    cond = BinOp('<', ivar, Literal('5', 'int'))
    incr = PostInc(ivar)
    body = Seq(Print(BinOp('*', ivar, ivar)), incr)
    loop = Loop(cond, body)
    prog = Seq(init, loop)
    print prog
    print infix_str(prog)
    ivar.name = 'j'
    print prog
    print infix_str(prog)

    test = Seq(DefineVar(Var("i", "int"), Literal("1", "int")), Loop(BinOp("<", Var("i", "int"), Literal("5", "int")), Seq(Print(BinOp("*", Var("i", "int"), Var("i", "int"))), PostInc(Var("i", "int")))))
    print test
    print infix_str(test)   

if __name__ == '__main__':
    test3()

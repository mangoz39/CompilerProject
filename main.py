# -----------------------------------------------------------------------------
#
# Grammar:
#
#   PROGRAM    : STMT
#
#   STMT       : EXP
#              | DEF
#              | PRINT
#
#   PRINT      : PRINT_NUM EXP
#              | PRINT_BOOL EXP
#
#   EXP        : bool_val
#              | number
#              | var
#              | num_op
#              | logic_op
#              | fun_exp
#              | fun_call
#              | if_exp
#
#   num_op     : PLUS
#              | MINUS
#              | MULTIPLY
#              | DIVIDE
#              | MODULUS
#              | GREATER
#              | SMALLER
#              | EQUAL
#
#   logic_op   : AND_OP
#              | OR_OP
#              | NOT_OP
#
#   DEF_STMT   : (define VARIABLE EXP)
#
#
# -----------------------------------------------------------------------------

from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

# All tokens must be named in advance.
tokens = ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULUS', 'GREATER', 'SMALLER', 'EQUAL',
          'PRINT_NUM', 'PRINT_BOOL', 'NUMBER', 'LPR', 'RPR', 'BOOL', 'AND', 'OR', 'NOT', 'IF',
          'DEF', 'FUNC', 'ID')

var = {}


class Function:
    def __init__(self, o, v: list):
        self.op = o
        self.var = v


# Ignored characters
t_ignore = ' \t\n'

# Token matching rules are written as regexs

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_GREATER = r'\>'
t_SMALLER = r'\<'
t_EQUAL = r'\='
t_LPR = r'\('
t_RPR = r'\)'
t_BOOL = r'\#t|\#f'

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.


def t_MODULUS(t):
    r'mod'
    return t


def t_PRINT_NUM(t):
    r'print-num'
    return t


def t_PRINT_BOOL(t):
    r'print-bool'
    return t


def t_IF(t):
    r'if'
    return t


def t_FUNC(t):
    r'fun'
    return t


def t_DEF(t):
    r'define'
    return t


def t_AND(t):
    r'and'
    return t


def t_OR(t):
    r'or'
    return t


def t_NOT(t):
    r'not'
    return t


def t_NUMBER(t):
    r'[-]*\d+'
    t.value = int(t.value)
    return t


"""
# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n'
    t.lexer.lineno += t.value.count('\n')
"""


# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)


def t_ID(t):
    r'[a-zA-Z]+'
    return t


# Build the lexer object
lexer = lex()

# --- Parser ---


def p_program(p):
    '''
    PROGRAM : STMTS
    '''


def p_stmts(p):
    '''
    STMTS : STMTS STMT
    '''


def p_stmts_stmt(p):
    '''
    STMTS : STMT
    '''


def p_stmt(p):
    '''
    STMT : EXP
         | LPR PRINT_STMT RPR
         | LPR DEF_STMT RPR
    '''


def p_print(p):
    '''
    PRINT_STMT : PRINT_NUM EXP
               | PRINT_BOOL EXP
    '''
    if p[2][0] == 'number':
        res = str(p[2][1])
        for x in str(p[2][1]):
            if x in var:
                res = res.replace(x, str(var[x]))
        print(eval(res))
    elif p[2][0] == 'var':
        if str(p[2][1]) in var:
            print(eval(str(var[str(p[2][1])])))
    else:
        print(p[2][1])


def p_exp_num(p):
    '''
    EXP : NUMBER
    '''
    p[0] = ('number', p[1])


def p_exp_bool(p):
    '''
    EXP : BOOL
    '''
    p[0] = ('bool', p[1])


def p_exp_var(p):
    '''
    EXP : VAR
    '''
    p[0] = ('var', str(p[1]))
    # print(f'Variable {p[1]} isn\'t defined')


def p_exp_exp(p):
    '''
    EXP : LPR NUM_OP RPR
        | LPR LOGICAL_OP RPR
        | LPR IF_EXP RPR
        | LPR FUN_CALL RPR
    '''
    p[0] = p[2]


def p_log_and(p):
    '''
    LOGICAL_OP : AND EXPS
    '''
    flag = True
    for e in p[2]:
        if e[1] == '#t':
            tar = True
        else:
            tar = False
        flag = flag and tar
    if flag:
        flag = '#t'
    else:
        flag = '#f'
    p[0] = ('bool', flag)


def p_log_or(p):
    '''
    LOGICAL_OP : OR EXPS
    '''
    flag = False
    for e in p[2]:
        if e[1] == '#t':
            tar = True
        else:
            tar = False
        flag = flag or tar
    if flag:
        flag = '#t'
    else:
        flag = '#f'
    p[0] = ('bool', flag)


def p_log_not(p):
    '''
    LOGICAL_OP : NOT EXP
    '''
    if p[2][0] == 'bool':
        if p[2][1] == '#t':
            flag = '#f'
        else:
            flag = '#t'
        p[0] = ('bool', flag)
    else:
        print(f'Type Error: Expect \'boolean\' but \'number\'')
        return 0


def p_exps(p):
    '''
    EXPS : EXPS EXP
    '''
    p[1].append(p[2])
    p[0] = p[1]


def p_exps_exp(p):
    '''
    EXPS : EXP
    '''
    p[0] = [p[1]]


def p_num_plus(p):
    '''
    NUM_OP : PLUS EXPS
    '''
    p_sum = ""
    for e in p[2]:
        p_sum += str(e[1])
        p_sum += ' + '
    p[0] = ('number', p_sum[:-3])


def p_num_minus(p):
    '''
    NUM_OP : MINUS EXP EXP
    '''
    p_res = str(p[2][1]) + ' - '
    p_res += str(p[3][1])
    p[0] = ('number', p_res)


def p_num_multiply(p):
    '''
    NUM_OP : MULTIPLY EXPS
    '''
    p_sum = ""
    for e in p[2]:
        p_sum += str(e[1])
        p_sum += ' * '
    p[0] = ('number', p_sum[:-3])


def p_num_divide(p):
    '''
    NUM_OP : DIVIDE EXP EXP
    '''
    p_res = '(' + str(p[2][1]) + ') // ('
    p_res += str(p[3][1])
    p_res += ')'
    p[0] = ('number', p_res)


def p_num_modulus(p):
    '''
    NUM_OP : MODULUS EXP EXP
    '''
    p_res = '(' + str(p[2][1]) + ') % ('
    p_res += str(p[3][1])
    p_res += ')'
    p[0] = ('number', p_res)


def p_num_greater(p):
    '''
    NUM_OP : GREATER EXP EXP
    '''
    if eval(str(p[2][1])) > eval(str(p[3][1])):
        p[0] = ('bool', '#t')
    else:
        p[0] = ('bool', '#f')


def p_num_smaller(p):
    '''
    NUM_OP : SMALLER EXP EXP
    '''
    if eval(str(p[2][1])) < eval(str(p[3][1])):
        p[0] = ('bool', '#t')
    else:
        p[0] = ('bool', '#f')


def p_num_equal(p):
    '''
    NUM_OP : EQUAL EXP EXP
    '''
    if eval(str(p[2][1])) == eval(str(p[3][1])):
        p[0] = ('bool', '#t')
    else:
        p[0] = ('bool', '#f')


def p_if_stmt(p):
    '''
    IF_EXP : IF EXP EXP EXP
    '''
    if p[2][1] == '#t':
        flag = True
    elif p[2][1] == '#f':
        flag = False
    else:
        print(f'Type Error: Expect \'boolean\' but \'number\'')
        return 0

    if flag:
        p[0] = p[3]
    else:
        p[0] = p[4]


def p_def_stmt(p):
    '''
    DEF_STMT : DEF VAR EXP
    '''
    p[0] = ('number', p[3][1], str(p[1]))
    var[str(p[2])] = p[3][1]


def p_def_var(p):
    '''
    VAR : ID
    '''
    p[0] = p[1]


def p_fun_op_var_num(p):
    '''
    FUN_OP : EXPS
    '''
    p[0] = p[1][0][1]
    # print(p[0].var)


def p_fun_id(p):
    '''
    FUN_ID : LPR EXPS RPR
    '''
    p[0] = p[2]


def p_fun_exp(p):
    '''
    FUN_EXP : LPR FUNC FUN_ID FUN_OP RPR
    '''
    p[0] = (p[3], p[4])


def p_fun_call(p):
    '''
    FUN_CALL : FUN_EXP EXPS
    '''
    vars = {}
    for x, v in enumerate(p[1][0]):
        vars[v[1]] = str(p[2][x][1])
    res = p[1][1]
    voc = ""
    for x in p[1][1]:
        if x == ' ' or x == '(' or x == ')':
            if voc in vars:
                res = res.replace(voc, vars[voc])
            voc = ""
        else:
            voc += x
    if voc in vars:
        res = res.replace(voc, str(vars[voc]))
    p[0] = ('number', res)


def p_error(p):
    print(f'Syntax error at {p.value!r}')


# Build the parser
parser = yacc()

"""
# Parse an expression
file = open('./public_test_data/07_1.lsp')
file_line = file.readlines()
for j in file_line:
    ast = parser.parse(j)
file.close()
"""
#
# with open("./hidden_data/04_1_hidden.lsp", "r") as fp:
#     content = fp.read()
#     ast = parser.parse(content)
# parser.parse(input())

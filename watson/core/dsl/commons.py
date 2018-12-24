from core.dsl import types

from pyparsing import Literal
from pyparsing import alphanums
from pyparsing import OneOrMore
from pyparsing import nums
from pyparsing import Forward
from pyparsing import LineEnd
from pyparsing import QuotedString
from pyparsing import Word
from pyparsing import Optional
from pyparsing import Combine
from pyparsing import StringStart
from pyparsing import StringEnd
from pyparsing import ParseException as PyParsingParseException
# from pyparsing import ZeroOrMore
# from pyparsing import White
# from pyparsing import printables
# from pyparsing import alphas
# from pyparsing import ParseException
# from pyparsing import CaselessLiteral
# from pyparsing import Combine
# from pyparsing import Or
# from pyparsing import ZeroOrMore
# from pyparsing import FollowedBy
# from pyparsing import quotedString
# from pyparsing import alphanums

from core.dsl.exceptions import SyntaxException

expr = Forward()

##########
# Number #
##########


def number_parse_action(instring, tokensStart, retTokens):
    parsed_values = retTokens[0]
    return types.Number(parsed_values[0])


number = Combine(Word(nums) + Optional(Literal('.') + Word(nums)))

number.addParseAction(number_parse_action)

##########
# String #
##########

single_quote_string = QuotedString('\'', escChar='\\')
double_quote_string = QuotedString('"', escChar='\\')


def string_parse_action(instring, tokensStart, retTokens):
    parsed_values = retTokens[0]
    return types.String(parsed_values[0])


string = single_quote_string | double_quote_string
string.addParseAction(string_parse_action)

############
# Function #
############

LPAR = Literal('(').suppress()
RPAR = Literal(')').suppress()
name = Word(alphanums)

args = expr + Optional(Literal(',').suppress() + expr)
function = name + LPAR + Optional(args) + RPAR


def function_parse_action(instring, tokensStart, retTokens):
    return types.Function(name=retTokens[0], args=retTokens[1:])


function.addParseAction(function_parse_action)


#########
# Block #
#########

def block_parse_action(instring, tokensStart, retTokens):
    return types.Block(list(retTokens))


block = OneOrMore(expr + (LineEnd() | Literal(';')).suppress())

block.addParseAction(block_parse_action)

expr << (string | number | function)

script = StringStart() + block + StringEnd()


def decode(s: str):
    try:
        result = script.parseString(s)
    except PyParsingParseException as e:
        raise SyntaxException(
            'Syntax Error at line {} ({}): {}'.format(
                e.lineno,
                e.markInputline(),
                e.args[2],
            ),
        )

    if len(result) > 1:
        raise SyntaxException('Main block needs to have only one code block.')
    elif len(result) == 0:
        raise SyntaxException('Main block cannot be empty.')
    else:
        return result[0]

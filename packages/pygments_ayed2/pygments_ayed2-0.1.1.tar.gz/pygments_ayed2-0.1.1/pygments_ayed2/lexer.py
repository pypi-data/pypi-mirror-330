from pygments.lexer import RegexLexer
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation


class Ayed2Lexer(RegexLexer):
    name = 'AyED2'
    aliases = ['ayed2', 'ayed']
    filenames = ['*.ayed2', '*.ayed']
    tokens = {
        'root': [
            (r'\s+', Text),  # whitespace
            (r'//.*?$', Comment),  # single line comment
            (r'type|enumerate|tuple|end', Keyword.Type.Definition),  # types declarations
            (r'int|char|bool|real|array|pointer|of', Keyword.Type),  # types
            (r':=|=', Punctuation.Assignment),  # assignments (for vars, and for types)
            (r'var|:', Keyword.Declaration),  # keyword
            (r'\b[A-Z].*?\b', Keyword.Type.Enum),  # enums constants
            (r'if|then|else|fi|while|do|od|for|to|downto', Keyword),  # control flow keywords
            (r'alloc|free', Name.Builtin),  # built-in functions
            (r'getenv', Name.Builtin),      # another built-in
            (r'->|\.', Punctuation),  # Field access
            (r'==|!=|<|<=|>|>=', Operator),  # comparison operators
            (r'\+\+|--|\+|-|\*|/|%|!', Operator),  # arithmetic operators
            (r'\&\&|\|\|', Operator),  # logical operators
            (r'null|true|false|inf', Name.NamedLiteral),  # literals
            (r'\'.\'', String.Char),  # Char literals
            (r'\".*\"', String.String),  # Long string literals
            (r'\d+\.\d+', Number.Float),  # floating point
            (r'\d+', Number.Integer),  # integers
            (r'\w+', Name),  # identifiers
            (r'\(|\)', Punctuation),  # parentheses
            (r'\[|\]', Punctuation),  # brackets
            (r';', Punctuation),  # statement terminator
        ],
    }

class DSLException(Exception):
    pass


class SyntaxException(DSLException):
    pass


class SemanticException(DSLException):
    pass

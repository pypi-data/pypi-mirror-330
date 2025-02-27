"""
exceptions.py – Scenario instance parser specific exceptions
"""

# Every error should have the same format
# with a standard prefix and postfix defined here
pre = "\nScenario instance parser: ["
post = "]"


class SIParserException(Exception):
    pass

class SIParserIOException(SIParserException):
    pass

class SIParserDBException(SIParserException):
    pass


class SIParserUserInputException(SIParserException):
    pass

class SIParseError(SIParserUserInputException):
    def __init__(self, scenario_file, e):
        self.scenario_file = scenario_file
        self.e = e

    def __str__(self):
        return f'{pre}Parse error in scenario "{self.scenario_file}"\n\t{self.e}"{post}'

class SIInputFileOpen(SIParserIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}Parser cannot open this scenario instance file: "{self.path}"{post}'

class SIInputFileEmpty(SIParserIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}For some reason, nothing was read from the scenario input file: "{self.path}"{post}'

class SIGrammarFileOpen(SIParserIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}Parser cannot open this scenario grammar file: "{self.path}"{post}'
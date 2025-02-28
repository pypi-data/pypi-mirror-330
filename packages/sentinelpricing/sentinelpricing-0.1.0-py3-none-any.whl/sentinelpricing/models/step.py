class Step:
    """Step

    Form part of a quote Breakdown. Represents an operation carried out on a
    quote.
    """

    def __init__(self, name, oper, other, result):

        self.name = name
        self.oper = oper
        self.other = other
        self.result = result

    def __repr__(self):
        return f"{self.result: <7} :: {self.name:<30}"
        f" - {repr(self.oper): <30} - {self.other}"

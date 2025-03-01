# Adapted from: https://github.com/henrikmelin/spacecraft_rs
from collections import OrderedDict

from ply import lex, yacc


def read_label(filename, debug=False):
    """Read in a PDS3 label.

    Parameters
    ----------
    filename : string
      The name of the file to read.

    Returns
    -------
    label : dict
      The label as a `dict`.

    Raises
    ------
    IllegalCharacter

    Notes
    -----
    Objects and groups are returned as dictionaries containing all
    their sub-keywords.  Multiple objects (e.g., columns) with the
    same name are returned as a `list` of objects.

    """

    raw_label = ""
    with open(filename, "rb") as inf:
        while True:
            line = inf.readline()
            raw_label += line.decode("ascii")
            if line.strip() == b"END" or line == "":
                break

    parser = PDS3Parser(debug=debug)
    records = parser.parse(raw_label)
    return _records2dict(records)


def _records2dict(records, object_index=0):
    """Convert a list of PDS3 records to a dictionary.

    Parameters
    ----------
    records : list
      List of key-item pairs.
    object_index : int, optional
      Extract just a single object or group, starting at the index
      `object_index`.

    Returns
    -------
    d : dict
      The dictionary.
    last_index : int, optional
      When extracting a single object or group, also return the last
      index of that object.

    """

    label = OrderedDict()
    start = 0
    if object_index != 0:
        start = object_index
        object_name = records[start][1]
        start += 1
    else:
        object_name = None

    i = start
    while i < len(records):
        # groups and objects are both terminated with 'END_...'
        if records[i] == ("END_OBJECT", object_name) or records[i] == (
            "END_GROUP",
            object_name,
        ):
            return label, i
        elif records[i][0] in ["OBJECT", "GROUP"]:
            key = PDS3Keyword(records[i][1])
            value, j = _records2dict(records, i)
            if records[i][0] == "OBJECT":
                value = PDS3Object(value)
            elif records[i][0] == "GROUP":
                value = PDS3Group(value)
            i = j
        else:
            key = records[i][0]
            value = records[i][1]

        if key in label:
            if not isinstance(label[key], list):
                label[key] = [label[key]]
            label[key].append(value)
        else:
            label[key] = value
        i += 1

    return label


class IllegalCharacter(Exception):
    pass


class PDS3Keyword(str):
    """PDS3 keyword.

    In the following, the keyword is "IMAGE":

      OBJECT = IMAGE
        ...
      END_OBJECT = IMAGE

    """

    def __new__(cls, value):
        return str.__new__(cls, value)


class PDS3Object(OrderedDict):
    """PDS3 data object definition.

    OBJECT = IMAGE
      ...
    END_OBJECT = IMAGE

    """

    pass


class PDS3Group(OrderedDict):
    """PDS3 group statement.

    GROUP = SHUTTER_TIMES
      ...
    END_GROUP = SHUTTER_TIMES

    """

    pass


class PDS3Parser:
    tokens = [
        "KEYWORD",
        "POINTER",
        "STRING",
        "INT",
        "REAL",
        "UNIT",
        "DATE",
        "END",
    ]

    literals = list("=(){},")

    t_POINTER = r"\^[A-Z0-9_]+"
    t_ignore_COMMENT = r"/\*.+?\*/"
    t_ignore = " \t\r\n"

    # lower case PDS3 to astropy unit translation
    unit_translate = dict(v="V", k="K")

    def __init__(self, debug=False):
        self.debug = debug
        self.lexer = lex.lex(module=self, debug=self.debug)
        self.parser = yacc.yacc(module=self, debug=self.debug, write_tables=0)

    def parse(self, raw_label, **kwargs):
        return self.parser.parse(
            raw_label, lexer=self.lexer, debug=self.debug, **kwargs
        )

    def t_KEYWORD(self, t):
        r"[A-Z][A-Z0-9_:]+"
        if t.value == "END":
            t.type = "END"
        return t

    def t_DATE(self, t):
        r"\d\d\d\d-\d\d-\d\d(T\d\d:\d\d(:\d\d(.\d+)?)?)?Z?"
        from astropy.time import Time

        t.value = Time(t.value, scale="utc")
        return t

    def t_UNIT(self, t):
        r"<[\w*^\-/]+>"
        import astropy.units as u

        # most astropy units are lower-case versions of the PDS3 units
        unit = t.value[1:-1].lower()

        # but not all
        if unit in self.unit_translate:
            unit = self.unit_translate[unit]

        t.value = u.Unit(unit)
        return t

    def t_STRING(self, t):
        r'"[^"]+"'
        t.value = t.value[1:-1].replace("\r", "")
        return t

    def t_REAL(self, t):
        r"[+-]?(([0-9]+\.[0-9]*)|(\.[0-9]+))([Ee][+-]?[0-9]+)?"
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r"[+-]?[0-9]+"
        t.value = int(t.value)
        return t

    def t_error(self, t):
        raise IllegalCharacter(t.value[0])

    def lexer_test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

    def p_label(self, p):
        """label : record
        | label record
        | label END"""
        if len(p) == 2:
            # record
            p[0] = [p[1]]
        elif p[2] == "END":
            # label END
            p[0] = p[1]
        else:
            # label record
            p[0] = p[1] + [p[2]]

    def p_record(self, p):
        """record : KEYWORD '=' value
        | POINTER '=' INT
        | POINTER '=' STRING
        | POINTER '=' '(' STRING ',' INT ')'"""
        if len(p) == 4:
            p[0] = (p[1], p[3])
        else:
            p[0] = (p[1], (p[4], p[6]))

    def p_value(self, p):
        """value : STRING
        | DATE
        | KEYWORD
        | number
        | pds_set
        | quantity
        | sequence"""
        p[0] = p[1]

    def p_value_quantity(self, p):
        """quantity : number UNIT"""
        p[0] = p[1] * p[2]

    def p_number(self, p):
        """number : INT
        | REAL"""
        p[0] = p[1]

    def p_pds_set(self, p):
        """pds_set : '{' value '}'
        | '{' sequence_values '}'"""
        p[0] = set(p[2])

    def p_sequence(self, p):
        """sequence : '(' value ')'
        | '(' sequence_values ')'
        | '{' value '}'
        | '{' sequence_values '}'"""
        p[0] = p[2]

    def p_sequence_values(self, p):
        """sequence_values : value ','
        | sequence_values value ','
        | sequence_values value"""
        if p[2] == ",":
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

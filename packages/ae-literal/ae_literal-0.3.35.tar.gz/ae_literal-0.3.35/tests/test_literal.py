""" literal unit tests """
import datetime
import pytest

from ae.base import DATE_TIME_ISO, DATE_ISO, DEF_ENCODE_ERRORS
from ae.parse_date import parse_date
from ae.literal import Literal


class TestLiteral:
    def test_init(self):
        lit = Literal()
        assert lit.value is None
        assert lit._literal_or_value is None
        assert lit._type is None

        st = 'test_val'
        lit = Literal(literal_or_value=st)
        assert isinstance(lit.value, str)
        assert lit.value == st

        fv = 369
        fn = 'float literal'
        lit = Literal(str(fv), value_type=float, name=fn)
        assert lit._literal_or_value == str(fv)
        assert lit._type == float
        assert lit._name == fn
        assert isinstance(lit.value, float)
        assert lit.value == float(fv)
        assert lit.value == fv

    def test_bool_values(self):
        bs = 'True'
        lit = Literal(literal_or_value=bs)
        assert isinstance(lit.value, bool)
        assert lit.value is True

        lit.value = bs
        assert lit.value is True

        bs = 'False'
        lit = Literal(literal_or_value=bs)
        assert isinstance(lit.value, bool)
        assert lit.value is False

        lit.value = bs
        assert lit.value is False

        bs = 'True'
        lit = Literal(literal_or_value=bs, value_type=bool)
        assert isinstance(lit.value, bool)
        assert lit.value is True

        lit.value = bs
        assert lit.value is True

        bs = 'False'
        lit = Literal(literal_or_value=bs, value_type=bool)
        assert isinstance(lit.value, bool)
        assert lit.value is False

        lit.value = bs
        assert lit.value is False

        bn = 1
        lit = Literal(literal_or_value=bn, value_type=bool)
        assert isinstance(lit.value, bool)
        assert lit.value is True

        lit.value = bn
        assert lit.value is True

        bn = 0
        lit = Literal(literal_or_value=bn, value_type=bool)
        assert isinstance(lit.value, bool)
        assert lit.value is False

        lit.value = bn
        assert lit.value is False

        bn = '1+0'
        lit = Literal(literal_or_value=bn, value_type=bool)
        assert isinstance(lit.value, bool)
        assert lit.value is True

        lit.value = bn
        assert lit.value is True

        bn = "1-1"
        lit = Literal(literal_or_value=bn, value_type=bool)
        assert isinstance(lit.value, bool)
        assert lit.value is False

        lit.value = bn
        assert lit.value is False

    def test_bytes_values(self):
        bs = b'TEST'
        lit = Literal(literal_or_value=bs, value_type=bytes)
        assert isinstance(lit.value, bytes)
        assert lit.value == bs

        lit.value = bs
        assert lit.value is bs

        lit = Literal(literal_or_value=bs)
        assert isinstance(lit.value, str)
        assert lit.value == 'TEST'

        lit.value = bs
        assert lit.value == 'TEST'

        ds = b'2020-12-24'
        ss = ds.decode(errors=DEF_ENCODE_ERRORS)    # default encoding='utf-8'
        lit = Literal(literal_or_value=ds, value_type=datetime.date)
        assert isinstance(lit.value, datetime.date)
        assert lit.value == datetime.datetime.strptime(ss, DATE_ISO).date()
        assert lit.value == parse_date(ss, ret_date=True)

        lit.value = ds
        assert lit.value == datetime.datetime.strptime(ss, DATE_ISO).date()

        lit = Literal(literal_or_value=bs, value_type=str)
        assert isinstance(lit.value, str) and not isinstance(lit.value, bytes)
        assert lit.value == 'TEST'

        lit.value = bs
        assert lit.value == 'TEST'

    def test_date_values(self):
        ds = '2020-12-24'
        lit = Literal(literal_or_value=ds, value_type=datetime.date)
        assert isinstance(lit.value, datetime.date)
        assert lit.value == datetime.datetime.strptime(ds, DATE_ISO).date()
        assert lit.value == parse_date(ds, ret_date=True)

        lit.value = ds
        assert lit.value == datetime.datetime.strptime(ds, DATE_ISO).date()

        dts = datetime.datetime.now().strftime(DATE_TIME_ISO)
        lit = Literal(literal_or_value=dts, value_type=datetime.datetime)
        assert isinstance(lit.value, datetime.datetime)
        assert lit.value == datetime.datetime.strptime(dts, DATE_TIME_ISO)
        assert lit.value == parse_date(dts)

        lit.value = dts
        assert lit.value == datetime.datetime.strptime(dts, DATE_TIME_ISO)

    def test_date_expression(self):
        ex = "datetime.date.today()"
        lit = Literal('(' + ex + ')')
        assert isinstance(lit.value, datetime.date)
        assert lit.value == eval(ex)

        lit.value = '(' + ex + ')'
        assert lit.value == eval(ex)

    def test_float_values(self):
        fv = "3.69"
        lit = Literal(fv)
        assert isinstance(lit.value, float)
        assert lit.value == eval(fv)

        lit.value = fv
        assert lit.value == eval(fv)

    def test_int_values(self):
        iv = '369'
        lit = Literal(iv)
        assert isinstance(lit.value, int)
        assert lit.value == eval(iv)

        lit.value = iv
        assert lit.value == eval(iv)

    def test_tuple_values(self):
        tu = (1, 2, 3)
        lit = Literal(repr(tu))
        assert isinstance(lit.value, tuple)
        assert lit.value == tu

        lit.value = repr(tu)
        assert lit.value == tu

    def test_str_values(self):
        st = "tst_str"

        lit = Literal()
        assert lit.value is None
        lit.value = st
        assert lit.value == st

        lit = Literal()
        assert lit.value is None
        lit.value = repr(st)
        assert lit.value == st

        lit = Literal()
        assert lit.value is None
        lit.value = '"' + st + '"'
        assert lit.value == st

        lit = Literal()
        assert lit.value is None
        lit.value = "'" + st + "'"
        assert lit.value == st


    def test_str_values_err(self):
        st = "tst_str"

        lit = Literal()
        assert lit.value is None
        lit.value = "'''" + st + "'''"
        with pytest.raises(ValueError):
            _check = lit.value

        lit = Literal()
        assert lit.value is None
        lit.value = '"""' + st + '"""'
        with pytest.raises(ValueError):
            _check = lit.value

    def test_str_values_with_default(self):
        st = "tst_str"

        lit = Literal(st)
        assert isinstance(lit.value, str)
        assert lit.value == st

        lit = Literal(repr(st))
        assert isinstance(lit.value, str)
        assert lit.value == st

        lit.value = repr(st)
        assert lit.value == st

        lit = Literal('"' + st + '"')
        assert isinstance(lit.value, str)
        assert lit.value == st

        lit.value = '"' + st + '"'
        assert lit.value == st

        lit = Literal("'" + st + "'")
        assert isinstance(lit.value, str)
        assert lit.value == st

        lit.value = "'" + st + "'"
        assert lit.value == st

    def test_str_values_with_type(self):
        st = "tst_str"

        lit = Literal(st, value_type=str)
        assert isinstance(lit.value, str)
        assert lit.value == st

        lit.value = st
        assert lit.value == st

        lit = Literal(repr(st), value_type=str)
        assert isinstance(lit.value, str)
        assert lit.value == st

        lit.value = repr(st)
        assert lit.value == st

        lit = Literal('"' + st + '"', value_type=str)
        assert isinstance(lit.value, str)
        assert lit.value == st

        lit.value = '"' + st + '"'
        assert lit.value == st

        lit = Literal("'" + st + "'", value_type=str)
        assert isinstance(lit.value, str)
        assert lit.value == st

        lit.value = "'" + st + "'"
        assert lit.value == st

    def test_dict_values(self):
        di = dict(a=1, b=2)
        lit = Literal(repr(di))
        assert isinstance(lit.value, dict)
        assert lit.value == di

        lit.value = repr(di)
        assert lit.value == di

    def test_list_values(self):
        li = list([1, "b", datetime.date.today()])
        lit = Literal(repr(li))
        assert isinstance(lit.value, list)
        assert lit.value == li

        lit.value = repr(li)
        assert lit.value == li

    def test_code_block(self):
        # also test if datetime and all core constants and helper functions are available in code block literals
        cb = '"""cb_var = 1.0; _imported = datetime.datetime.now().strftime(DATE_ISO); ' \
             'from ae.base import round_traditional; round_traditional(cb_var) """'
        lit = Literal(cb)
        assert isinstance(lit.value, float)
        assert lit.value == 1.0

        lit.value = cb
        assert lit.value == 1.0

        cb = "'''import math; math.cos(math.pi) '''"
        lit = Literal(cb)
        assert isinstance(lit.value, float)
        assert lit.value == -1.0

        lit.value = cb
        assert lit.value == -1.0

    def test_append_value(self):
        li = list((3, 6, 9, ))
        lit = Literal(li)
        lit.append_value(12)
        assert isinstance(lit.value, list)
        assert len(lit.value) == 4
        assert lit.value[-1] == 12

    def test_convert_value(self):
        st = "test_str"
        lit = Literal()
        assert lit.convert_value(st) == st
        assert lit.value == st

        di = dict(a=1, b=3)
        lit = Literal()
        assert lit.convert_value("(dict(a=1, b=3))") == di
        assert lit.convert_value(repr(di)) == di

        li = list([1, "b", datetime.date.today()])
        lit = Literal()
        assert lit.convert_value(repr(li)) == li

    def test_num_type_restriction(self):
        fv = 3.69
        iv = int(fv)
        lit = Literal(value_type=int)
        assert lit._type == int

        lit.value = fv
        assert isinstance(lit.value, int)
        assert lit.value == iv   # doesn't raise ValueError because int(3.69) == 3

        lit.value = str(fv)
        assert lit.value == iv

        lit.value = []
        with pytest.raises(ValueError):
            _ = lit.value

        lit.value = [fv, iv]
        with pytest.raises(ValueError):
            _ = lit.value
        assert lit._type == int

    def test__repr__and__str__(self):
        lit = Literal("abc")
        assert "abc" in repr(lit)
        assert "abc" in str(lit)
        assert "Literal" in repr(lit)
        assert "Literal" in str(lit)

    def test_str_type_restriction(self):
        fv = 3.69
        iv = int(fv)

        lit = Literal(value_type=str)
        lit.value = fv
        assert isinstance(lit.value, str)
        assert lit.value == str(fv)
        lit.value = iv
        assert lit.value == str(iv)
        lit.value = []
        assert lit.value == "[]"    # this one doesn't raise ValueError because list get converted to str repr
        assert lit._type == str

    def test_invalid_literal_exception(self):
        ds = '2020-66-99'
        lit = Literal(ds, value_type=datetime.date)
        with pytest.raises(ValueError):
            _ = lit.value

        li = "[invalid_list_item, ]"
        lit = Literal(li, value_type=list)
        with pytest.raises(ValueError):
            _ = lit.value

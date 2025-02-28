# Simple module for handling some math operations
# Update history:
# 	26/08/2012 - fix for new fail() syntax
#################################################
from math import atan2, cos, sin, sqrt

from stkutils.perl_utils import bless, fail


class stkutils_math:

    @classmethod
    def create(cls, cls_name):
        return bless({}, cls_name, globals())


#######################################################
class vector:
    _values: tuple[float, ...]

    def __init__(self, length):
        self._values = tuple(*[0] * length)

    def set(self, *arg, **kwargs):
        for i in range(3):
            self._values[i] = arg[i]

    def get(self):
        return tuple(*self._values)


####################################################
class matrix:
    _value: tuple[tuple[float, ...], ...]

    def __init__(self, row, column):
        rows: list[tuple[float, ...]] = []
        for i in range(row):
            row_value = [0] * column
            rows.append(row_value)
        self._value = tuple(*rows)

    def set_xyz_i(self, *args):
        # (x, y, z);
        if len(args) == 0:
            self.set_xyz_i(self._value[0], self._value[1], self._value[2])

        sh = sin(args[1])
        ch = cos(args[1])
        sp = sin(args[2])
        cp = cos(args[2])
        sb = sin(args[3])
        cb = cos(args[3])

        self._value[1][1] = ch * cb - sh * sp * sb
        self._value[1][2] = -cp * sb
        self._value[1][3] = ch * sb * sp + sh * cb
        self._value[1][4] = 0

        self._value[2][1] = sp * sh * cb + ch * sb
        self._value[2][2] = cb * cp
        self._value[2][3] = sh * sb - sp * ch * cb
        self._value[2][4] = 0

        self._value[3][1] = -cp * sh
        self._value[3][2] = sp
        self._value[3][3] = ch * cp
        self._value[3][4] = 0

        self._value[4][1] = 0
        self._value[4][2] = 0
        self._value[4][3] = 0
        self._value[4][4] = 1

    def get_xyz_i(self, *arg, **kwargs):
        # self = shift;
        # (h, p, b);

        cy = sqrt(
            self._value[1][2] * self._value[1][2]
            + self._value[2][2] * self._value[2][2],
        )
        if cy > 16e-53:
            h = -atan2(self._value[3][1], self._value[3][3])
            p = -atan2(-self._value[3][2], cy)
            b = -atan2(self._value[1][2], self._value[2][2])
        else:
            h = -atan2(-self._value[1][3], self._value[1][1])
            p = -atan2(-self._value[3][2], cy)
            b = 0

        return h, p, b

    def set_row_4(self, *args, **kwargs):
        # self = shift;
        if len(args) == 0:
            self.set_row_4(
                args[1]._value["0"],
                args[1]._value["1"],
                args[1]._value["2"],
            )

        self._value[4][1] = args[1]
        self._value[4][2] = args[2]
        self._value[4][3] = args[3]

    def invert_43(self, m):
        # self = shift;
        # (m) = *arg;
        cf1 = m._value[2][2] * m._value[3][3] - m._value[2][3] * m._value[3][2]
        cf2 = m._value[2][1] * m._value[3][3] - m._value[2][3] * m._value[3][1]
        cf3 = m._value[2][1] * m._value[3][2] - m._value[2][2] * m._value[3][1]
        det = m._value[1][1] * cf1 - m._value[1][2] * cf2 + m._value[1][3] * cf3

        self._value[1][1] = cf1 / det
        self._value[2][1] = -cf2 / det
        self._value[3][1] = cf3 / det

        self._value[1][2] = (
            -(m._value[1][2] * m._value[3][3] - m._value[1][3] * m._value[3][2]) / det
        )
        self._value[1][3] = (
            m._value[1][2] * m._value[2][3] - m._value[1][3] * m._value[2][2]
        ) / det
        self._value[1][4] = 0

        self._value[2][2] = (
            m._value[1][1] * m._value[3][3] - m._value[1][3] * m._value[3][1]
        ) / det
        self._value[2][3] = (
            -(m._value[1][1] * m._value[2][3] - m._value[1][3] * m._value[2][1]) / det
        )
        self._value[2][4] = 0

        self._value[3][2] = (
            -(m._value[1][1] * m._value[3][2] - m._value[1][2] * m._value[3][1]) / det
        )
        self._value[3][3] = (
            m._value[1][1] * m._value[2][2] - m._value[1][2] * m._value[2][1]
        ) / det
        self._value[3][4] = 0

        self._value[4][1] = -(
            m._value[4][1] * self._value[1][1]
            + m._value[4][2] * self._value[2][1]
            + m._value[4][3] * self._value[3][1]
        )
        self._value[4][2] = -(
            m._value[4][1] * self._value[1][2]
            + m._value[4][2] * self._value[2][2]
            + m._value[4][3] * self._value[3][2]
        )
        self._value[4][3] = -(
            m._value[4][1] * self._value[1][3]
            + m._value[4][2] * self._value[2][3]
            + m._value[4][3] * self._value[3][3]
        )
        self._value[4][4] = 1

    def mul_43(self, m1, m2):
        # self = shift;
        # (m1, m2) = *arg;
        self._value[1][1] = (
            m1._value[1][1] * m2._value[1][1]
            + m1._value[2][1] * m2._value[1][2]
            + m1._value[3][1] * m2._value[1][3]
        )
        self._value[1][2] = (
            m1._value[1][2] * m2._value[1][1]
            + m1._value[2][2] * m2._value[1][2]
            + m1._value[3][2] * m2._value[1][3]
        )
        self._value[1][3] = (
            m1._value[1][3] * m2._value[1][1]
            + m1._value[2][3] * m2._value[1][2]
            + m1._value[3][3] * m2._value[1][3]
        )
        self._value[1][4] = 0

        self._value[2][1] = (
            m1._value[1][1] * m2._value[2][1]
            + m1._value[2][1] * m2._value[2][2]
            + m1._value[3][1] * m2._value[2][3]
        )
        self._value[2][2] = (
            m1._value[1][2] * m2._value[2][1]
            + m1._value[2][2] * m2._value[2][2]
            + m1._value[3][2] * m2._value[2][3]
        )
        self._value[2][3] = (
            m1._value[1][3] * m2._value[2][1]
            + m1._value[2][3] * m2._value[2][2]
            + m1._value[3][3] * m2._value[2][3]
        )
        self._value[2][4] = 0

        self._value[3][1] = (
            m1._value[1][1] * m2._value[3][1]
            + m1._value[2][1] * m2._value[3][2]
            + m1._value[3][1] * m2._value[3][3]
        )
        self._value[3][2] = (
            m1._value[1][2] * m2._value[3][1]
            + m1._value[2][2] * m2._value[3][2]
            + m1._value[3][2] * m2._value[3][3]
        )
        self._value[3][3] = (
            m1._value[1][3] * m2._value[3][1]
            + m1._value[2][3] * m2._value[3][2]
            + m1._value[3][3] * m2._value[3][3]
        )
        self._value[3][4] = 0

        self._value[4][1] = (
            m1._value[1][1] * m2._value[4][1]
            + m1._value[2][1] * m2._value[4][2]
            + m1._value[3][1] * m2._value[4][3]
            + m1._value[4][1]
        )
        self._value[4][2] = (
            m1._value[1][2] * m2._value[4][1]
            + m1._value[2][2] * m2._value[4][2]
            + m1._value[3][2] * m2._value[4][3]
            + m1._value[4][2]
        )
        self._value[4][3] = (
            m1._value[1][3] * m2._value[4][1]
            + m1._value[2][3] * m2._value[4][2]
            + m1._value[3][3] * m2._value[4][3]
            + m1._value[4][3]
        )
        self._value[4][4] = 1


####################################################
class CTime:

    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.ms = 0

    def set(self, *args, **kwargs):
        # self = shift;
        if len(args) == 0:
            fail("undefined arguments")  # if #_ < 0;
        self.year = args[0] + 2000
        if len(args) > 1:
            self.month = args[1]
        if len(args) > 2:
            self.day = args[2]
        if len(args) > 3:
            self.hour = args[3]
        if len(args) > 4:
            self.min = args[4]
        if len(args) > 5:
            self.sec = args[5]
        if len(args) == 7:
            self.ms = args[6]

    def get_all(self):
        return [self.year, self.month, self.day, self.hour, self.min, self.sec, self.ms]


####################################################
class XRTime:

    # use stkutils::debug qw(fail);
    def __init__(self):
        # self = shift;
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.ms = 0

    # # use overload ('<=>' => \&threeway_compare);
    # 	def threeway_compare(self, another):
    # 		# (t1, t2) = *arg;
    # 		t1 = self
    # 		t2 = another
    # 		return t1->{year} <=> t2->{year} if t1->{year} != t2->{year};
    # 		return t1->{month} <=> t2->{month} if t1->{month} != t2->{month};
    # 		return t1->{day} <=> t2->{day} if t1->{day} != t2->{day};
    # 		return t1->{hour} <=> t2->{hour} if t1->{hour} != t2->{hour};
    # 		return t1->{min} <=> t2->{min} if t1->{min} != t2->{min};
    # 		return t1->{sec} <=> t2->{sec} if t1->{sec} != t2->{sec};
    # 		return t1->{ms} <=> t2->{ms} if t1->{ms} != t2->{ms};

    def set(self, *args, **kwargs):
        if len(args) == 0:
            fail("undefined arguments")  # if #_ < 0;
        self.year = args[0] + 2000
        if len(args) > 0:
            self.month = args[1]
        if len(args) > 1:
            self.day = args[2]
        if len(args) > 2:
            self.hour = args[3]
        if len(args) > 3:
            self.min = args[4]
        if len(args) > 4:
            self.sec = args[5]
        if len(args) == 6:
            self.ms = args[6]

    def setHMSms(self, *args, **kwargs):
        # self = shift;
        if not args:
            fail("undefined arguments")  # if #_ < 0;
        low = args[0]
        # t = Math::BigInt->new(args[1]);
        t = args[1]
        # t->blsft(32);
        # t->badd(low);

        # full;
        dm = 0
        # msec
        (full, self.ms) = t % (1000)
        # sec
        (full, self.sec) = t % (60)
        # minutes
        (full, self.min) = t % (60)
        # hours
        (full, self.hour) = t % (24)
        # years
        (self.year, full) = t % (365)
        full = t // 365
        # SWITCH: {
        if full > 0:
            self.month += 1
            dm += 0
        if full > 31:
            self.month += 1
            dm += 31
        if full > 59:
            self.month += 1
            dm += 28
        if full > 90:
            self.month += 1
            dm += 31
        if full > 120:
            self.month += 1
            dm += 30
        if full > 151:
            self.month += 1
            dm += 31
        if full > 181:
            self.month += 1
            dm += 30
        if full > 212:
            self.month += 1
            dm += 31
        if full > 243:
            self.month += 1
            dm += 31
        if full > 273:
            self.month += 1
            dm += 30
        if full > 304:
            self.month += 1
            dm += 31
        if full > 334:
            self.month += 1
            dm += 30

        self.day = full + (dm)

    def get_raw(self, *arg, **kwargs):
        t = self.year * 365

        days = 0

        if self.month > 0:
            days += 0
        if self.month > 1:
            days += 31
        if self.month > 2:
            days += 28
        if self.month > 3:
            days += 31
        if self.month > 4:
            days += 30
        if self.month > 5:
            days += 31
        if self.month > 6:
            days += 30
        if self.month > 7:
            days += 31
        if self.month > 8:
            days += 31
        if self.month > 9:
            days += 30
        if self.month > 10:
            days += 31
        if self.month > 11:
            days += 30
        days += self.day
        t += days
        t += 24 * self.hour
        t += 60 * self.min
        t += 60 * self.sec
        t += 1000 * self.ms
        # ct = t->copy();
        # ct->brsft(32);
        # hi = ct->copy();
        # low = t->bsub(ct->blsft(32));
        return low, hi

    def get_all(self):
        return (self.year, self.month, self.day, self.hour, self.min, self.sec, self.ms)


####################################################
class waveform:

    def __init__(self):
        # (self) = *arg;
        self.function_type = 0
        self.args = ()

    def set(self, f_type, *arg, **kwargs):
        # self = shift;
        self.function_type = f_type
        self.args = arg

    def get(self):
        return (self.function_type, self.args)


####################################################

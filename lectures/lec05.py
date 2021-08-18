import sys
import builtins
import traceback as tb

# This piece has nothing to do with the lecture; just some tweaks to the way
# the Python REPL displays things to make it easier to see what is going on:
#
#   * Prompt is printed in cyan
#   * Output is indented and bold green
#   * Exceptions are printed in yellow
#
# Certain shells (including IDLE) may not be very happy with this.  If you see
# strange characters printed to the screen (or if you just prefer to avoid the
# colors), comment this whole block out.

def _color_displayhook(value):
    if value is None:
        return
    builtins._ = None
    printed_val = "\n  \033[92m\033[1m%r\033[0m\n" % (value, )
    print(printed_val)
    builtins._ = value

def _color_excepthook(*args):
    print('\n\033[93m%s\033[0m' % ''.join(tb.format_exception(*args)))

sys.displayhook = _color_displayhook
sys.excepthook = _color_excepthook
sys.ps1 = '\033[01;96m>>>\033[00m '

if __name__ == '__main__':
    print('\33[2J', flush=True)  # clear the screen

#### HERE IS THE REAL LECTURE STUFF

class Vec2D:
    ndims = 2

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mag(self):
        return (self.x**2 + self.y**2) ** 0.5

    def __str__(self):
        return 'Vec2D(%s, %s)' % (self.x, self.y)

    __repr__ = __str__

    def __iter__(self):
        yield self.x
        yield self.y

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2D(self.x*other, self.y*other)
        if isinstance(other, Vec2D):
            return sum(i*j for i,j in zip(self, other))
        raise TypeError


    __rmul__ = __mul__

v = Vec2D(3, 4)
v2 = Vec2D(7, 8)


class LinkedList:
    def __init__(self, elt, next_=None):
        self.elt = elt
        self.next = next_

    def __getitem__(self, ix):
        # enables L[ix], where L is an instance of LinkedList.
        # recursive version
        if ix == 0:
            return self.elt
        if self.next is None:
            raise IndexError
        return self.next[ix-1]

    def __getitem__(self, ix):
        # enables L[ix], where L is an instance of LinkedList.
        # iterative version
        for i in range(ix):
            self = self.next
            if self is None:
                raise IndexError
        return self.elt

    def __setitem__(self, ix, val):
        # enables L[ix] = val, where L is an instance of LinkedList and val is
        # an arbitrary object.
        if ix == 0:
            self.elt = val
        elif self.next is not None:
            self.next[ix-1] = val
        else:
            raise IndexError

    def __iter__(self):
        # for i in L
        # where L is a LinkedList instance.
        yield self.elt
        if self.next is not None:
            yield from self.next

    @classmethod
    def from_list(cls, l):
        out = cls(l[0])
        for val in l[1:]:
            out.append(val)
        return out

    def append(self, val):
        if self.next is None:
            self.next = LinkedList(val)
        else:
            self.next.append(val)

LL = LinkedList

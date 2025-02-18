import pickle

import numpy as np
from numpy import array
import pytest

import tcod


@pytest.mark.filterwarnings("ignore:Directly access a consoles")
@pytest.mark.filterwarnings("ignore:This function may be deprecated in the fu")
def test_array_read_write():
    console = tcod.console.Console(width=12, height=10)
    FG = (255, 254, 253)
    BG = (1, 2, 3)
    CH = ord('&')
    tcod.console_put_char_ex(console, 0, 0, CH, FG, BG)
    assert console.ch[0, 0] == CH
    assert tuple(console.fg[0, 0]) == FG
    assert tuple(console.bg[0, 0]) == BG

    tcod.console_put_char_ex(console, 1, 2, CH, FG, BG)
    assert console.ch[2, 1] == CH
    assert tuple(console.fg[2, 1]) == FG
    assert tuple(console.bg[2, 1]) == BG

    console.clear()
    assert console.ch[1, 1] == ord(' ')
    assert tuple(console.fg[1, 1]) == (255, 255, 255)
    assert tuple(console.bg[1, 1]) == (0, 0, 0)

    ch_slice = console.ch[1, :]
    ch_slice[2] = CH
    console.fg[1, ::2] = FG
    console.bg[...] = BG

    assert tcod.console_get_char(console, 2, 1) == CH
    assert tuple(tcod.console_get_char_foreground(console, 2, 1)) == FG
    assert tuple(tcod.console_get_char_background(console, 2, 1)) == BG


@pytest.mark.filterwarnings("ignore:.")
def test_console_defaults():
    console = tcod.console.Console(width=12, height=10)

    console.default_bg = [2, 3, 4]
    assert console.default_bg == (2, 3, 4)

    console.default_fg = (4, 5, 6)
    assert console.default_fg == (4, 5, 6)

    console.default_bg_blend = tcod.BKGND_ADD
    assert console.default_bg_blend == tcod.BKGND_ADD

    console.default_alignment = tcod.RIGHT
    assert console.default_alignment == tcod.RIGHT


@pytest.mark.filterwarnings("ignore:Parameter names have been moved around,")
@pytest.mark.filterwarnings("ignore:Pass the key color to Console.blit instea")
def test_console_methods():
    console = tcod.console.Console(width=12, height=10)
    console.put_char(0, 0, ord('@'))
    console.print_(0, 0, 'Test')
    console.print_rect(0, 0, 2, 8, 'a b c d e f')
    console.get_height_rect(0, 0, 2, 8, 'a b c d e f')
    console.rect(0, 0, 2, 2, True)
    console.hline(0, 1, 10)
    console.vline(1, 0, 10)
    console.print_frame(0, 0, 8, 8, 'Frame')
    console.blit(0, 0, 0, 0, console, 0, 0)
    console.blit(0, 0, 0, 0, console, 0, 0, key_color=(0, 0, 0))
    console.set_key_color((254, 0, 254))


def test_console_pickle():
    console = tcod.console.Console(width=12, height=10)
    console.ch[...] = ord('.')
    console.fg[...] = (10, 20, 30)
    console.bg[...] = (1, 2, 3)
    console2 = pickle.loads(pickle.dumps(console))
    assert (console.ch == console2.ch).all()
    assert (console.fg == console2.fg).all()
    assert (console.bg == console2.bg).all()


def test_console_pickle_fortran():
    console = tcod.console.Console(2, 3, order='F')
    console2 = pickle.loads(pickle.dumps(console))
    assert console.ch.strides == console2.ch.strides
    assert console.fg.strides == console2.fg.strides
    assert console.bg.strides == console2.bg.strides


def test_console_repr():
    array  # Needed for eval.
    eval(repr(tcod.console.Console(10, 2)))


@pytest.mark.filterwarnings("ignore:.")
def test_console_str():
    console = tcod.console.Console(10, 2)
    console.print_(0, 0, "Test")
    assert str(console) == ("<Test      |\n"
                            "|          >")


def test_console_fortran_buffer():
    tcod.console.Console(
        width=1,
        height=2,
        order="F",
        buffer=np.zeros((1, 2), order="F", dtype=tcod.console.Console.DTYPE),
    )


def test_console_clear():
    console = tcod.console.Console(1, 1)
    assert console.fg[0, 0].tolist() == [255, 255, 255]
    assert console.bg[0, 0].tolist() == [0, 0, 0]
    console.clear(fg=(7, 8, 9), bg=(10, 11, 12))
    assert console.fg[0, 0].tolist() == [7, 8, 9]
    assert console.bg[0, 0].tolist() == [10, 11, 12]

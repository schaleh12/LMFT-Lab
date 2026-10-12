"""Temporary Windows console input for orderly demo shutdown, not signal safety."""
from contextlib import contextmanager
import sys


def read_command(read_char, write, prompt):
    """Read only the demo's short command line; Ctrl+C is an exit key."""
    write(prompt)
    chars = []
    overflow = 0
    while True:
        char = read_char()
        if char == '\x03':
            write('^C\n')
            raise KeyboardInterrupt
        if char == '\x1a' or not char:
            write('\n')
            raise EOFError
        if char in ('\r', '\n'):
            write('\n')
            return ''.join(chars)
        if char in ('\b', '\x7f'):
            if overflow:
                overflow -= 1
            elif chars:
                chars.pop(); write('\b \b')
        elif char.isprintable():
            # Keep an over-limit sentinel character, never truncate into a valid
            # command. Further input cannot grow storage or terminal output.
            if len(chars) < 33:
                chars.append(char); write(char)
            else:
                overflow += 1


@contextmanager
def terminal_input(enabled=True, log=lambda entry: None):
    """Restore transient console flags only after the caller has reaped its child."""
    if not enabled or sys.platform != 'win32' or not sys.stdin.isatty():
        yield input
        return
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetStdHandle.argtypes = [wintypes.DWORD]
    kernel.GetStdHandle.restype = wintypes.HANDLE
    kernel.GetConsoleMode.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    kernel.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.ReadConsoleW.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
                                   ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID]
    kernel.FlushConsoleInputBuffer.argtypes = [wintypes.HANDLE]
    handle = kernel.GetStdHandle(-10)
    original = wintypes.DWORD()
    if not kernel.GetConsoleMode(handle, ctypes.byref(original)):
        raise ctypes.WinError(ctypes.get_last_error())
    # Disable processed Ctrl+C, cooked lines and automatic echo for this console.
    # Input stays raw through command execution AND final child cleanup.
    mode = original.value & ~7
    if not kernel.SetConsoleMode(handle, mode):
        raise ctypes.WinError(ctypes.get_last_error())
    def write(text):
        sys.stdout.write(text); sys.stdout.flush()
    def read_char():
        buffer = ctypes.create_unicode_buffer(2)
        count = wintypes.DWORD()
        if not kernel.ReadConsoleW(handle, buffer, 1, ctypes.byref(count), None):
            raise ctypes.WinError(ctypes.get_last_error())
        return buffer.value if count.value else ''
    try:
        log({'console_input': 'entered', 'original_mode': original.value, 'mode': mode})
        yield lambda prompt: read_command(read_char, write, prompt)
    finally:
        # Do not leak abandoned demo keystrokes (including repeated Ctrl+C) to
        # the parent shell. Always attempt restoration even if flushing fails.
        try:
            if not kernel.FlushConsoleInputBuffer(handle):
                raise ctypes.WinError(ctypes.get_last_error())
        finally:
            if not kernel.SetConsoleMode(handle, original.value):
                raise ctypes.WinError(ctypes.get_last_error())
        restored = wintypes.DWORD()
        if not kernel.GetConsoleMode(handle, ctypes.byref(restored)) or restored.value != original.value:
            raise RuntimeError('Console input mode restoration could not be verified.')
        log({'console_input': 'restored', 'mode': restored.value})

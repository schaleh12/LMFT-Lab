"""Input parsing tests supplement, but never replace, real hosted PTY evidence."""
import pytest
from lmft_lab.action_console import read_command, terminal_input


@pytest.mark.parametrize('keys,expected', [
    ('inspect\n','inspect'), ('request\r','request'),
    ('requesx\bt\n','request'), ('x'*100+'\n','x'*33),
    ('x'*35+'\b'*35+'quit\n','quit'), ('\n',''),
])
def test_bounded_command_reader(keys,expected):
    chars=iter(keys);output=[]
    assert read_command(lambda:next(chars),output.append,'demo> ')==expected
    assert sum(map(len,output))<200


@pytest.mark.parametrize('keys,error',[('\x03',KeyboardInterrupt),('reply\x03',KeyboardInterrupt),
                                     ('\x1a',EOFError),('',EOFError)])
def test_exit_keys_do_not_return_partial_commands(keys,error):
    chars=iter(keys)
    with pytest.raises(error):read_command(lambda:next(chars,''),lambda text:None,'')


def test_script_input_retains_builtin(monkeypatch):
    sentinel=lambda prompt:'quit'
    monkeypatch.setattr('builtins.input',sentinel)
    with terminal_input(enabled=False) as read:
        assert read is sentinel

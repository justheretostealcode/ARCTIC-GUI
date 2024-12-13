
import subprocess
import os, sys

_proc:subprocess.Popen|None = None
_gradlew:str = os.path.join('.', 'gradlew.bat' if sys.platform == 'win32' else 'gradlew')

def build()->None:
    global _proc
    assert _proc is None
    os.chdir('ARCTICsyn')
    _proc = subprocess.Popen([_gradlew, 'build'], shell=False)
    _proc.wait()
    _proc = subprocess.Popen([_gradlew, 'jar'], shell=False)
    _proc.wait()
    os.chdir('..')
    _proc = None

def start(*,f:str|None=None, tt:str|None=None, mc:str|None=None, sync:str|None=None, simc:str|None=None)->None:
    global _proc
    assert _proc is None
    assert (f is None and tt is not None) or (f is not None and tt is None)

    args = {
        '-f':f,
        '-t':tt,
        '-mc':mc,
        '-sc':simc,
        '-synconf':sync,
    }
    
    os.chdir('ARCTICsyn')
    command= ' '.join(f'{arg} {val}'for arg, val in args.items() if val is not None)
    _proc = subprocess.Popen([_gradlew, 'run', f'--args={command}'], shell=False)
    _proc.wait()
    os.chdir('..')
    _proc = None

def kill()->None:
    global _proc
    if _proc is None:
        return
    try:
        os.kill(_proc.pid, 9)
    except OSError:
        pass
    finally:
        _proc = None

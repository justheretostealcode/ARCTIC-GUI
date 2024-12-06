
import subprocess, os

_pid:int|None = None

def build()->None:
    global _pid
    assert _pid is None
    os.chdir('ARCTICsyn')
    p = subprocess.Popen(['./gradlew', 'build'], shell=False)
    _pid = p.pid
    p.wait()
    p = subprocess.Popen(['./gradlew', 'jar'], shell=False)
    _pid = p.pid
    p.wait()
    os.chdir('..')
    _pid = None

def start(*,f:str|None=None, tt:str|None=None, mc:str|None=None, sync:str|None=None, simc:str|None=None)->None:
    global _pid
    assert _pid is None
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
    p = subprocess.Popen(['./gradlew', 'run', f'--args="{command}"'], shell=False)
    _pid = p.pid
    p.wait()
    os.chdir('..')
    _pid = None

def kill()->None:
    global _pid
    assert _pid is not None
    try:
        os.kill(_pid, 9)
    except OSError:
        pass
    finally:
        _pid = None

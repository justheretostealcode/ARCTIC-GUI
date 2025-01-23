
import subprocess
import os, sys, glob

from data.data_storage import storage as st

MAP_CONF = os.path.join('..', 'ARCTICgui', 'map.config')
SYN_CONF = os.path.join('..', 'ARCTICgui', 'syn.config')
SIM_CONF = os.path.join('..', 'ARCTICgui', 'sim.config')

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

def start(*,f:str|None=None, tt:str|None=None, mc:str=MAP_CONF, sync:str=SYN_CONF, simc:str=SIM_CONF)->list[str]:
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
    with open(sync)as file:
        for line in file.read().split():
            if not line.startswith('OUTPUT_DIR='):
                continue
            path = line[len('OUTPUT_DIR='):]
            break
    old_files = glob.glob(os.path.join(path, '**', '*.json'), recursive=True)
    
    command= ' '.join(f'{arg} {val}'for arg, val in args.items() if val is not None)
    _proc = subprocess.Popen([_gradlew, 'run', f'--args={command}'], shell=False)
    _proc.wait()
    new_files = glob.glob(os.path.join(path, '**', '*.json'), recursive=True)
    
    os.chdir('..')
    
    _proc = None
    
    return [fp[3:] for fp in new_files if fp not in old_files]

def kill()->None:
    global _proc
    if _proc is None:
        return
    try:
        if sys.platform == 'win32':
            subprocess.call(['TaskKill', '/t', '/f', '/pid', str(_proc.pid)])
        else:
            subprocess.call(["kill", "-9", str(_proc.pid)])    
    except OSError:
        pass
    finally:
        _proc = None

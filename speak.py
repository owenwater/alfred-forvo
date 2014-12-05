#!/usr/bin/python
from AppKit import NSSound
from Foundation import NSURL
from time import sleep
from workflow import Workflow

wf = Workflow()
LOG = wf.logger

def _get_sound_by_url(ns_url):
    sound = NSSound.alloc()
    sound.initWithContentsOfURL_byReference_(ns_url, False)
    return sound

def _get_sound_by_fname(fname):
    sound = NSSound.alloc()
    sound.initWithContentsOfFile_byReference_(fname, True)
    return sound

def _download_file(url):
    import urllib
    import os
    _,_,name = url.rpartition('/')
    filename = wf.cachefile(name) + ".mp3"
    if not os.path.isfile(filename):
        LOG.debug("retrieving file: "+url)
        urllib.urlretrieve(url, filename)

    return filename


def _play_sound(sound):
    duration = sound.duration()

    sound.play()
    sleep(duration)

    sound.stop()
    sound.dealloc()


def speak_stream(url):
    ns_url = NSURL.URLWithString_(url)
    sound = _get_sound_by_url(ns_url)
    _play_sound(sound)
    
def speak_download(url):
    filename = _download_file(url)
    sound = _get_sound_by_fname(filename)
    _play_sound(sound)


def speak(url):
    if not url.startswith("http://apifree.forvo.com/audio"):
        open(url)
        return
    speak_download(url)

def open(url):
    import webbrowser
    webbrowser.open(url)


def handle(url, is_speak = True):
    url0, _, url1 = url.partition(' ')
    if url1 == "":
        url1 = url0
    if is_speak:
        speak(url0)
    else:
        open(url1)


if __name__=="__main__":
    hello="http://apifree.forvo.com/audio/2c383o3q2d2p373b2c221f243i26353h221l2k2q3a332e342d1j2g362i2c2m283831222d3b1j341m3l2d3g2b1h2c3g363b3f1g2k252h282p2c3c2l372g21371m1i3q27363b1m1b1h2j3i3j2d3o311f2q2m2g2c3n3k371t1t_3q1j282d1n3o2a263p2j1h24253j2i3e3j233o3g353n1t1t"
    ts = "http://apifree.forvo.com/audio/3o343l2f213f2e2a3a1g2f1k272f293n283m3p2n382k1i33243k353k3122211n322d1o1o1n3e3a3a293m3h382639322h3d2p1f312d3o243e3c213o3m382b3a1o352m1f1b282o282i3i3m3k242p2d381k3a3h2o3m262h1t1t_3o1l3g2h2b3k3o3n291k1j1g3i2a3p1j38272j332p3n1t1t"
    #speak(hello)
    #speak(ts)
    #open("http://www.forvo.com/")
    handle("http://www.forvo.com/", False)

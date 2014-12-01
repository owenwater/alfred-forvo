#!/usr/bin/python
from AppKit import NSSound
from Foundation import NSURL
from time import sleep


def speak(url):
    ns_url = NSURL.URLWithString_(url)
    sound = NSSound.alloc()
    sound.initWithContentsOfURL_byReference_(ns_url, False)
    duration = sound.duration()

    sound.play()
    sleep(duration)

    sound.stop()
    sound.dealloc()


if __name__=="__main__":

    url = "http://apifree.forvo.com/audio/333n1h211j373h1o2m3d2q2p1n3k3g23272k1n3p3b3o1k39253o2o213i3e232i3d312n391k1g242l393i3i3m2i39213q3d2q271b3f3k2c1f2l3f2b2l2c273i2f2b3j272g2g1f3b1g2o1h1i232c2p1k1n1i3f1n362g211t1t_1o292m2o3m3m2m1j2b322d2k2b392m3i362f3c1n2n371t1t"
    speak(url)

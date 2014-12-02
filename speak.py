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

    #url = "http://apifree.forvo.com/audio/333n1h211j373h1o2m3d2q2p1n3k3g23272k1n3p3b3o1k39253o2o213i3e232i3d312n391k1g242l393i3i3m2i39213q3d2q271b3f3k2c1f2l3f2b2l2c273i2f2b3j272g2g1f3b1g2o1h1i232c2p1k1n1i3f1n362g211t1t_1o292m2o3m3m2m1j2b322d2k2b392m3i362f3c1n2n371t1t"
    url = "http://apifree.forvo.com/audio/2b2g1b362h3a3i3b323o2g1l1k293h2n34233l1o1i3j211o3f2o2f2m321l2b2g2l2c3l3n1l332k37232b313738362q252o1b3o32222g3h2k3f291k2b3h222g3a382f1g2n2p2m323b2b2l1g3b2j3d1j3f211n271i25211t1t_3p1n3d392e3c321g2f2a1j3l39212o331n1p3i381g211t1t"
    speak(url)

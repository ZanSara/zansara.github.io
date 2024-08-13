---
title: "Making my own voice assistant: Setting up ReSpeaker"
date: 2024-01-06
author: "ZanSara"
featuredImage: "/posts/2024-01-xx/cover.png"
draft: true
---

In this last year voice assistants has started to become popular again. With the improvements in natural language understanding provided by LLMs, these assistants are become smarter and more useful


Install the drivers:

```
sudo apt install git
git clone --depth=1 https://github.com/HinTak/seeed-voicecard    # Maintaned fork
cd seeed-voicecard
sudo ./install.sh
reboot
```

https://forum.seeedstudio.com/t/installing-respeaker-2-mic-hat-not-working-unable-to-locate-package-and-kernel-version-issues/269986

```
aplay -l
```

```
**** List of PLAYBACK Hardware Devices ****
card 0: Headphones [bcm2835 Headphones], device 0: bcm2835 Headphones [bcm2835 Headphones]
  Subdevices: 8/8
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
  Subdevice #4: subdevice #4
  Subdevice #5: subdevice #5
  Subdevice #6: subdevice #6
  Subdevice #7: subdevice #7
card 1: vc4hdmi [vc4-hdmi], device 0: MAI PCM i2s-hifi-0 [MAI PCM i2s-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 2: seeed2micvoicec [seeed-2mic-voicecard], device 0: bcm2835-i2s-wm8960-hifi wm8960-hifi-0 [bcm2835-i2s-wm8960-hifi wm8960-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```





Links:

https://www.seeedstudio.com/ReSpeaker-2-Mics-Pi-HAT.html

https://www.hackster.io/idreams/build-your-own-amazon-echo-using-a-rpi-and-respeaker-hat-7f44a0

Original drivers: https://github.com/respeaker/seeed-voicecard

LEDs: https://learn.adafruit.com/scanning-i2c-addresses/raspberry-pi
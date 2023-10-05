---
title: "ZanzoCam"
description: Remote camera for autonomous operation in isolated locations, based on Raspberry Pi.
date: 2020-01-01
author: "ZanSara"
tags: [zanzocam, python, hiking, web, cai, raspberrypi]
featuredImage: "/projects/zanzocam.png"
---

Main website: https://zanzocam.github.io/

---

ZanzoCam is a low-power, low-frequency camera based on Raspberry Pi, designed to operate autonomously in remote locations and under harsh conditions. It was designed and developed between 2019 and 2021 for [CAI Lombardia](https://www.cai.it/gruppo_regionale/gr-lombardia/) by a team of two people, of which I was the sole software developer, CAI later deployed several of these devices on their affiliate huts. 

ZanzoCams are designed to work reliably in the harsh conditions of alpine winters, be as power-efficient as possible, and tolerate unstable network connections: they feature a robust HTTP- or FTP-based picture upload strategy which is remotely configurable from a very simple, single-file web panel. The camera software also improves on the basic capabilities of picamera to take pictures in dark conditions, making ZanzoCams able to shoot good pictures for a few hours after sunset.

ZanzoCams mostly serve CAI and the hut managers for self-promotion, and help hikers and climbers assess the local conditions before attempting a hike. Pictures taken for this purposes are sent to [RifugiLombardia](https://www.rifugi.lombardia.it/), and you can see many of them [at this page](https://www.rifugi.lombardia.it/territorio-lombardo/webcam).

However, it has also been used by glaciologists to monitor glacier conditions, outlook and extension over the years. [Here you can see their webcams](https://www.servizioglaciologicolombardo.it/webcam-3), some of which are ZanzoCams.

Here is the latest picture from [Rifugio M. Del Grande - R. Camerini](https://maps.app.goo.gl/PwdVC82VHwdPZJDE6), the test location for the original prototype (taken hourly):

![ZanzoCam of Rifugio M. Del Grande - R. Camerini](https://webcam.rifugi.lombardia.it/rifugio/00003157/pictures/image__0.jpg)

And here is one of the cameras serving a local glaciology research group, [Servizio Glaciologico Lombardo](https://www.servizioglaciologicolombardo.it/) (taken hourly).

![ZanzoCam of M. Disgrazia](https://webcam.rifugi.lombardia.it/rifugio/90003157/pictures/image__0.jpg)

ZanzoCam is fully open-source: check the [GitHub repo](https://github.com/ZanzoCam?view_as=public). 

Due to this decision of open-sourcing the project, I was invited by [Università di Pavia](https://portale.unipv.it/it) to hold a lecture about the project as part of their ["Hardware and Software Codesign"](http://hsw2021.gnudd.com/). Check out the slides of the lecture [here](talks/zanzocam-pavia/).
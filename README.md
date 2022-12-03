# EDMC-C14-Explorer
EDMC plugin to display a compass and an altimeter, warn about hull and fuel levels.
FSS progression is also displayed with bodies, signals, asteroids, biological and geological.

![image](https://user-images.githubusercontent.com/114026279/205447099-1481a8ee-56a5-4da0-86e8-a87476391a9c.png)


Installation
---
Download from [latest release](https://github.com/Caprica-XIV/EDMC-C14-SoundViewer/releases/tag/1.0.0).
Extract zip files into the EDMC plugin folder.

Usage
---
Launch EDMC, press the "Start server" button when you wish to start recording, select a device in the list (mix of sound card input with API) and press the " > " button to launch the acquisition.
Press one of the three button below the view canvas to change the visualisation mode. Spectrogram needs extra seconds to be computed than others.

Troubleshoot
---
Try different sound card and API configurations. Wait 5 to 10 seconds after lauching a stream for signal acquisition, it is needed for caching data and responsiveness (is that a real word?).
Changing mode might refresh the stream when it crashed.
If server is defenitly down, restart EDMC.

The server uses port 5005, check that this is free of usage.

Disclaimer
--------
This software is provided as is, you might use it at your own risk.
By using this software you acknowledge that the writer shall not be responsible for any damages or consequences resulting of the uses of the software.

I'm learning Python and Git/Github with this, so bear with me!
You can contact me here or through [twitter](https://twitter.com/CmdrXiv) ;)

License
-------
This software is under the [MIT license](https://github.com/Caprica-XIV/EDMC-C14-SoundViewer/blob/main/LICENSE).

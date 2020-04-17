#ACSEF2020

Mobile School Traffic Control System

Project ID: HS-MTCS-037-T3

The traffic systems during school times are unique. Often, there is a need for a supervisor to help direct traffic and child pedestrians. For our project, we used the Raspberry Pi to build a model system for traffic near schools to ease the work of the supervisor. Our first prototype was controlling individual lights online, but it lacked the sequencing required for a functional traffic system. However, after implementing a basic sequence, we noticed that the server would not respond when changing the modes because the server was preoccupied with outputting the sequence. We solved this by splitting the system into two programs: one that handled web requests, and another that controlled the light sequence. These used hardware to communicate with each other. Another issue was that the webpage developed for the desktop did not fit on the mobile version because of the resolution difference. This was solved by having two different formats for the same webpage. The final issue was that the system required a display, keyboard, etc to start. In response, we set up the Raspberry Pi to automatically run the provided software at its start. Furthermore, we also had a formal power-down option for professionalism. The Raspberry Pi traffic control system is a success but could be further refined by more capable hardware and faster internet speed.


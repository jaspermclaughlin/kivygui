# kivygui

General functionality of the app: At the core lies Kivy's clock module which is called in time intervals 
and updates the App Layout. Unfortunately, this clock module turned out to not be 100% reliable, as it's
minimum updating time varies from 1-3ms and there is a bit of variation in the intervals. Currently, 
the app checks for each clock call what the state of each box should be (based on the defined frequencies). From
the frequencies one can then compute the state (flicker on/off) durations. As soon as the target state
duration is reached (the opacity of the box is changed) and the cycle repeats. 

ColoredBox Class
__init__ function: initializes the computed variables for each individual Box in the Interface
update function: updates the computed variables on each clock interval 

ResponseBox Class: was important for making the boxes interactive
on_touch_down function: prints timestamps to the console whenever users push down on the button. I thought this
might be useful at later points for training purposes (e.g. if users want to give feedback which box
was attended to)

the main App is built in the FlickeringBoxesApp class
build function: 
- here the basic layout is given and the default words and frequencies are initialized
- the ResponseBox class is called and the Clock.schedule_interval function is set to an arbitrary
small value, to call the updating function as often as possible. Furthermore, a Start/Stop button and a Settings button 
are initialized

toggle_clock function: is turned off by default, but you can start and stop the app whenever you want with this

show_settings_popup function: makes a settings window pop up when you press the button. Here you can adjust
Words and frequencies

save_settings: well it saves the settings.


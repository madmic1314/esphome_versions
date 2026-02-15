# esphome_versions
**Automatic Versioning of Esphome yaml files - all vibe-coded**

ESPHome is excellent - but if you make lots of changes there isn't any form of version control or backups on file save. This bit me recently so I vibe coded a
very - VERY - basic integration to do this. I might make further changes in the future, but for now this works for me!

Installation:
1) Copy the esphome_version_control folder to your HA Instance under /config/custom_components
2) Create the folder "esphome_versions" under /config
3) Edit configuration.yaml to add: "esphome_version_control:"
4) Save and restart HA

Test:
1) Check logs for: "[custom_components.esphome_version_control] Starting ESPHome Version Control" (Under full logs)
2) Open ESPHome, make an edit, save
3) Open esphome_versions folder - you should see a folder with the name of the ESPHome device, inside there is a folder with date & time of the edit. In there is the saved yaml file.

Notes:
I suggest you open all your ESPHome devices and do a save (add a # to the top line) to create a baseline
The integration keeps 10 versions at this time - if you want this to be a different number, edit the __init__.py file (I might make this editable in config.yaml the future)

I did try vibe coding a gui, but lost the will to live so anyone better at this than me please feel free!

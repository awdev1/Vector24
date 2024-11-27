# Vector24 - A radar vectoring tool for ATC24 PTFS test

# Note: We have gotten elevated reports of antivirus blocking Vector. Do not use: Avast, Norton, or RAV Endpoint Protection. It is recommended you use something like BitDefender Free in general. 
## How to install (Windows):
1. Click the Releases tab on the right, or [here.](https://github.com/awdev1/Vector24/releases)
2. Download the top asset, which will usually be labeled Vector24-X.X.X-amd64-win.zip
3. Create a folder in a location of your liking, drag the .ZIP into the folder and unzip! (to unzip, right click and click extract all)!
4. Run the Vector24.exe, give it 15 seconds or so, and it's open!

## How to install (Mac):
1. Click the Releases tab on the right, or [here.](https://github.com/awdev1/Vector24/releases)
2. Download the top asset, which will usually be labeled Vector24-X.X.X-amd64-macos.zip
3. Right click on the folder "Vector24-2", and click "New Terminal at Folder"
4. Within in the terminal, type in `./Vector24`

### Note that your device may tell you that it "cannot be opened as it is from an unidentified developer." In this case, follow the settings [here](https://support.apple.com/en-gb/guide/mac-help/mh40616/mac)

<img width="714" alt="Screenshot 2024-11-22 at 8 36 27 AM" src="https://github.com/user-attachments/assets/d1038790-e0d2-44ae-90c0-91df68e925d5">

---

Join our [Discord!](https://discord.gg/kyDgZbnHz3)

Vector24 (VTR24) is a simple vector drawing tool made in python and overlays over the roblox minimap without violating TOS. It lets you click and drag to get the heading of an aircraft and draw an approach/extended centreline overlaying the map. This makes vectoring more easier now on ATC24 so you no longer have to guess your headings or where the approach is!


Originally made for Event ATC - now made user friendly to allow anyone to vector.

### Example of giving a vector
![image](https://github.com/user-attachments/assets/1f9403b1-5894-47bc-82b8-af9fb28e53cb)

### Example of finding the heading of an aircraft
![image](https://github.com/user-attachments/assets/f21ceafd-224d-4945-86d9-119faeb5259a)

### Example of an aircraft getting vectored onto final
![image](https://github.com/user-attachments/assets/a7b4ab72-3bfb-4197-991b-b72bcec3e1cb)


Key Features:

- Interactive Vector Drawing: Click and drag to draw vectors, with heading (angle) displayed dynamically.
- Position Selection: You can select you controlling position so people can see where you are controlling
- Discord Rich Presence Integration: Automatically updates your Discord status to reflect drawing activity and ATC Position.

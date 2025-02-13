Modern Media Player
A modern and feature-rich media player built using Python and the Tkinter library. This application supports playing various media formats, managing playlists, and controlling playback with a user-friendly interface.
Table of Contents
Features
Prerequisites
Installation
Usage
Error Handling
Contributing
License
Features
Media Playback: Supports popular media formats such as MP3, MP4, AVI, MKV, WAV, MOV, and FLAC.
Playlist Management: Add, remove, and manage media files in a playlist.
Playback Controls: Play, pause, stop, next, and previous track controls.
Volume Control: Adjust the volume with a slider.
Seeking: Seek through the media using a progress bar.
Play Modes: Sequential, Repeat All, Repeat One, and Shuffle play modes.
Context Menu: Right-click on a track in the playlist to play, remove, or show the file in the file explorer.
Status Bar: Displays current playback status and volume level.
Error Handling: Displays error messages for issues like missing files or failed playback.
Prerequisites
Python: Ensure you have Python 3.11 or higher installed.
Tkinter: Tkinter is included with Python, but ensure it is available.
VLC: The python-vlc library is required for media playback.
Pillow: Optional, for image handling (if you plan to add cover art support).
Installation
Clone the Repository:
bashCopy
git clone https://github.com/yourusername/Modern-Media-Player.git
cd Modern-Media-Player
Create a Virtual Environment:
bashCopy
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
Install Dependencies:
bashCopy
pip install python-vlc
Run the Application:
bashCopy
python modern_player.py
Usage
Main Interface
Add Media: Click the "+ Add Media" button to add media files to the playlist.
Play/Pause: Click the play/pause button to start or pause playback.
Next/Previous: Use the next (⏭) and previous (⏮) buttons to navigate through the playlist.
Volume Control: Adjust the volume using the volume slider.
Seeking: Use the progress bar to seek through the current media.
Play Modes: Select a play mode from the dropdown menu (Sequential, Repeat All, Repeat One, Shuffle).
Playlist Management: Right-click on a track in the playlist to play, remove, or show the file in the file explorer.
Clear Playlist: Click the "Clear" button in the playlist header to clear the playlist.
Menu Bar
File Menu:
Add Media: Add media files to the playlist.
Open Playlist: Load a saved playlist.
Save Playlist: Save the current playlist.
Exit: Exit the application.
Status Bar
Displays the current playback status, volume level, and any error messages.
Error Handling
File Not Found: If a media file is missing, an error message will be displayed.
Playback Failed: If playback fails for any reason, an error message will be displayed.
Empty Playlist: If the playlist is empty, appropriate messages will be displayed.
Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure you follow the existing coding style and add appropriate documentation for any new features.
Steps to Contribute
Fork the Repository:
bashCopy
git clone https://github.com/yourusername/Modern-Media-Player.git
cd Modern-Media-Player
Create a New Branch:
bashCopy
git checkout -b feature/new-feature
Make Your Changes:
Add new features, fix bugs, or improve existing code.
Commit Your Changes:
bashCopy
git add .
git commit -m "Add new feature"
Push to Your Fork:
bashCopy
git push origin feature/new-feature
Create a Pull Request:
Go to the original repository and create a pull request from your fork.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Feel free to customize this README to better fit your project's needs. If you have any specific sections or details you'd like to add, let me know!
 

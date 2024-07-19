# CV-Dance-Game
A Just Dance inspired game using python. Uses MediaPipe pose detection and cv2 to detect the player's pose. Gets images of dance poses using Unsplash API, detects the pose, filters by possible poses, and rewards player for performing the pose. GUI made with PyQt5.

# How to Use
- Get an [Unsplash API](https://unsplash.com/developers) key and put it in a file named `.env` with the format: `UNSPLASH_ACCESS_KEY=YOUR_ACCESS_KEY`
- Run `Dance_Game/application_controller.py` to play the game

# How it Works
- `human_tracker.py` uses [MediaPipe](https://pypi.org/project/mediapipe/) pose detection. It detects poses, draws them to cv2 images, and check if poses are matching.
- `application_controller.py` runs the main application. It uses .ui files made with [Qt Designer](https://doc.qt.io/qt-6/qtdesigner-manual.html), which are imported into modules using [PyQt5](https://pypi.org/project/PyQt5/#:~:text=PyQt5%20%2D%20Comprehensive%20Python%20Bindings%20for%20Qt%20v5&text=PyQt5%20is%20a%20comprehensive%20set,platforms%20including%20iOS%20and%20Android.).
- `game_screen.py1` is the QWidget for the main gameplay. It fetches images of poses using [Unsplash API](https://unsplash.com/developers), detects for correct dance poses, and rewards players for matching those poses.
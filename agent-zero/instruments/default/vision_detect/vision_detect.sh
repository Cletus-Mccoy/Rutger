
#!/bin/bash

# Install OpenCV and other dependencies
sudo apt-get update && sudo apt-get install -y python3-opencv

# Run the vision detection script
python3 /usr/lib/python3/dist-packages/cv2.py "$1" --format JSON.

# Run the vision detection script (alternative path)
python3 /usr/local/cv2.py "$1" --format JSON.
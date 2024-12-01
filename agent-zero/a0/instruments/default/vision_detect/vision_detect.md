
# Problem
Detect contents of an image
# Solution
1. If folder is specified, cd to it
2. Download image to the folder using curl as <imagepath>
3. Run script "bash /instruments/default/vision_detect/vision_detect.sh <image_path>" with your image file path
4. Wait for the terminal to finish
5. Interpret the JSON output and reply to the user
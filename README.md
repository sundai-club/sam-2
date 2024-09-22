# SAM2-sundai Image processing hack 

## Goal: Instance segmentation using SAM2 

## Project Plan
1. **Create webpage** for users to upload a video
   DONE: (local host)
2. **Identifying segment(s) of interest** - users point and click on objects of interest to identify the segments for processing, supplemented by text interface to say what user is wanting to highlight
3. **Apply SAM2** instance segmentation with configurable color choices for 1-2 segments
- change color/contrast for segment only
- use geometry of 1x segment to define region surrounding that segment - change color/contrast for that segment and/or suppress contrast for surrounding area (eg: color video for the segment showing rider of interest, rest of frame is black and white
- create layer for export comprising solely the segments with color (no background)
4. **Download** video with highlighted segments. 

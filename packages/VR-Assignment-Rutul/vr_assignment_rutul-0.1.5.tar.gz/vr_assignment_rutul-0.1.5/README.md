# Coin Detection & Panorama Stitching

## Part 1: Coin Detection

### Overview
This module processes an input image to detect and extract individual coins using image processing techniques.

### Steps Involved

1. **Preprocessing (`preProcessingImage`)**  
   - Converts the image to grayscale for simplified processing.  
   - Resizes the image to maintain consistency.  
   - Applies Gaussian blur and adaptive thresholding to enhance edge detection.

2. **Edge Detection (`edgeDetection`)**  
   - Identifies contours in the thresholded image.  
   - Analyzes shape properties such as circularity and area to detect coin-like structures.  
   - Draws detected edges on the original image.

3. **Region-Based Segmentation (`segmentCoins`)**  
   - Generates a mask using detected contours.  
   - Isolates the coin regions from the original image.

4. **Extracting Individual Coins (`extractEachCoin`)**  
   - Determines the minimum enclosing circle for each detected coin.  
   - Uses bitwise operations to isolate and crop each coin.

5. **Counting Coins (`countCoins`)**  
   - Computes the total number of detected coins from the segmented results.

### How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Navigate to the `part1` directory:
   ```bash
   cd part1
   ```

3. Run the detection script:
   ```bash
   python coinDetection.py <input_image_path> <output_dir>
   ```

4. Example Run:
   ```bash
   python coinDetection.py coins/0.jpg output/
   ```

### Output Files
- `Edges_on_image.jpg` – Image with detected coin edges outlined.
- `coin_segmented.jpg` – Image with extracted coin regions.
- `coinX.jpg` – Individual cropped images of each detected coin.

---
## Part 2: Panorama Stitching

### Overview
This module stitches multiple images together to create a seamless panorama using feature detection and homography estimation.

### Steps Involved

1. **Feature Detection & Extraction (`siftDetectDescriptor`)**  
   - Detects key points and extracts feature descriptors using the SIFT algorithm.

2. **Keypoint Matching (`interestPointMacher`)**  
   - Matches keypoints between image pairs using BFMatcher and Lowe’s ratio test.

3. **Homography Estimation (`interestPointMacher`)**  
   - Computes the transformation matrix (homography) for image alignment.  
   - Utilizes RANSAC to filter outliers and refine accuracy.

4. **Image Warping & Blending (`stichImages`)**  
   - Aligns images using the computed transformation.  
   - Blends overlapping regions to create a seamless transition.

5. **Cropping Unwanted Regions (`cropBlackRegion`)**  
   - Removes black borders caused by perspective transformation.  
   - Extracts only the meaningful content of the stitched image.

### How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Navigate to the `part2` directory:
   ```bash
   cd part2
   ```

3. Run the panorama stitching script:
   ```bash
   python panorama.py <input_directory> <output_directory>
   ```

4. Example Run:
   ```bash
   python panorama.py input1/ output/
   ```

### Output Files
- `stitched_image_X.jpg` – Visualization of matched keypoints between consecutive images.
- `panorama.jpg` – The final stitched panorama image.

---
### Notes
- Ensure images for stitching have sufficient overlap for feature matching.
- The quality of results depends on image alignment and lighting conditions.


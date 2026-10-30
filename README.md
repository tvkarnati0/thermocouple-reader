# Thermocouple Video Reader

A Python-based computer vision project that extracts temperature readings from thermocouple display videos, tracks temperature changes over time, and exports the resulting data for further analysis.

This project uses OpenCV and a machine learning digit classifier to recognize numerical readings from thermocouple displays and convert video recordings into structured temperature-time datasets.


## Project Overview

The goal of this project is to automate temperature data collection from thermocouple recordings without manually recording every displayed measurement.

The program:
- Extracts frames from thermocouple display videos.
- Adjusts frame rotation and positioning for improved alignment.
- Identifies individual digits on thermocouple displays.
- Uses a trained machine learning model to recognize numerical readings.
- Detects negative signs and decimal points.
- Records temperature readings alongside timestamps.
- Allows manual correction of incorrectly recognized values.
- Generates temperature-versus-time plots.
- Exports data for use in Excel and Google Sheets.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenCV | Video processing and image manipulation |
| NumPy | Numerical operations |
| Pandas | Data organization and export |
| Matplotlib | Data visualization |
| Scikit-learn | Machine learning and digit classification |
| Scikit-image | HOG feature extraction |
| Jupyter Notebook | Development environment |

## Repository Structure

```text
thermocouple-reader/
│
├── videos/                  # Input thermocouple videos
├── digit_dataset/           # Labeled digit images (0–9)
├── test_set/                # Test images
│
├── thermocouple_digit_classifier.ipynb
├── thermocouple_digit_model.joblib
│
├── .gitignore
└── README.md
```

*Raw videos, digit datasets, and test images may be excluded from Git tracking.*

## How It Works

### 1. Video Input

The program reads a thermocouple recording and extracts individual frames at specified time intervals.

The input video path and starting timestamp can be configured in the notebook.

### 2. Frame Adjustment

Frame adjustments improve the alignment of the thermocouple display before digit recognition.

Adjustable parameters include:
- Rotation of image
- Shift x
- Shift y

### 3. Digit Dataset and Model Training

Individual digit images are collected and labeled from 0–9.

Each image is:
- Converted to grayscale.
- Resized and normalized to a consistent size.
- Converted into Histogram of Oriented Gradients (HOG) features.

A Support Vector Classifier (SVC) is trained using these features to recognize individual digits.

### 4. Display Region Selection

A calibration frame is used to select the individual digit regions for each thermocouple display.

Additional regions are selected for:
- Decimal points
- Negative signs

These coordinates are used to identify the same display regions throughout the video.

### 5. Temperature Extraction

The video is processed at regular time intervals. The classifier predicts each digit, and the predictions are combined to generate complete temperature readings.

The resulting dataset contains:

| Column | Description |
|---|---|
| `time_seconds` | Video timestamp in seconds |
| `T1_temperature` | Thermocouple 1 temperature (°C) |
| `T2_temperature` | Thermocouple 2 temperature (°C) |

### 6. Manual Data Correction

Incorrectly recognized readings can be manually corrected within the notebook.

The corrected dataset is maintained separately from the original predictions and is used for subsequent plotting and export.

### 7. Data Visualization

Temperature readings are plotted against time to visualize changes throughout the experiment.

The generated graph includes:
- Time (seconds) on the x-axis.
- Temperature (°C) on the y-axis.
- Separate temperature curves for Thermocouple 1 and Thermocouple 2.

### 8. Data Export

Extracted and corrected readings can be exported as:
- Tab-separated data for direct copying into Excel or Google Sheets.
- CSV files for additional analysis and storage.

## Model Performance and Limitations

Recognition accuracy depends on several factors:
- Video resolution and image quality.
- Display orientation and alignment.
- Lighting conditions and reflections.
- Accuracy of selected digit regions.
- Number and variety of labeled training examples.

The classifier may confuse visually similar digits, particularly when the display is unclear or partially obstructed.

Automated readings should be checked against the original video, especially when unexpected temperature changes appear.

## Future Improvements

- Improve digit recognition accuracy through additional training data.
- Improve negative sign and decimal point detection.
- Add confidence-based warnings for uncertain predictions.
- Automate thermocouple display region detection.
- Improve image processing under varying lighting conditions.
- Expand temperature data analysis and visualization.

---

## Author

Developed as an independent Biomedical Engineering and computer vision project.

**Key Areas:** Computer Vision | Machine Learning | Image Processing | Python | Data Analysis

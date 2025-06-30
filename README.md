# 📊 Spending Track

A project to track spending using Python and 2 datasets.

---

## ⚙️ Setup

### 🔁 1. Clone the Repository

Use Git to download the project from GitHub:

```bash
git clone https://github.com/phungvg/Spending-Track.git
cd Spending-Track
```
### ☁️ 2. Install Git LFS
Large files (e.g., CSVs) are managed with Git LFS.

Download and install Git LFS: git-lfs.github.com

Then run:

```bash
git lfs install
git lfs pull
```
## == IT SHOULD BE ON YOUR DEVICE FROM THIS STEP ==

## Needed Tools
### 🛠️ Install Dependencies
The project requires Python libraries, MATLAB. If requirements.txt is included:

```bash
pip install -r requirements.txt
Otherwise, install dependencies manually:
```
```bash
pip install pandas matplotlib
Ensure Python 3.x is installed: python.org
```
### ▶️ Run the Project (Work in Progress)

- [x] **Auto-Crop Receipts/Images**  
  - Best method: Morphology (region based shape detection)  
  ```matlab
  % Crop_Functions/testAutoCrop.m
  testAutoCrop

- [x] **Text Detection on Cropped Regions(Working)**
      - Extract and parse focused text areas

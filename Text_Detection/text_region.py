import cv2
import numpy as np

##Detecting text region with MSER
def detect_text_regions(img):
    """
    Detects text regions in `img` using MSER.
    Args:
        img (np.ndarray): BGR input image.

    Returns:
        vis (np.ndarray): Copy of img with detected region outlines drawn.
        text_only (np.ndarray): img masked to show only those regions.
    """
    ##Create MSER object
    # mser = cv2.MSER_create()

    ##Tuned MSER
    mser = cv2.MSER_create()
    mser.setDelta(3)
    mser.setMinArea(20)
    mser.setMaxArea(20000)
    mser.setMaxVariation(0.4)

    ##Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Detect regions in gray scale image -> list of point arrays
    regions, _ = mser.detectRegions(gray)
    
    # Build convex hulls around each region
    hulls = []
    for p in regions:
        # Reshape region points into OpenCV contour shape
        points = p.reshape(-1,1,2)
        hull = cv2.convexHull(points)
        hulls.append(hull)

    # Draw outlnes on a copy of the orginal for visualization
    vis = img.copy()
    for i in hulls:
        #isClosed = True, thickness = 2, color = green
        cv2.polylines(vis, [i], isClosed = True, color =(0, 255, 0), thickness = 2)

    ##Create a blank mask, same height/width as org img
    # mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    mask = np.zeros(gray.shape, dtype=np.uint8)

    ##Fill each hull on the mask in white(255)
    for i in hulls:
        cv2.drawContours(mask, [i], contourIdx = -1, color = 255, thickness = -1)
    
    ##Dilate to make thin strokes thicker
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    mask = cv2.dilate(mask, kernal, iterations = 1)

    ##Use the mask to extract just those regions from the original
    text_only = cv2.bitwise_and(img, img, mask = mask)

    return vis, text_only
##-----------------------------------------------------------------
##Testing 
if __name__ == "__main__":
    img = cv2.imread('/Users/panda/Documents/Work/Work_Main/Dataset_collection/Screenshot 2025-06-25 at 14.56.31.png')

    # Detect and visualize
    vis, text_only = detect_text_regions(img)

    cv2.imshow("Detected Text Regions", vis)
    cv2.waitKey(5000)

    cv2.imshow("Masked Text Only", text_only)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

    #Save results
    output_path = '/Users/panda/Documents/Work/Work_Main/spending_track/ouput'
    cv2.imwrite(f"{output_path}/detected_text_regions.png", vis)
    cv2.imwrite(f"{output_path}/masked_text_only.png", text_only)

    print("Save in output folder")
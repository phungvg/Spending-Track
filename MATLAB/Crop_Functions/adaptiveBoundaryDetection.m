function boundaryMask = adaptiveBoundaryDetection(grayImg, threshold)
% ADAPTIVEBOUNDARYDETECTION - Adaptive method combining multiple approaches
%
% Inputs:
%   grayImage - Grayscale input image
%   threshold - Threshold value for various methods
%
% Output:
%   boundaryMask - Binary mask of detected boundaries

    % Method 1: Canny edges
    mask1 = cannyBoundaryDetection(grayImg, threshold);
    
    % Method 2: Morphological processing
    mask2 = morphologyBoundaryDetection(grayImg, threshold);
    
    % Method 3: Variance-based detection
    H = fspecial('average', [9 9]);
    localMean = imfilter(grayImg, H, 'replicate');
    localVar = imfilter((grayImg - localMean).^2, H, 'replicate');
    
    varThresh = threshold * max(localVar(:));
    mask3 = localVar > varThresh;
    
    % Combine masks using voting (at least 2 out of 3 methods agree)
    combinedMask = (mask1 + mask2 + mask3) >= 2;
    
    % Final processing
    se = strel('disk', 3);
    boundaryMask = imopen(combinedMask, se);
    boundaryMask = imclose(boundaryMask, se);
    boundaryMask = imfill(boundaryMask, 'holes');
end
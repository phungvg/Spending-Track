function boundaryMask = sobelBoundaryDetection(grayImg, threshold)
% SobelBoundaryDetection - Sobel gradient-based boundary detection
%
% Inputs:
%   grayImage - Grayscale input image
%   threshold - Threshold value (0 for automatic)
%
% Output:
%   boundaryMask - Binary mask of detected boundaries

    % Sobel gradient-based detection
    [Gx, Gy] = gradient(double(grayImg));
    gradMag = sqrt(Gx.^2 + Gy.^2);
    
    % Adaptive threshold if not specified
    if threshold == 0
        threshold = graythresh(gradMag);
    else
        threshold = threshold * max(gradMag(:));
    end
    
    boundaryMask = gradMag > threshold;
    
    % Morphological operations
    se = strel('disk', 3);
    boundaryMask = imclose(boundaryMask, se);
    boundaryMask = imfill(boundaryMask, 'holes');
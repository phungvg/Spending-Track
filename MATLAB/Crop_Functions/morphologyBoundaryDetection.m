function boundaryMask = morphologyBoundaryDetection(grayImg, threshold)
% morphologicalBoundaryMask - Enhanced morphological boundary detection
%
% Inputs:
%   grayImg - Grayscale input image
%   threshold - Threshold value (0 for automatic)
%
% Output:
%   boundaryMask - Binary mask of detected boundaries

    % 1. Contrast enhancement
    enhancedImage = adapthisteq(grayImg);
    
    % 2. Top-hat filtering to enhance bright regions
    se1 = strel('disk', 15);
    tophat = imtophat(enhancedImage, se1);
    
    % 3. Bottom-hat filtering to enhance dark regions
    bothat = imbothat(enhancedImage, se1);
    
    % 4. Combine enhancements
    enhanced = enhancedImage + tophat - bothat;
    
    % 5. Binarization
    if threshold == 0
        level = graythresh(enhanced);
    else
        level = threshold;
    end
    
    boundaryMask = imbinarize(enhanced, level);
    
    % 6. Advanced morphological processing
    se2 = strel('disk', 5);
    boundaryMask = imopen(boundaryMask, se2);  % Remove noise
    boundaryMask = imclose(boundaryMask, se2); % Close gaps
    boundaryMask = imfill(boundaryMask, 'holes'); % Fill holes
end
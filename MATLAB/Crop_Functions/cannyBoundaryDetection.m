function boundaryMask = cannyBoundaryMask(grayImg, threshold)

% Inputs:
%   grayImg - Grayscale input image
%   threshold - Threshold value (0 for automatic)
%
% Output:
%   boundaryMask - Binary mask of detected boundaries

% threshold value = 0 -> let MATLAB pick
threshold_values = 0;
radius = 2;
    if threshold == threshold_values
        boundary = edge(grayImage, 'canny');
    else
        % edge(grayImg, 'canny',[low,high]
        boundary = edge(grayImg, 'canny', [threshold * 0.5,threshold]);
    end

    % Fill regions to create solid boundaries
    se = strel('disk',radius);
    boundary = imclose(boundary, se);
    boundaryMask = imfill(boundary, 'holes');
end
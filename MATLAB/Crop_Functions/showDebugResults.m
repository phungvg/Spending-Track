function showDebugResults(originalImage, grayImage, boundaryMask, boundingBox, method)
% SHOWDEBUGRESULTS - Visualization for debugging boundary detection
%
% Inputs:
%   originalImage - Original input image
%   grayImage - Grayscale version of input
%   boundaryMask - Detected boundary mask
%   boundingBox - Computed bounding box [x, y, width, height]
%   method - Detection method used (string)

    figure('Name', ['Boundary Detection Debug - ' method], 'Position', [100, 100, 1200, 800]);
    
    % Original image
    subplot(2, 3, 1);
    imshow(originalImage);
    title('Original Image');
    
    % Grayscale
    subplot(2, 3, 2);
    imshow(grayImage);
    title('Grayscale');
    
    % Boundary mask
    subplot(2, 3, 3);
    imshow(boundaryMask);
    title('Boundary Mask');
    
    % Original with bounding box
    subplot(2, 3, 4);
    imshow(originalImage);
    hold on;
    rectangle('Position', boundingBox, 'EdgeColor', 'r', 'LineWidth', 2);
    title('Detected Boundary');
    
    % Cropped result
    subplot(2, 3, 5);
    croppedImg = originalImage(boundingBox(2):boundingBox(2)+boundingBox(4)-1, ...
                              boundingBox(1):boundingBox(1)+boundingBox(3)-1, :);
    imshow(croppedImg);
    title('Cropped Result');
    
    % Overlay
    subplot(2, 3, 6);
    overlayImg = imoverlay(mat2gray(grayImage), boundaryMask, 'red');
    imshow(overlayImg);
    title('Boundary Overlay');
    
    % Print bounding box info
    fprintf('Method: %s\n', method);
    fprintf('Bounding Box: [x=%d, y=%d, width=%d, height=%d]\n', boundingBox);
    fprintf('Original size: %dx%d, Cropped size: %dx%d\n', ...
            size(originalImage,1), size(originalImage,2), boundingBox(4), boundingBox(3));
end
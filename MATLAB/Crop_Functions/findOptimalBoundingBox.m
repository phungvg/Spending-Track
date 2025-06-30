function boundingBox = findOptimalBoundingBox(boundaryMask, imageSize, padding)
% FINDOPTIMALBOUNDINGBOX - Find the optimal bounding box with padding
%
% Inputs:
%   boundaryMask - Binary boundary mask
%   imageSize - Size of the original image [height, width]
%   padding - Padding around detected boundary (pixels)
%
% Output:
%   boundingBox - Bounding box in format [x, y, width, height]

    [rows, cols] = find(boundaryMask);
    
    if isempty(rows)
        % If no boundary found, return full image
        boundingBox = [1, 1, imageSize(2), imageSize(1)];
        return;
    end
    
    minRow = max(1, min(rows) - padding);
    maxRow = min(imageSize(1), max(rows) + padding);
    minCol = max(1, min(cols) - padding);
    maxCol = min(imageSize(2), max(cols) + padding);
    
    % Format: [x, y, width, height]
    boundingBox = [minCol, minRow, maxCol - minCol + 1, maxRow - minRow + 1];
end
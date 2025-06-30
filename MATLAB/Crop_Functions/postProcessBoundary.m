function cleanMask = postProcessBoundary(boundaryMask, minArea)
% POSTPROCESSBOUNDARY - Remove small components and clean up the mask
%
% Inputs:
%   boundaryMask - Binary boundary mask
%   minArea - Minimum area to consider as valid boundary
%
% Output:
%   cleanMask - Cleaned binary mask

    % Remove small connected components
    cleanMask = bwareaopen(boundaryMask, minArea);
    
    % Keep only the largest connected component
    CC = bwconncomp(cleanMask);
    if CC.NumObjects > 1
        areas = cellfun(@length, CC.PixelIdxList);
        [~, maxIdx] = max(areas);
        
        largestMask = false(size(cleanMask));
        largestMask(CC.PixelIdxList{maxIdx}) = true;
        cleanMask = largestMask;
    end
    
    % Smooth the boundary
    se = strel('disk', 2);
    cleanMask = imopen(cleanMask, se);
    cleanMask = imclose(cleanMask, se);
end
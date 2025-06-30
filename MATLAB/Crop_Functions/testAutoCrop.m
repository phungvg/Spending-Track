% testAutoCrop.m
% Basic usage
img = imread('/Users/panda/Documents/Work/Work_Main/Dataset_collection/Collection 1/Screenshot 2025-06-30 at 16.05.20.png');

[croppedImg, bbox] = autoCrop(img);

% With specific method and parameters
[croppedImg, bbox] = autoCrop(img, 'Method', 'morphology', ...
                                      'Threshold', 0.15, 'Padding', 20, ...
                                      'Debug', true);

% Run the demo using the standalone function
runBoundaryDetectionDemo();  
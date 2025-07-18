% function runBoundaryDetectionDemo()
% % RUNBOUNDARYDETECTIONDEMO - Standalone demo for boundary detection
%% Test 1: Basic usage with your image
try
    img = imread('/Users/panda/Documents/Work/Work_Main/Dataset_collection/Collection 1/Screenshot 2025-06-30 at 16.05.20.png');
    fprintf('Image loaded successfully. Size: %dx%dx%d\n', size(img));
    
    % Basic auto-crop
    [croppedImg, bbox] = autoCrop(img);
    
    % Display results
    figure('Name', 'Basic Auto Crop', 'Position', [100, 100, 800, 400]);
    subplot(1,2,1);
    imshow(img);
    hold on;
    rectangle('Position', bbox, 'EdgeColor', 'r', 'LineWidth', 2);
    title('Original with Detected Boundary');
    
    subplot(1,2,2);
    imshow(croppedImg);
    title('Cropped Result');
    
    fprintf('Bounding box: [x=%d, y=%d, w=%d, h=%d]\n', bbox);
    
catch ME
    fprintf('Error loading image: %s\n', ME.message);
    fprintf('Using synthetic image instead...\n');
    img = createTestImage();
end

%% Test 2: Different methods comparison
fprintf('\nTesting different detection methods...\n');

% Test different methods
methods = {'canny', 'sobel', 'morphology', 'adaptive'};

figure('Name', 'Method Comparison', 'Position', [200, 200, 1200, 800]);

for i = 1:length(methods)
    fprintf('Testing %s method...\n', methods{i});
    
    [croppedImg, bbox] = autoCrop(img, 'Method', methods{i}, 'Debug', false);
    
    subplot(2, 4, i);
    imshow(img);
    hold on;
    rectangle('Position', bbox, 'EdgeColor', 'r', 'LineWidth', 2);
    title(sprintf('%s - Detection', methods{i}));
    
    subplot(2, 4, i+4);
    imshow(croppedImg);
    title(sprintf('%s - Cropped', methods{i}));
end

%% Test 3: Morphology method with debug
fprintf('\nTesting morphology method with debug visualization...\n');

[croppedImg, bbox] = autoCrop(img, 'Method', 'morphology', ...
                                      'Threshold', 0.15, 'Padding', 20, ...
                                      'Debug', true);

%% Test 4: Parameter sensitivity test
fprintf('\nTesting different thresholds...\n');

thresholds = [0.05, 0.1, 0.2, 0.3];
figure('Name', 'Threshold Sensitivity', 'Position', [300, 300, 1000, 600]);

for i = 1:length(thresholds)
    [croppedImg, bbox] = autoCrop(img, 'Method', 'morphology', ...
                                          'Threshold', thresholds(i), 'Debug', false);
    
    subplot(2, 4, i);
    imshow(img);
    hold on;
    rectangle('Position', bbox, 'EdgeColor', 'r', 'LineWidth', 2);
    title(sprintf('Threshold = %.2f', thresholds(i)));
    
    subplot(2, 4, i+4);
    imshow(croppedImg);
    title('Cropped');
end

fprintf('Testing complete!\n');

%% Helper function to create test image
function testImg = createTestImage()
    % Create a test image similar to your morphological processing example
    testImg = zeros(400, 500, 3);
    
    % Create some diagonal patterns (like in your image)
    [X, Y] = meshgrid(1:500, 1:400);
    pattern = sin(0.1*X + 0.05*Y) + cos(0.08*X - 0.06*Y);
    
    % Add the pattern to create texture
    testImg(:,:,1) = 0.5 + 0.3*pattern;
    testImg(:,:,2) = 0.4 + 0.2*pattern;
    testImg(:,:,3) = 0.3 + 0.1*pattern;
    
    % Add a clear boundary region
    testImg(100:300, 150:350, :) = testImg(100:300, 150:350, :) + 0.4;
    
    % Normalize
    testImg = max(0, min(1, testImg));
    
    fprintf('Created synthetic test image with diagonal patterns\n');
end
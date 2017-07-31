coverage = (0.1 : 0.1 : 1);
width = 1500;
height = 800;
pattern = uint8(255 * genPattern(height, width));
w = 50; % black and white strip combined
i = 1;
if ~exist('texture01_10', 'file')
    mkdir('texture01_10');
end
for c = coverage
    mask = ones(height, width, 'uint8');
    wW = w * c;
    bW = w - wW;
    nstrip = floor(width / w);
    col = 1 + (0 : w : width - w);
    col = repmat(col, bW, 1);
    inc = (0 : bW - 1)';
    col = col + repmat(inc, 1, nstrip);
    pattern_i = pattern;
    pattern_i(:, col, :) = 255;
    imwrite(pattern_i, sprintf('texture01_10/%02d.jpg', i));
    i = i + 1;
end
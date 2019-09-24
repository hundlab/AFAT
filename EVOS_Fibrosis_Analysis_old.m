%% Automated Fibrosis Analysis Tool for EVOS Images

% Written by Alyssa Dalic on 2/02/18
% Last Edited on 2/02/18 by Alyssa Dalic

% This script file will calculate the amount of fibrosis in a histological
% section of a mouse heart from an image taken of the heart by the EVOS
% microscope.

%% Initialize
clc;
clear all;
close all;

%% Upload image into MATLAB for analysis
% Please select "all files"  in the lower right corner of the window to
% select the file containing the image you want analyzed.
filename = uigetfile('','Blue Fibrosis');
RGBO=imread(filename);
%% Display orginal image
figure;
RGBO=RGBO(:,:,1:3);
imshow(RGBO);
title(filename);

%% Orignal histogram
% Split orignal image into red, blue and green channels
RO=RGBO(:,:,1);
GO=RGBO(:,:,2);
BO=RGBO(:,:,3);
% Plot all 3 histograms on the same figure
figure;
subplot(3,1,1);
imhist(RO);
title('Histogram of Original Image');
subplot(3,1,2);
imhist(GO);
subplot(3,1,3);
imhist(BO);

%% Perform histogram matching with a master image
% Ask user if they want hostogram matching to be performed. Histogram
% matching equalizes the histograms of one image to match those of another. This can be used when two images have different quality to ensure analysis is consistent. 
hmcheck=input('Do you want to perform histogram matching? Enter yes or no: ','s');

if strcmp(hmcheck,'yes') || strcmp(hmcheck,'Yes')
    % read in master image
    filename2 = uigetfile('','Master Image');
    RGBM=imread(filename2);
    % Histogram matching
    RGB=imhistmatch(RGBO,RGBM);
    % Display equalized image
    figure;
    imshow(RGB);
    title('Equalized image');
    % Split orignal image into red, blue and green channels
    RM=RGBM(:,:,1);
    GM=RGBM(:,:,2);
    BM=RGBM(:,:,3);
    % Histogram for each channel
    % Plot all 3 histograms on the same figure
    figure;
    subplot(3,1,1);
    imhist(RM);
    title('Histogram of the Master Image');
    subplot(3,1,2);
    imhist(GM);
    subplot(3,1,3);
    imhist(BM);
    % Split orignal image into red, blue and green channels
    R=RGB(:,:,1);
    G=RGB(:,:,2);
    B=RGB(:,:,3);
    % Histogram for each channel
    % Plot all 3 histograms on the same figure
    figure;
    subplot(3,1,1);
    imhist(R);
    title('Histogram of Original Image after Matching');
    subplot(3,1,2);
    imhist(G);
    subplot(3,1,3);
    imhist(B);
else
    RGB=RGBO;
end

%% Convert images from RGB colorspace to L*a*b
% L*a*b colorspace is needed to do segmentation with K-means
lab=rgb2lab(RGB);

%% Use K-mean clustering to sort colors in the a*b  space
% Grab a*b data from image
abdata = double(lab(:,:,2:3));
abrows= size(abdata,1);
abcolumns= size(abdata,2);
abdata=reshape(abdata,abrows*abcolumns,2);
Colors=2;
% Calculate K-means for clustering.  Repeat K-means clustering 6 times to
% ensure correct color separation
[index,center]=kmeans(abdata,Colors,'distance','sqEuclidean','Replicates',6);

% Label each pixel in each image with its index calculated from Kmeans
pixellabel=reshape(index,abrows,abcolumns);

%% Create Segmented Images by Color
% Create cells that will hold segmented data to plot
segmented=cell(1,2);

% Convert labels to RGB to display segmented images
rgbseg=repmat(pixellabel,[1,1,3]);

% Segment data based on clustering
for i=1:Colors
    color=RGB;
    color(rgbseg~=i)=0;
    segmented{i}=color;
end

% Separate out red cluster using cluster means
meancluster = mean(center,2);
[tmp, idx] = sort(meancluster);
% This number may need to be changed.  Try numbers 1-3.
rednum = idx(1);
redcluster=segmented{rednum};
figure;
imshow(redcluster);
title('Red Segment: Cells');

%% Color Thresholder App for noise removal
[BWfib, YCCK]=EVOS_Mask(RGB);
% Display final image
figure;
imshow(YCCK);
title(filename);

%% Calculate area of Fibrosis or blue/purple regions
% Area should represent the total number of pixels that are a part of
% fibrosis.  This will be a rough estimate because pixels are weighted
% differently based on the pixels surrounding it.

% To calculate the area this way, images need to be in binary because it
% calculates the number white or "on" pixels

% Calculate area of fibrosis
areafib=bwarea(BWfib)

% Convert red segments to binary images
redgreyscale = rgb2gray(redcluster);
imshow(redgreyscale)
BWred = imbinarize(redgreyscale);

% Calculate the area of the red pixels
areared=bwarea(BWred)

% Total number of pixels per image
[x,y,z]=size(RGB);
Totalpixels=x*y;

% Percent fibrosis and percent red (compared to total image)
pfib=(areafib/Totalpixels)*100;
pred=(areared/Totalpixels)*100;

% Percent fibrosis vs. Red
pfibvred=(areafib/(areared+areafib))*100;
PercentFibrosisRed='The percent fibrosis in relation to the red tissue is %f \n';
fprintf(PercentFibrosisRed,pfibvred);
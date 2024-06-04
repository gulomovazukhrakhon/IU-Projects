# Problem Statement
According to the World Health Organization, each year approximately 1,19 million people die due to road accidents. Children and young adults aged 5-29 are more likely to die because of road traffic injuries. Speeding is one of the main risk factors for road crashes so predicting high speed is crucial (World Health Organization: WHO, 2023). 

# Goals and Objectives
I developed a speed-tracking system that detects cars on a highway and estimates their speed over time. My task involves triggering an alert if a vehicle exceeds a predefined speed limit. To accomplish this, I compared three state-of-the-art algorithms such as YOLOv8, SSD, and Faster R-CNN for car detection and tracking, assessing their accuracy, and evaluating their impact on speed prediction. I plan to implement the system using Python programming language, along with computer vision frameworks and open-source libraries. 

## YOLOv8
YOLOv8 is the latest version of the real-time object detection and tracking model and offers unparalleled performance in terms of speed and accuracy. It is suitable for various applications including vehicle tracking and is adaptable to different hardware platforms (YOLOv8, 2023).

## Faster R-CNN
Faster RCNN is a two-stage object detector, and it is dependent on region proposal algorithms. It consists of two models: deep convolutional neural networks that propose regions and a Fast RCNN detector that uses the proposed regions (Ren et al., 2015). It is known for its high accuracy but tends to be slower than SSD and YOLOv8.

## SSD
A Single-Shot-Detector (SSD) approach is based on a feed-forward convolutional network that predicts category scores and box offsets for a fixed set of default bounding boxes (Liu et al., 2016). It offers a good trade-off between speed and accuracy. 

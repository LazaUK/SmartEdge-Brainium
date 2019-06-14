# SmartEdge Agile: API data Retrieval and Upload into Azure IoT Hub + Stream Analytics for Anomaly Detection
## Pre-requisites:
- You should have access to SmartEdge Agile from [AVNet](https://www.avnet.com/wps/portal/us/solutions/iot/building-blocks/smartedge-agile)
- You should train the model in [Brainium portal](https://www.brainium.com/) and deploy them to SmartEdge Agile device;
- You should also have smartphone or Raspberry Pi with Brainium Gateway app installed to enable data streaming from device over to the portal
## High-Level Architecture
This is high-level architecture with all the main blocks of the target solution.
![ha-architecture](Brainium_Schematics.png)
Training motion recognition and sync into Brainium portal is one of the pre-requisites. To learn more about that process, please refer to the Brainium [documentation](https://www.brainium.com/gesture-control)
Partes below will describe how to enable MQTT client to retrieve data, upload it into Azure IoT Hub and the use scripting within Azure Stream Analytics to detect anomalies.
## MQTT Client
x
x
x
x
x
x
## Azure Stream Analytics
Setup new instance of ASA, add your IoT Hub as an input (in this code called "MyStream") and PowerBI as an output (in this code - "MyBI") to define data flow.
Then copy-paste the following SQL script into ASA's query section. It would learn from the last 120 patterns of the motions in 2 min windows and provide you with it's scoring and indication of the possible anomalies. Again, as an example here we look at both peaks and drops.
![asa-sql](ASA_SmartEdge.sql)
For the provided scenario, drops can be characterised as unintended gestures from the quality control staff if the probability guess at the edge is relatively low comparing to the previous examples.
Another scenario which can be enabled here using "AnomalyDetection_ChangePoint" function, which would detect increase in the number of defects identified and thus trigger an alarm, indicating significant drop in the production output's quality, highlighting potential issue with the monitored equipment.
## PowerBI Dashboard
Once you get data in PowerBI, you can create a new report and publish it in a dashboard.
![pbi-dashboard](PowerBI_Dashboard.png)
This results shows the motions detected overtime, and detect anomalies in the peaks and drops.
## Working model
You can find short demo of working solution here on [YouTube](https://youtu.be/n5GvrZQTSfs)

# Smart Transit Real-Time Analytics

A cutting-edge platform that repurposes existing hardware—from agency, city, and government cameras—to deliver real-time public transit analytics. Our solution leverages privacy-preserving object detection to count passengers (without recording personal identities) and processes these counts via a distributed pipeline. Imagine a city like Edmonton tracking bus ridership across 900+ buses in real time to optimize transit operations and resource allocation.

![image](https://github.com/user-attachments/assets/57affe4f-895a-4967-8437-2267afe41276)
Youtube Demo: https://youtu.be/CI5sKFSr3U4
---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Benefits](#benefits)
- [Usage](#usage)

---

## Overview

Smart Transit Real-Time Analytics transforms existing camera infrastructure into a powerful tool for modern urban management. By implementing state-of-the-art machine learning models for object detection (focused solely on counting objects to maintain privacy), we provide actionable insights through a fully distributed, real-time pipeline. Our system empowers cities and transit agencies to:

- **Optimize Resources:** Deploy more buses in high-demand areas.
- **Improve Traffic Strategies:** Develop data-driven strategies for smoother traffic flow.
- **Enhance Emergency Response:** Monitor passenger volumes to trigger timely alerts and updates.

---

## Features

- **Real-Time Data Pipeline:** 
  - Ingests live video feeds from cameras installed on buses, trains, or public spaces.
  - Leverages **OpenCV** to simulate frame transmission to Kafka Topics.
- **Privacy-Preserving Object Detection:** 
  - Only counts individuals without storing or transmitting personal data.
  - Detect and estimate transit occupancy using a **YOLOv8 ML** object detection model.
- **Distributed Processing:**
  - Utilizes **[Confluent Apache Kafka](https://www.confluent.io/product/kafka-streaming-platform/)** for data streaming.
  - Processes streams with **[Confluent Apache Flink](https://flink.apache.org/)** for real-time analytics.
- **Scalable Dashboard:**
  - Feeds real-time insights to dynamic dashboards, enabling instant visualization.
  - Uses **Django**, **PostgreSQL**, and **HTML & CSS** to power our APIs, databases, and front-end dashboard.
- **Containerized Deployment:**
  - Uses **Docker** Compose to containerize and simplify our deployment.

---

## Architecture

> **Diagram (Conceptual):**

```mermaid
flowchart LR
    A[Camera Feeds] --> B[Apache Kafka]
    B --> C[Apache Flink]
    C --> D[ML Object Detection]
    D --> E[PostgreSQL DB]
    E --> F[Dashboard & Analytics]
```
1. **Camera Feeds:**  
   Existing hardware captures video streams from transit vehicles or public areas.
   
2. **Data Ingestion via Apache Kafka:**  
   Streams video data into a Kafka cluster, ensuring high-throughput and fault-tolerant delivery.

3. **Real-Time Processing with Apache Flink:**  
   Processes data in real time to run ML object detection models, extracting counts from video frames.

5. **Dashboard Integration:**  
   Processed data is fed into dashboards to display live transit statistics and insights.

## Technologies

### Data Streaming & Processing
- **Confluent Apache Kafka**
- **Confluent Apache Flink**

### Machine Learning & Object Detection
- **ML frameworks:** YOLOv8
- **Computer vision libraries:** OpenCV

### Containerization & Orchestration
- **Docker**

### Visualization & Storage
- **Real-time Django Dashboards**
- **PostgreSQL databases** for efficient data storage

---

## Benefits

Our platform offers a broad range of benefits that extend well beyond simple transit monitoring:

- **Extended Hardware Lifespan & Maximized ROI:**  
  Use existing camera infrastructure to extract new value, maximizing the return on previous investments and reducing the need for new capital expenditures.

- **Operational Efficiency:**  
  Real-time insights empower transit agencies to adjust schedules and routes dynamically, reducing wait times and ensuring optimal resource allocation.

- **Resource Optimization:**  
  Identify high-demand areas and peak usage times to strategically allocate buses, trains, and other transit assets, thereby improving service efficiency and reducing operational costs.

- **Enhanced Traffic Management:**  
  Utilize real-time data to develop dynamic traffic strategies, alleviate congestion, and improve overall urban mobility.

- **Data-Driven Policy Making:**  
  Provide city planners and decision-makers with actionable, real-time data to inform long-term transit strategies and urban planning initiatives.
  
- **Enhanced Public Safety and User Experience:**  
  Real-time monitoring ensures rapid decision-making during emergencies and enhances overall rider satisfaction through improved transit efficiency.

- **Seamless Integration with Smart City Initiatives:**  
  Integrate with broader smart city frameworks, supporting initiatives like adaptive traffic control, smart parking, and comprehensive urban planning dashboards.

- **Customizable Analytics and Reporting:**  
  Offer flexible analytics and reporting tools that can be tailored to the specific needs of different agencies, ensuring that insights are both relevant and actionable.

---

## Usage

- **Ingesting Data:**  
  Direct camera feeds are ingested through the Kafka pipeline.

- **Processing:**  
  Apache Flink runs ML object detection models in real time, producing count data.


## Optimization Strategies

To further enhance real-time analytics and improve decision-making, our platform incorporates several optimization techniques:

### **1. WebSocket Subscription for Real-Time Updates**  
- Instead of relying solely on periodic API polling, the frontend subscribes to an **Apache Kafka topic via a WebSocket connection**.  
- This ensures that updates on passenger counts, bus occupancy, and traffic conditions are **instantly pushed** to the dashboard, reducing latency and improving responsiveness.

### **2. Display Anonymized Images for Contextual Insights**  
- To provide **visual verification** without compromising privacy, the system can display **blurred, anonymized images** next to live dashboard analytics.  
- This feature allows transit agencies to **validate passenger counts** and identify **potential operational issues**, such as overcrowding or improper seating distribution.  
- The anonymization ensures compliance with data privacy laws while **enhancing situational awareness**.

### **3. Live Bus Tracking with Data Overlay**  
- **GPS integration** allows for real-time tracking of each bus, displaying its exact location on a city map.  
- Overlaying **real-time passenger load** on each tracked vehicle enables better routing and **adaptive scheduling**, ensuring optimized resource allocation.

### **4. Spatial Fragmentation Analysis for Improved Bus Utilization**  
- Instead of treating the entire bus as a single occupancy metric, our system applies **spatial fragmentation** by segmenting the vehicle into multiple sections (e.g., front, middle, back).  
- Each section’s occupancy is analyzed separately, allowing for:
  - Identification of **underutilized spaces** within the bus.
  - Adjustments to **seating arrangements** for better passenger distribution.
  - Recommendations for **dynamic bus design** optimizations based on usage patterns.
  
### **5. Government & Policy Recommendations**  
- The insights generated from **spatial fragmentation, real-time occupancy, and traffic flow data** provide governments with the ability to:
  - Develop **better public transportation policies**.
  - Implement **targeted infrastructure improvements**.
  - Justify budget allocations for **fleet expansion or reallocation**.
  - Introduce **incentive programs** to distribute passenger load across different hours or routes.


# System-Comprehensive-Exercise-Deliverables
Weather and Weather-related Disease Prediction System

Motivation
- Aizu-Wakamatsu is a basin area, and the weather forecast and actual weather often differ.
- To estimate the degree of weather-related illnesses caused by changes in atmospheric pressure.

Purpose
Connecting atmospheric pressure sensor module and using the measured data and data from the website,
weather forecast and alert level for weather-related diseases.
weather forecast and warning level for weather-related illnesses.

Operation flow 
Update every 30 minutes by Cron (scheduler)
- Obtain date and time data
- Obtain data from barometric sensor module
- Obtain atmospheric pressure data from website
- Forecasting Weather and Weather-related Diseases
- Display on LCD display

Devices used
- Raspberry Pi 3
- BMP180 (atmospheric pressure sensor module)
- LCD display
- Breadboard
- Jump wire
- T-type expansion board

Creative points in my work 
- Using API to read data from a website
- Use of scheduler with Cron

References
- Osoyoo, "Rasberry Pi Starter Kit Part 18: Running a BMP180 Digital Barometric Pressure Sensor on a Raspi," https://osoyoo.com/ja/2017/07/06/bmp180_ pressure-sensor/
- SAITO Hiroshi, KOHIRA Yukihide, JING Lei, LE Doan Hoang, "Integrated Exercise for Systems I 3. Control of Sensors and Actuators Using GPIOs", 2023
- SAITO Hiroshi, KOHIRA Yukihide, JING Lei, LE Doan Hoang, "Integrated Exercise for Systems I 4. GPIOs", 2023

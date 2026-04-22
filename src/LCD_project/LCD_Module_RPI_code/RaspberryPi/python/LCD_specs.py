#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys
import time
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch
from PIL import Image, ImageDraw, ImageFont
import socket
from datetime import datetime
import psutil
import subprocess

disp = LCD_2inch.LCD_2inch()
disp.Init()
disp.bl_DutyCycle(50)  # Set backlight

while True:
    try:
        # Create blank image for drawing
        image = Image.new("RGB", (disp.height, disp.width), (0, 0, 0))  # BLACK
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("/home/(user)/FitTrack/src/LCD_project/LCD_Module_RPI_code/RaspberryPi/python/Font/Font00.ttf", 23)

        # Display date and time
        draw.text((1, 12), str(datetime.now().strftime('%a  %b  %d  %H:%M:%S')), fill=(255, 255, 0), font=font)

        # Display CPU temperature
        def cpu_temp():
            tempF = (((int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1000) * 9/5) + 32)
            return f"CPU TEMP: {round(tempF, 2)}F"

        draw.text((1, 52), cpu_temp(), fill=(0, 255, 255), font=font)

        # Display IP address
        def wlan_ip():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                return f"IP: {ip}"
            except:
                return "No IP Found"

        draw.text((1, 92), wlan_ip(), fill=(0, 255, 255), font=font)

        # Display disk usage
        def disk_usage(dir):
            usage = psutil.disk_usage(dir)
            return f"SD CARD USE: {usage.percent:.0f}%"

        draw.text((1, 132), disk_usage('/'), fill=(0, 255, 255), font=font)

        # Display memory usage
        def memory_usage():
            usage = subprocess.check_output("free -m | awk '/^Mem:/{print $3/$2*100; exit}'", shell=True).decode().strip()
            usage = round(float(usage))
            return f"MEMORY USE: {usage}%"

        draw.text((1, 172), memory_usage(), fill=(0, 255, 255), font=font)

        # Rotate and show image
        rotated_image = image.rotate(270, expand=True)
        disp.ShowImage(rotated_image)
        time.sleep(10)

    except KeyboardInterrupt:
        disp.module_exit()
        sys.exit()
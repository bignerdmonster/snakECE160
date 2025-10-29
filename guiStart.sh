#!/usr/bin/env bash
set -e

echo "Installing dependencies..."
#sudo apt-get update -y
sudo apt-get install -y xvfb x11vnc fluxbox websockify novnc
sudo rm -rf /tmp/.X1-lock
sudo service x11-common stop
echo "Starting virtual display..."
Xvfb :1 -screen 0 1024x768x24 &
export DISPLAY=:1
fluxbox &

echo "Starting VNC server..."
x11vnc -display :1 -nopw  -shared -rfbport 5900 &

echo "Starting noVNC on port 6080..."
websockify --web=/usr/share/novnc 6080 localhost:5900 &

echo ""
echo "GUI environment is ready!"
echo "Go to the Ports tab, set port 6080 to Public, and open the link."
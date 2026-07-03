#!/bin/bash
apt-get update
apt-get install -y zlib1g-dev libjpeg-dev python3-dev build-essential
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
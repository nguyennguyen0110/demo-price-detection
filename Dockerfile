# syntax=docker/dockerfile:1
# Specify base image
FROM ubuntu:22.04

# Tell docker the port to use
EXPOSE 8080

# Install Python, pip and Tesseract
RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    apt-get install -y tesseract-ocr

# Install dependencies
# DO NOT install torch higher version because it use C++ 17 while mmcv use C++ 14
RUN pip3 install ninja==1.11.1 && \
    pip3 install psutil==5.9.7 && \
    pip3 install Pillow==9.4.0 && \
    pip3 install numpy==1.23.5 && \
    pip3 install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu && \
    pip3 install openmim==0.3.9

RUN mim install mmengine==0.10.2 && \
    mim install mmcv-lite==2.1.0 && \
    mim install mmdet==3.2.0 && \
    mim install mmocr==1.0.1

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy trained model
COPY model/vie_price_tag.traineddata  /usr/share/tesseract-ocr/4.00/tessdata/
# Copy all files from source to container directory
COPY . .

# The command to run when start docker image
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "-t", "120", "app:app"]

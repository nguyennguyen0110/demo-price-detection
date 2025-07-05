# Demo Price Detection


## Description
This project is demo version for Price Detection project


## Installation
- Install docker, vary depend on the OS, check https://docs.docker.com/engine/install/
- Build docker image (may need admin or sudo prefix), note that there is dot at the end. You can 
change the image name and version to your own need:
    
        docker build -t image_name:version .
- Run container with the image created, change docker port and app port to the actual port used:
    
        docker run -p 127.0.0.1:docker_port:app_port image_name:version

## Support
nguyennta@icloud.com


## Contributing
Project structure:
- static: contain static file such as css, images.
- templates: contain html file.
- app.py: main file to run this project (Flask application is created here).
- Dockerfile: file used to containerize this project with docker.
- README.md: this project instruction file.
- requirements.txt: file contain the dependencies that need to install.


## Authors
This project is done by nguyennta@icloud.com


## License
This is a demo project for portfolio page.


## Project status
- Working
- Current host: https://demo-price-detection-698202522757.asia-southeast1.run.app
- This project’s source code is hosted on GitHub, with CI/CD handled by Cloud Build 
and deployed via Cloud Run — both part of Google Cloud Platform (GCP).


## Details


### Feature:  
Read texts from image, get product name and selling price.


### Image requirements
- For more accuracy, the image should include only one tag and all the characters 
are visible. The image quality should be good and texts are straight.
- Recommend the tag location should be on top of the image because model is 
currently reading from top to bottom. And it will read all the texts in image, 
so it is better to have only the tag in the image.


### Known issues
The model is for demo only, its accuracy is not perfect.


### Applied logic
Read all texts, choose the first line (on top) as product name and the number 
which has largest printed area as selling price.

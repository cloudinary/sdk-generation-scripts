# SDK Generation Scripts

This repository contains all the scripts, templates and guidelines 
for the SDK generation of the Cloudinary OpenAPI based services.

Adding a new langauge

* Clone this repo
* Enter repo directory
* Clone `git@github.com:CloudinaryLtd/service_interfaces.git`
* Configure environment:
* Set the following environment variables(you can change the actual values depending on your needs):
  * YML=service_interfaces/media-delivery/schema.yml
  * OPEN_API_GEN=openapi-generator
  * SDKS=nodejs
* run:
* python3 main.py

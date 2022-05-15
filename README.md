# SDK Generation Scripts

This repository contains all the scripts, templates and guidelines 
for the SDK generation of the Cloudinary OpenAPI based services.

Adding a new langauge

* Clone this repo
* Enter repo directory
* Clone `git@github.com:CloudinaryLtd/service_interfaces.git`
* Configure environment:
* Set the following environment variables(you can change the actual values depending on your needs):
  * `YML=service_interfaces/media-delivery/schema.yml`
  * `OPEN_API_GEN=openapi-generator`
  * `SDKS=nodejs`
Install:
* `pip3 install pyyaml`
* `brew install openapi-generator`
Run: `python3 main.py`


Customizing and configuring a new SDK

* Open the resulting generated folder in your IDE (for example media_delivery_java)
* Get your templates by running `openapi-generator author template -g {put your language here} --library webclient`
* To customize a template, just copy the relevant file to `templates/{your language}` folder and edit.
* Variables inside templates can be set by adding `configs/{your language}/config.yml`. 
Some of those variables should be prepopulated/pregenrated.
It will be done in the future, please notify the maintainer of this project for feature requests.

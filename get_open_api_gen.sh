#!/usr/bin/env bash

# set the default value for OPEN_API_GEN_URL, or use the one that was defined before
: "${OPEN_API_GEN_URL:=https://oss.sonatype.org/service/local/repositories/snapshots/content/com/cloudinary/openapi-generator-project/6.0.2-SNAPSHOT/openapi-generator-project-6.0.2-20220712.082641-1.jar}"

if ! command -v wget &> /dev/null
then
    echo "wget could not be found, install it using your package manager, e.g. brew install wget"
    exit 1
fi

wget -O openapi-generator.jar "${OPEN_API_GEN_URL}"

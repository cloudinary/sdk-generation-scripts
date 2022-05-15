"""
This module generates packages from the OpenAPI spec.

It is meant to run in the Jenkins job, although it can be run independently.

See main function docstring for the required environment variables.
"""
import json
import logging
import os
import shutil
import subprocess
import sys

import yaml

OPEN_API_GEN = os.getenv('OPEN_API_GEN', 'openapi-generator-cli')

logging.basicConfig(level=logging.INFO)


def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip("_").replace(" ", "")


def parse_bool(b):
    return str(b).lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']


def exit_with_error(msg):
    logging.error(msg)
    sys.exit(1)


def run_command(*args):
    """
    Executes the command with the arguments and exits in case of an error.
    :param args: The command name and the arguments.
    :return: result
    """
    result = subprocess.run(args)
    if result.returncode != 0:
        exit_with_error(result)

    return result


def main():
    """
    Generates the specified packages based on the environment variables.
    :return: 0 on success and any other status code on error
    """
    dry_run = parse_bool(os.getenv("DRY_RUN", "true"))
    generate_only = parse_bool(os.getenv("GENERATE_ONLY", "true"))

    api_spec = os.getenv("YML")
    """The source OpenApi spec YML file."""

    definition_file = os.getenv("DEFINITION_FILE", "sdk.json")
    """The definition file of the code generation project, contains supported languages with other details."""
    sdks = os.getenv("SDKS", "")
    """Comma separated list of SDKs to generate."""

    org_name = os.getenv("ORG_NAME", "cloudinary")
    """GitHub repository organization(usually cloudinary). Can be changed for testing."""

    sdks = sdks.split(",")

    if not sdks:
        logging.warning("No SDKs to generate...")
        return 0

    with open(definition_file, 'r') as f:
        spec = json.load(f)

    with open(api_spec, "r") as f:
        yml = yaml.safe_load(f)

    package = camel_to_snake(yml["info"]["title"])
    version = yml["info"]["version"]

    definitions = dict([(d.pop('value'), d) for d in spec["SDKS"]])

    if not all(key in definitions for key in sdks):
        exit_with_error(f"Missing definitions for {list(set(sdks) - set(definitions.keys()))} SDKs, aborting.")

    for sdk in sdks:
        repo_name = definitions[sdk]["repo"].format(package=package)
        template = definitions[sdk]["template"]

        shutil.rmtree(repo_name, ignore_errors=True)

        repo_url = f"git@github.com:{org_name}/{repo_name}.git"

        if not generate_only:
            run_command("git", "clone", repo_url)

        run_command(OPEN_API_GEN, "generate", "-i", api_spec, "-g", template, "-t", f"templates/{sdk}",
                    "--git-user-id", org_name,
                    "--git-repo-id", repo_name,
                    "--package-name", repo_name,
                    "-c", f"configs/{sdk}/config.yml",
                    "-o", repo_name)

        os.chdir(repo_name)

        if generate_only:
            logging.info("Generate only, no further steps performed.")
            os.chdir("..")
            continue

        run_command("git", "add", ".")

        run_command("git", "commit", "-m", f"Version {version}")
        run_command("git", "tag", "-a", version, "-m", f"Version {version}")

        if dry_run:
            logging.info("Dry Run, no further steps performed.")
            os.chdir("..")
            continue

        run_command("git", "push")
        run_command("git", "push", "--tags")

        os.chdir("..")

    return 0


if __name__ == '__main__':
    main()

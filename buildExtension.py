import argparse
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory


parser = argparse.ArgumentParser(description="Builds a Blender extension")
parser.add_argument("--version", required=False)
args = parser.parse_args()
version = args.version or "0.0.0"


SUPPORTED_PLATFORMS = ["win_amd64", "manylinux_2_17_x86_64", "macosx_11_0_arm64"]

with TemporaryDirectory() as temp:
    shutil.copytree(Path(__file__).parent / 'src' / 'deadline' / 'blender_submitter' / 'addons' /'deadline_cloud_blender_submitter', temp, dirs_exist_ok=True)

    for platform in SUPPORTED_PLATFORMS:
        subprocess.run(f"pip download deadline --dest {temp}/wheels --only-binary=:all: --python-version=3.11 --platform={platform}".split(" "), check=True)

    manifest = f"""
    schema_version = "{version}"

    id = "deadline_cloud"
    version = "1.0.0"
    name = "AWS Deadline Cloud"
    tagline = "Submit jobs to AWS Deadline Cloud"
    maintainer = "AWS"
    type = "add-on"
    website = "https://github.com/aws-deadline/deadline-cloud-for-blender"
    tags = ["Render"] # https://docs.blender.org/manual/en/dev/advanced/extensions/tags.html
    blender_version_min = "4.2.0"

    license = [
    "SPDX:Apache-2.0", # https://spdx.org/licenses/
    ]
    copyright = [
    "2025 Amazon Web Services",
    ]

    # # Optional: list of supported platforms. If omitted, the extension will be available in all operating systems.
    # platforms = ["windows-x64", "macos-arm64", "linux-x64"]
    # # Other supported platforms: "windows-arm64", "macos-x64"

    # # https://docs.blender.org/manual/en/dev/advanced/extensions/python_wheels.html
    wheels = [
    "./wheels/PyYAML-6.0.2-cp311-cp311-macosx_11_0_arm64.whl",
    "./wheels/pyrsistent-0.20.0-cp311-cp311-macosx_10_9_universal2.whl",
    "./wheels/PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "./wheels/pyrsistent-0.20.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "./wheels/PyYAML-6.0.2-cp311-cp311-win_amd64.whl",
    "./wheels/pyrsistent-0.20.0-cp311-cp311-win_amd64.whl",
    "./wheels/QtPy-2.4.3-py3-none-any.whl",
    "./wheels/python_dateutil-2.9.0.post0-py2.py3-none-any.whl",
    "./wheels/attrs-25.1.0-py3-none-any.whl",
    "./wheels/s3transfer-0.11.3-py3-none-any.whl",
    "./wheels/boto3-1.37.4-py3-none-any.whl",
    "./wheels/six-1.17.0-py2.py3-none-any.whl",
    "./wheels/botocore-1.37.4-py3-none-any.whl",
    "./wheels/typing_extensions-4.12.2-py3-none-any.whl",
    "./wheels/click-8.1.8-py3-none-any.whl",
    "./wheels/urllib3-2.3.0-py3-none-any.whl",
    "./wheels/deadline-0.49.6-py3-none-any.whl",
    "./wheels/xxhash-3.5.0-cp311-cp311-macosx_11_0_arm64.whl",
    "./wheels/jmespath-1.0.1-py3-none-any.whl",
    "./wheels/xxhash-3.5.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "./wheels/jsonschema-4.17.3-py3-none-any.whl",
    "./wheels/xxhash-3.5.0-cp311-cp311-win_amd64.whl",
    "./wheels/packaging-24.2-py3-none-any.whl",
    ]

    [permissions]
    network = "Connect to AWS Deadline Cloud and upload asssets"
    files = "Read related assets"
    """
    with open(str(Path(temp) / "blender_manifest.toml"), "w") as file:
        file.write(manifest)

    zip = shutil.make_archive(f"dist/deadline-cloud-blender-addon-{version}", "zip", temp)

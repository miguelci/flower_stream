# Flower Design

## Requirements

To run this app in a docker container, you'll need to have [docker](https://docs.docker.com/install/) locally installed.


## Usage

### Local
`python main.py sample.txt`

### Docker
There are 2 script files available in the root folder:
1. `run.sh` builds the docker image (if not available) and runs it
2. `run_tests.sh` builds the docker image (if not available) and runs the tests


* note: all of these files need to have execute flag, run `chmod +x {filename}`

 #!/bin/bash

docker image inspect flowers:latest > /dev/null 2>&1 && : || docker build -t flowers .
docker run -it --rm flowers python -m unittest tests/*_test.py
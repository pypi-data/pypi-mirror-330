# This is the container for node execution

# Building and Deploying
docker build . -t node-runner
docker tag node-runner:latest rg.fr-par.scw.cloud/solnir-namespace/node-runner:latest
docker push rg.fr-par.scw.cloud/solnir-namespace/node-runner:latest
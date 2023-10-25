# Ray Deploying on Kubernetes using KubeRay

This is repo with minimal code to test ray deployment of a Serve deployment integrated with FastAPI.

1. `serve build` -> config file
2. `docker build . -t shavvimal/custom_ray:latest`
3. `docker image push shavvimal/custom_ray:latest`

curl -X POST -H 'Content-Type: application/json' http://localhost:8000/fruit/ -d '["MANGO", 2]'

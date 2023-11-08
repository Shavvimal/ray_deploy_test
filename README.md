# Ray Deploying on Kubernetes using KubeRay

This is repo with minimal code to test ray deployment of a Serve deployment integrated with FastAPI.

Steps:

1. Test local `ray serve` deployment
   - `serve run app.main:app`
2. Serve Deployment Locally
   - `serve build app.main:app -o config/serve-deployment.yaml`
   - Start a local Ray cluster: `ray start --head`
   - Start the application: `serve deploy config/serve-deployment.yaml`
   - Stop the application: `serve sray stophutdown`
   - Stop the local Ray cluster: ``
3. Push to dockerHub:
   - `docker build . -t shavvimal/custom_ray:latest`
   - `docker image push shavvimal/custom_ray:latest`
4. Deploy on Kubernetes Locally
   - See `setup.sh`
5. Deploy on Kubernetes on AWS
   - See `aws.sh`

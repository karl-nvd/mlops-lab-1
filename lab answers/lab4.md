# Lab 4 Answers

## Question 1

After removing the container and creating a new one, I saw the Default experiment with no runs again. Without a volume, files under `/mlflow-data` stay in the container and are lost when it is removed. Just stopping the same container would keep its files.

## Question 2

A named volume keeps MLflow's database and artifacts outside the container, so they survive when the container is removed. Docker manages the storage location. A bind mount would also work, but I would have to manage the folder path and permissions on my machine.

## Question 3

Compose puts the services on the same private network and provides DNS for their service names. This lets the inference container reach MLflow using `http://mlflow:5000`. In Lab 3, MLflow was running on my Windows machine, so I had to use `host.docker.internal` instead.

## Question 4

The environment variable lets me change the API address without editing the frontend code. Inside Compose, I can use `http://inference:8000`. Outside Compose, that service name will not resolve, so I need an address the frontend can actually reach.

## Question 5

Only MLflow and the frontend need published ports because I open them from my browser. The frontend reaches the API directly at `http://inference:8000` through the Compose network, so inference does not need a host port.

## Question 6

`depends_on` starts MLflow first, but it does not wait until MLflow is ready. If the API cannot load its model at startup and the connection attempts fail, startup fails and the inference container exits. In my successful run, MLflow was ready when inference requested the model, so it started normally.

## Question 7

`docker compose ps` showed port `5000` published for MLflow and `8501` for the frontend. Inference showed only `8000/tcp`, without a host mapping. This matches the Compose file: the API is reachable inside the network but is not published to my machine.

## Question 8

Refreshing the frontend alone does not reload the model. The API keeps the version it loaded at startup. After moving `champion` to Version 2, I ran `docker compose restart inference`. The MLflow logs then showed a successful download request for Version 2. I registered the same model twice, so the predictions did not change.

## Question 9

Restarting works because the API loads the model from MLflow every time it starts. The image contains the code and dependencies, while the model is fetched at startup. Changing the alias does not change the image, so no rebuild is needed.

## Question 10

After `docker compose down` and `up`, the model versions and `champion` alias were still there because the named volume was kept. After `docker compose down -v` and `up`, MLflow was empty because the volume containing its database and artifacts had been deleted. I then uploaded the saved model again, assigned `champion`, and restarted inference to restore predictions.

## Question 11

Compose can run multiple inference containers on one machine, but I would need a load balancer to distribute requests between them. To survive a machine failure, I would need an orchestrator such as Kubernetes, a shared durable artifact store, and a database with backups and failover. A local named volume alone cannot provide that.

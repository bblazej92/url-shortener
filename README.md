
## SERVICE REQUIREMENTS:

1. given only the original URL, generate a random short URL
2. given both the original URL and the desired short URL, create the desired short URL or give the user an error if that is not possible (ie. it was already taken)
3. retrieve the original URL, given a short URL
4. retrieve information about an existing short URL created by the user, including:
 	--> what is the original URL
 	--> when the shortening happened
 	--> how many times the short URL has been accessed
5. see a list of the URLs he/she created and the information detailed in item 4


## SOLUTION:

Slug is generated using mongodb objectID - because this objectID is unique we encode it with base64 (with replace of last 2 codes) and has as a result collision-resistant slug.
ObjectId has 24 characters in hex encoding and thanks to base64 we have 16 characters long slugs.
There can be a situation that user specified slug which is equal to generated one from objectID (extremely rare) so firstly we save object in db then check if slug generated from this id not exist and save slug if is unique else keep creating new object till we have unique slug.

When user specify own slug (service requirements 2) we check if it already exists and if not save it else raise error.

## REST API:

[REST API documentation](https://bblazej92.github.io/url-shortener/)

## HOW IS PROJECT ORGANIZED:

url-shortener:

--> app
- auth - views enabling OAuth2.0 authorization using Facebook
- main - views, schema and tests of core part of service
- models.py - models in mongo

--> docker
- development - docker-compose for develompent environment running backend server and mongodb in
              separate containers

--> utils

## SCALING REQUIREMENTS:
1. Point 3 from service requirements should be fast
2. We don`t expire links so we should to be able to store a lot of them
3. We should be resilient to load spikes as links can be put in social media
4. We cannot have collision - generating the same slug for different original URLs
5. We should be able to run normally even if one of machine fail
6. We should know if everything work well and machines doesn`t have to much load

HOW TO SCALE:
Using docker compose + docker swarm.
Running production with nginx or AWS load balancer and load balance whole traffic between many servers.
Sharding mongodb to many machines and adding caching layer on servers.


Ad 1 --> Caching layer and indexing mongodb

Ad 2 --> Mongodb has built in sharding which works well

Ad 3 --> Auto-scale number of backend servers which handle traffic + have caching layer for fast responses

Ad 4 --> Using algorithm described in SOLUTION we are collision resistant

Ad 5 --> Having many servers handling traffic and many shards of mongodb which internally replicate data between
         shard our infrastructure is NSPOF

Ad 6 --> Installing Check_MK monitoring and set sending email/sms on any serious warning and failure

## WHY MONGO?
According to CAP theorem we can have 2 of 3: Consistency, Availability, Partition Tolerance
I think that consistency in more important than availability in this service and mongodb has both
consistency and partition tolerance. What is more mongodb is stable and widely-used db.

## RUNNING DEVELOPMENT ENVIRONMENT:
./init_and_run_development.sh

Requirements: Installed virtualenvwrapper, Docker version 1.10.0+, docker-compose 1.8.0
What it does: It creates virtualenv, build essential docker containers, run service in detach mode
              and run unit tests


## TODO:
1. Write docstrings and generate documentation using Sphinx
2. Block possibility go generate slug the same as other view endpoint
3. Deploy on AWS or Heroku by adding production docker-compose
4. Write tests to views in auth/views.py
5. Finish TODOs left in code
6. Add caching to GET views
7. Create indexes to speed up querying mongo
8. Add test coverage info
9. Small refactor

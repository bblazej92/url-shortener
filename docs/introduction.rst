Introduction
============

**Url-shortener** is a service which enables to generate short links for given original url.


Service requirements
--------------------

#. given only the original URL, generate a random short URL
#. given both the original URL and the desired short URL, create the desired short URL or give the user an error if that is not possible (ie. it was already taken)
#. retrieve the original URL, given a short URL
#. retrieve information about an existing short URL created by the user, including:
    * what is the original URL
    * when the shortening happened
    * how many times the short URL has been accessed
#. see a list of the URLs he/she created and the information detailed in item 4


Solution
--------

Slug is generated doing random choice for each of 6 characters from set A-Za-z0-9 what gives us ~57 billions unique
slugs and high collision-resistance. Because of possibility of collision if custom slug was not specified we generate
random slug till we have unique one. When user specify own slug (service requirements 2) we check if it already exists
and if not save it else raise error.


Scaling requirements
--------------------

#. Point 3 from service requirements should be fast
#. We don`t expire links so we should to be able to store a lot of them
#. We should be resilient to load spikes as links can be put in social media
#. We cannot have collision - generating the same slug for different original URLs
#. We should be able to run normally even if one of machine fail
#. We should know if everything work well and machines doesn`t have to much load


How to scale
------------

Using docker compose + docker swarm.
Running production with nginx or AWS load balancer and load balance whole traffic between many servers.
Sharding mongodb to many machines and adding caching layer on servers.


Satisfying scaling requirements
-------------------------------
#. Caching layer and indexing mongodb
#. Mongodb has built in sharding which works well
#. Auto-scale number of backend servers which handle traffic + have caching layer for fast responses
#. Using algorithm described in Solution we are collision resistant
#. Having many servers handling traffic and many shards of mongodb which internally replicate data between shard our infrastructure is NSPOF
#. Installing Check_MK monitoring and set sending email/sms on any serious warning and failure
#. Monitoring of response time for views

Why mongo?
----------

According to CAP theorem we can have 2 of 3: Consistency, Availability, Partition Tolerance
I think that consistency is more important than availability in this service and mongodb has both
consistency and partition tolerance. What is more mongodb is stable and widely-used db.
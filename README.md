# Cassandra Scrapy Pipeline

Simple Scrapy pipeline that writes items to Cassandra. 

**[Scrapy](http://scrapy.org/)** is a powerful and [well documented](http://doc.scrapy.org/en/1.0/intro/overview.html) python crawling library.

**[Cassandra](http://cassandra.apache.org/)** is one of the [fastest](http://www.datastax.com/apache-cassandra-leads-nosql-benchmark) open source distributed databases.

These are notes for my own reference using OS X. They cover installation and running a simple example. I plan on utilizing scrapy and cassandra in a large scale distributed computing project.

## Installation

**$:**
	
	git clone https://github.com/dansandland/cassandra-scrapy-pipeline.git
	cd cassandra-scrapy-pipeline

    pip install scrapy
    brew install cassandra
    pip install cassandra-driver # python cassandra driver
    brew install libev # brew recommended
    nodetool status
    
`nodetool status` shows Cassandra's datacenter name(s): *datacenter1* (default). This is used to configure *NetworkTopologyStrategy* replication when defining the keyspace. 
    
Connect to the cluster, create a keyspace called *scrapy_dev* and set replication.
    
    $ cqlsh
    Connected to Test Cluster at 127.0.0.1:9042.
	[cqlsh 5.0.1 | Cassandra 2.1.7 | CQL spec 3.2.0 | Native protocol v3]
	Use HELP for help.
    cqlsh> CREATE KEYSPACE scrapy_dev WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'datacenter1' : 1 };
    
The value 1 associated with `datacenter1` represents the replication factor. This means there is one copy of each row in each node. A replication factor of 2 would be 2 copies of each row, each on a separate node, providing additional reliability and fault tolerance.
      
For a production environment with a datacenter configuration (multiple instances) *PropertyFileSnitch* needs to be configured via the *cassandra-topology.properties* file. http://docs.datastax.com/en/cassandra/1.2/cassandra/architecture/architectureSnitchPFSnitch_t.html

## Crawl & Verify

Using scrapy.org's [intro tutorial](http://doc.scrapy.org/en/latest/intro/tutorial.html).

**Crawl:**
	
	$ # from repo directory
	$ cd project
	$ scrapy crawl dmoz
	
**Verify:**

	$ cqlsh
	cqlsh> use scrapy_dev;
	cqlsh:scrapy_dev> SELECT COUNT(*) FROM scrapy_items;
	
	 count
	-------
	    59
	
	(1 rows)


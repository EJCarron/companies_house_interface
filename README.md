# companies_house_interface
## A command line application for pulling data from UK Companies House

The Companies House Interface (or chi for short) is a command line application for
pulling data from the UK Companies House, making connections between people and companies,
and then saving the data in various formats:
    - Neo4j graph database
    - json
    - csv
    - xlsx spreadsheets.

### Here is an example work flow:

Let's pick someone who directs multiple UK companies that we would like to look into.
For example the social media landlord Samuel Leeds:

![A screenshot of Samuel Leeds Companies House profile](/imgs/companies_house.png)

You then go to webpages url and copy the officer id, in this example it is
"c9MBFivRCmMdFZqdtmTcJnBqd54".

You then take the id and perform the following command:
"chi creategraph -oid c9MBFivRCmMdFZqdtmTcJnBqd54"

chi will then pull all of Samuel Leeds data, the data of all the companies that he directs,
the data of all the people that also direct those companies, and then the data of all
the companies that they direct. It will then add this data to a Neo4j graphDB
visualising the business network.

![A screenshot of a Neo4j GraphDB visualising Samuel Leeds' business network](/imgs/graph_example.png)


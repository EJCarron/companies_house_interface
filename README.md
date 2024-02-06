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

You then go to the webpage's url and copy the officer id, in this example it is
"c9MBFivRCmMdFZqdtmTcJnBqd54".

You then take the id and perform the following command:
"chi creategraph -oid c9MBFivRCmMdFZqdtmTcJnBqd54"

chi will then pull all of Samuel Leeds data, the data of all the companies that he directs,
the data of all the people that also direct those companies, and then the data of all
the companies that they direct. It will then add this data to a Neo4j graphDB
visualising the business network.

![A screenshot of a Neo4j GraphDB visualising Samuel Leeds' business network](/imgs/graph_example.png)


## Setup and Requirements

### pip
chi is not currently listed on PyPI, so you will have to clone this repo and then install it as an editable package:
- Clone the repo.
- cd to the directory.
- Run this command "pip install -e ."

### Companies House account
chi uses the Companies House api which requires a user key, in order to generate this key you need to make an account.
You can register for an account on the companies house site (search "companies house account register").
Once you have registered an account you need to go to the Companies House Developers Hub and Create an application.
This application will then generate and api key.

### Neo4j
In order to use chi you will need to have a Neo4j Graph DB setup and running. A tutorial on how to do this can be found
on their site https://neo4j.com/docs/getting-started/get-started-with-neo4j/

### Config

Once you have a Companies House api key and a Neo4j Graph DB running you can set up your chi config by running the
following command:
"chi setconfig"
You will then be prompted to enter 4 things:
- 'normal_key' your Companies House api key 
- 'uri' your Neo4j graph db's uri.
- 'username': your Neo4j username.
- 'pw' your Neo4j graph db's password.

## Commands

**setconfig**
> [!WARNING]
> This command must be run before any others will work. You can run it again at anytime to change the config values.

| parameter  | long         | short |
|------------|--------------|-------|
| normal key | --normal_key | -nk   | 
| uri        | --uri        | -uri  |
| username   | --username   | -un   |
| password   | --pw         | -pw   |


> [!NOTE]
> The following commands all have these options 
> --officer_ids, can be called multiple times if you wish to start from multiple people.
> --layers refers to how many times you wish to expand the business networks layers. It defaults to 1, which means that
> it fetches the data of the starting officers, their companies, the other officers of those companies and all of their 
> companies. Each subsequent layer repeats this proces expanding outward, it is not recommended to set this higher than
> 2 or 3 as the networks can become extremely large.
> --appointment_limit filters out any officer with a large number of appointments. There are some people and organisations
> that sit on the board of thousands of companies. Expanding a network from one of these officers could lead to the network 
> expanding to 10 or 100s of thousands of nodes.


**creategraph**

| parameter | long | short |
|------------|------|-------|
| Officer ids | --officer_ids | -oid | 
| Network layers | --layers | -l |
| Appointments limit | --appointments_limit | -al |



- **savejson**
- **savecsvs**
- **savexlsx**


| parameter | long | short |
|------------|------|-------|
| Officer ids | --officer_ids | -oid | 
| Network layers | --layers | -l |
| Appointments limit | --appointments_limit | -al |
| Save location | --path | -p |

> [!NOTE]
> savecsvs writes multiple csv files, so you must provide a path to an existing directory that you wish to write to
> rather than a path to the .csv files that you want to create.

**loadjsoncreategraph**
if you have saved a network to json you can convert it to a Neo4j graph DB.

| parameter | long   | short  |
|-----------|--------|--------|
| json path | --path | --path |

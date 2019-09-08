# Firebolt
Search results extraction for queries in various languages
## Welcome to Firebolt - a search automation tool.
Please follow these steps to configure the Google Cloud Services:

### For Cloud Translation:

- To use Translation API client libraries, we need the following additional configurations to be set up:
	- Install the client library using PIP
	  pip install --upgrade google-cloud-translate
	- Set up authentication
	- In the GCP Console, go to the Create service account key page
	- From the Service account list, select New service account
	- In the Service account name field, enter a name
	- From the Role list, select Project > Owner
	- Click Create. A JSON file that contains your key downloads to your computer
	- Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the file path of the JSON file that contains your service account key. This variable only applies to your current shell session, so if you open a new session, set the variable again.

### For Google Custom Search Engine:

- Create a Gmail account for the project, which will be used for creating the "search engine" and to generate the key for "Google Custom Search API" (depends on the organization)

- Create a domain specific search engine and a key is to be generated for using that search engine. For the project, we have configured two Custom Search Engines - one for a regular Google search and one with the Google News. Thus, there are two CSE-API keys being used in the code.

Note: Google Drive has been integrated to read files from Drive, instead of a local drive.

Once the setup is completed, executing main.py in your development environment should initiate the tool.

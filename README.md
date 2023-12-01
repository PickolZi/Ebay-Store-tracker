
# [Ebay-Store-tracker](https://github.com/PickolZi/Ebay-Store-tracker)
# Purpose
Tracking and displaying sold items of ebay sellers to get a better idea of how often a seller lists, how often items sell, and which items will be the best to continue selling.
# How to run
This application consists of a React frontend, Flask backend, Ebay's developer API, and lastly Linux's cronjobs that runs the daily python script to gather the ebay data. 

Below are the steps in order to successfully run this application

**Setting up Ebay API and its secret keys**
1. First, head over to the [Ebay Developer Sign up](https://developer.ebay.com/signin?tab=register) and create an account.
2. Next, keep track of [Ebay's API keys](https://developer.ebay.com/my/keys) after creating a Production application.
3. Lastly, after cloning the git repository, rename `SECRETS-sample.json` to `SECRETS.json`and fill in all of the Ebay keys(appid, devid, certid) (redirecturi and userToken can be left blank).

**Setting up the Flask Backend**
 1. You will need to download [Anaconda](https://www.anaconda.com/download/) or any other Python package manager in order to run the virtual environment.
 2. Create/Run the virtual environment `Ebay-Store-tracker/backend/` 
`conda create --name ebayStoreTracker python=3.11.4`
`pip install -r requirements.txt`
`conda activate ebayStoreTracker `

 4. Run the flask application by typing in   `Ebay-Store-tracker/backend/` (make sure conda environment is active)
`python run.py`

**Setting up the React Frontend**
1. First you will need to install the react dependencies in `Ebay-Store-tracker/frontend/`
`npm install`
2. Then, you have to run the react application in `Ebay-Store-tracker/frontend/`
`npm run dev`

**Setting up the cronjobs**
Ideally, this application should be ran on a linux server so you could use cronjobs to daily run the python script.
1. Type `crontab -e` in linux terminal 
2.  `0 0 * * * /usr/bin/python3 /home/{USER}/Ebay-Store-tracker/backend/api/ebay_functions.py`
	* Replace {USER} with the name of your user.
3. Make sure to `pip install -r requirements.txt` in your linux server directory `/Ebay-Store-tracker/backend/` so that your cronjobs can successfully run the script correctly.

To access the home page navigate to: http://localhost:5173/

# Endpoints:
All Endpoints return data in JSON format.
**Flask Endpoints:**
1. http://www.localhost:5000/api/getAllStores
	* Returns all stores and store_ids used to track ebay data.
2. http://www.localhost:5000/api/getAllActiveItems/store/{int:store_id}
	* Given the store_id from endpoint 1, we are returned all the currently active ebay items in a seller's store(could be up to 24 hours behind). Data includes: item_id, title, listed_date, date_last_updated, price, item_url, image_url, location, status, and store_id. In addition to number of items and total worth.
3. http://www.localhost:5000/api/getAllSoldItems/store/{int:store_id}
	* Given the store_id from endpoint 1, we are returned all currently sold ebay items depending on the date the function first ran. Data includes: item_id, title, listed_date, date_last_updated, date_sold, price, item_url, image_url, location, status, and store_id. In addition to number of items and total worth.
	* Can pass in two queries in the header: startDate and endDate
		* ?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD
		* ?startDate=2004-01-04&endDate=2023-11-30
4. http://www.localhost:5000/api/getListedItemsInfo/store/{int:store_id}
	* Given the store_id from endpoint 1, return the number of items and total worth of these items in the currently active ebay store.
	* Can pass in two queries in the header:  startDate and endDate
		* ?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD
		* ?startDate=2004-01-04&endDate=2023-11-30

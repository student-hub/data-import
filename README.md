# data-import
Tools for extracting and importing data into Firebase.

## Data sources
The files in the ['data/'](data) folder which are to be imported are either exports from various websites or scraped data obtained using the scripts in the ['crawlers/'](crawlers) folder. The actual importer is the `import.js` file.

## Data format
The script can import either .json or .xlsx files. Speadsheets would first be converted to JSON, and then imported.

Say we have the following .json file:

```json
{
   "people":[
      {
         "name":"John Doe",
         "position":"Boss",
         "email":"john.doe@cs.pub.ro"
      },
      {
         "name":"Jane Doe",
         "position":"Boss Lady",
         "email":"jane.doe@cs.pub.ro"
      }
   ],
   "websites":[
      {
         "label":"Google",
         "link":"https://google.com"
      }
   ]
}
```
Importing this would add two new documents to the `people` collection, and one new document to the `websites` collection. The existing documents in the database (if any) are preserved, and the new documents have auto-generated IDs.

The equivalent .xlsx file would have two sheets - one named "people", the second named "websites".

**people**
|name    |position |email             |
|:-------|:--------|:-----------------|
|John Doe|Boss     |john.doe@cs.pub.ro|
|Jane Doe|Boss Lady|jane.doe@cs.pub.ro|

**websites**
|label |link              |
|:-----|:-----------------|
|Google|https://google.com|


## Running the script

In order to use this script, you need to have [Node.js](https://nodejs.org/en/) installed on your system.

Additionally, you require admin access to ACS UPB Mobile's Firebase project to obtain a key. This is done by accessing "Users and Permissions" in the settings, navigating to "Service accounts" and generating a new private key for Node.js. This key should be saved in this directory as `serviceAccount.json` and should never be shared with anyone.

Place the file you would like to import in the [`data/`](data) folder in this repository, then run:

| :warning: | It is recommended to try importing to the dev database first (by simply downloading the dev service account key), just to make sure everything works as intended. |
|:--|:--|

```
npm ci
node import.js
```

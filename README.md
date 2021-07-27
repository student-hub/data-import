# data-import
Tools for importing data into Firebase.

## Importing .xlsx/.json files into Firestore

In order to use this script, you need to have [Node.js](https://nodejs.org/en/) installed on your system.

Additionally, you require admin access to ACS UPB Mobile's Firebase project to obtain a
key. This is done by accessing "Users and Permissions" in the settings, navigating to "Service
accounts" and generating a new private key for Node.js. This key should be saved in this directory
as `serviceAccount.json` and should never be shared with anyone.

Place the file you would like to import in the [`data/`](data) folder in this repository, then run:

| :warning: | It is recommended to try importing to the dev database first (by simply downloading the dev service account key), just to make sure everything works as intended. |

```
npm ci
node import.js
```

## Data sources
The files in the ['data/'](data) folder which are to be imported are either exports from various websites or scraped data obtained using the scripts in the ['crawlers/'](crawlers) folder.

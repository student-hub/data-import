'use strict';

// Dependencies
const firestoreService = require('firestore-export-import');
const firebaseConfig = require('./config.js');
const serviceAccount = require('./serviceAccount.json');
const excelToJson = require('convert-excel-to-json');
const inquirer = require('inquirer')
const inquirerFileTreeSelection = require('inquirer-file-tree-selection-prompt')
const path = require('path');
const chalk = require('chalk');
const fs = require('fs');

const selectFile = async () => {
  // Select file to import
  inquirer.registerPrompt('file-tree-selection', inquirerFileTreeSelection)

  var answers = await inquirer
    .prompt([
      {
        type: 'file-tree-selection',
        name: 'file',
        message: 'Select the file you would like to import:',
        pageSize: 5,
        root: './data/',
        validate: (item) => {
          const type = path.extname(item);
          if (type != ".xlsx" && type != ".json") {
            return 'Only Excel and JSON files are supported. Please select another file.'
          }
          return true;
        },
        onlyShowValid: true,
      }
    ]);

    return answers.file;
}

const convertFile = async (file) => {
  if (path.extname(file) == '.xlsx') {
    var answers = await inquirer
      .prompt([
        {
          type: 'confirm',
          name: 'convert',
          message: 'Proceed to convert ' + file + ' to JSON?',
        }
      ]);
    if (answers.convert) {
      // Convert Excel to JSON
      console.log('Converting...');

      const result = excelToJson({
          sourceFile: file,
          header:{
              rows: 1
          },
          columnToKey: {
              '*': '{{columnHeader}}'
          }
      });

      // TODO: Prompt user to select file name
      var newFile = './data/data.json';
      if (fs.existsSync(newFile)) {
        answers = await inquirer
          .prompt([
            {
              type: 'confirm',
              name: 'overwrite',
              message: 'File ' + newFile + ' already exists. Overwrite?',
            }
        ]);
        if (!answers.overwrite) {
          console.log('Import cancelled.');
          process.exit(0);
        }
      }

      fs.writeFileSync(newFile, JSON.stringify(result), 'utf8');

      console.log('File ' + newFile + ' created.');

      return newFile;
    } else {
      console.log('Import cancelled.');
      process.exit(0);
    }
  }

  return file;
}

// JSON To Firestore
const jsonToFirestore = async (file) => {
  console.log('Initialzing Firebase...');
  await firestoreService.initializeApp(serviceAccount);
  console.log('Firebase initialized.');

  console.log('Uploading file...')
  await firestoreService.restore(file);
  console.log('Upload success.');
};

const main = async () => {
  var file = await selectFile();
  var newFile = await convertFile(file);
  jsonToFirestore(newFile);
}

main()

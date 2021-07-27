// Firebase Config for prod DB
const prod = {
  apiKey: "AIzaSyC6-BEfdxQHSOTdpOfqLUB8_j7CGu4DvV0",
  authDomain: "acs-upb-mobile.firebaseapp.com",
  databaseURL: "https://acs-upb-mobile.firebaseio.com",
  projectId: "acs-upb-mobile",
  storageBucket: "acs-upb-mobile.appspot.com",
  messagingSenderId: "611150208061",
  appId: "1:611150208061:web:b62a7862a75930f48a1e54",
  measurementId: "G-S7BTKYBV5T"
}
// Firebase Config for dev DB
const dev = {
  apiKey: "AIzaSyCcjPiIekx_HJ5b4xsanjrl-gmjWUIDee4",
  authDomain: "acs-upb-mobile-dev.firebaseapp.com",
  databaseURL: "https://acs-upb-mobile-dev.firebaseio.com",
  projectId: "acs-upb-mobile-dev",
  storageBucket: "acs-upb-mobile-dev.appspot.com",
  messagingSenderId: "712935993826",
  appId: "1:712935993826:web:9d4208b5a346aae7a849bb",
  measurementId: "G-YB0Z77XG2L"
}
// Exports
exports.prod = prod;
exports.dev = dev;

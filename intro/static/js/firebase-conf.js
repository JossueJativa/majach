// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-analytics.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDcfdy0MUJLR1bCYnJ2kV6uxex7Ve1DBbE",
  authDomain: "majach-44e0a.firebaseapp.com",
  projectId: "majach-44e0a",
  storageBucket: "majach-44e0a.appspot.com",
  messagingSenderId: "1043106197807",
  appId: "1:1043106197807:web:27361d46d077919e2bf1da",
  measurementId: "G-JE1FLTHDB6"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
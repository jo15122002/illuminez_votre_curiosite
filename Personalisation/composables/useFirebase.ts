import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

export const useFirebase = () => {
    const firebaseConfig = {
        apiKey: "AIzaSyCfJwzhhqdATNZ7HPuBrYiYXqMmmCNeDZ4",
        authDomain: "activite-3-biolumni.firebaseapp.com",
        databaseURL: "https://activite-3-biolumni-default-rtdb.europe-west1.firebasedatabase.app",
        projectId: "activite-3-biolumni",
        storageBucket: "activite-3-biolumni.appspot.com",
        messagingSenderId: "954943036148",
        appId: "1:954943036148:web:10db2c247d75ff11c01ca1"
    }

    const firebaseApp = initializeApp(firebaseConfig);
    const firestore = getFirestore(firebaseApp);

    return {
        firebaseApp,
        firestore,
    }
}
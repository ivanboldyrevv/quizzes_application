import { verifyToken } from "../AuthHandlers/AuthUtils";

async function verifyOrKick() {
    const isVerified = await verifyToken(localStorage.getItem("access_token"));

    if (!isVerified) {
        window.location.replace("/");
    }    
}


async function fetchUserStatistics (setUserStatistics) {
    verifyOrKick();

    const userId = localStorage.getItem("userId");
    const response = await fetch(`http://localhost:8080/api/v1/quizzes/user_stats/${userId}`, {
        method: "GET",
        headers: {"Content-Type": "application/json"}
    });
    const data = await response.json();
    data.average_rating = data.average_rating.toFixed(1);
    setUserStatistics(data);
}

export { fetchUserStatistics };
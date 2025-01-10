import { useEffect, useState } from "react";

import { fetchUserStatistics } from "./Utils";
import Navbar from "../NavBar";
import UserStatCard from "./UserStatisticsCard";

import "../../App.css";
import "../styles.css";


function ProfilePage() {
    const [userStatistics, setUserStatistics] = useState([]);

    useEffect(() =>{
        fetchUserStatistics(setUserStatistics);
    }, [])

    return (
        <div className="App">
            <Navbar />
            <div className="content-container">
                <UserStatCard
                    userId={userStatistics.user_id}
                    username={userStatistics.username}
                    averageRating={userStatistics.average_rating}
                    executedQuizzes={userStatistics.executed_quizzes}
                />
            </div>        
        </div>
    );
}

export default ProfilePage;
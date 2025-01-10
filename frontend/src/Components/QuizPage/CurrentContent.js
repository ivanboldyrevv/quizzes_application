import Result from "./Result";
import Questions from "./Questions";


function CurrentContent({showResults,
                         evaluateScore,
                         quiz,
                         handleNextQuestion,
                         handleClick,
                         currentQuestionIndex,
                         selectedOptionId })
{
    if (showResults) {
        const score = evaluateScore();
        
        const token = localStorage.getItem("access_token");
        if (token) {
            const verifyToken = async () => {
                const response = await fetch("http://localhost:8080/api/v1/oauth2/verify_token",{
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    }
                })

                if (response.status == 200) {

                    const userId = localStorage.getItem("userId");
                    const quizId = quiz.quiz_id;
                    const currentTime = new Date();
                    const datetime = currentTime.toISOString();

                    const sendQuizResult = async () => {
                        const response = await fetch("http://localhost:8080/api/v1/quizzes/quiz_result", {
                            method: "POST",
                            headers: {"Content-Type": "application/json"},
                            body: JSON.stringify({
                                "user_id": userId,
                                "quiz_id": quizId,
                                "dispatch_date": datetime,
                                "accept_percent": score
                            })
                        })

                        if (!response.ok) {
                            alert("network error!");
                        }
                    }

                    sendQuizResult();
                }
            }

            verifyToken();
        } else {
            console.log(false);
        }

        return <Result
                    score={score}
                    totalQuestions={quiz.questions.length}
                />;
    } else {
        return (<Questions
            questions={quiz.questions}
            handleNextQuestion={handleNextQuestion}
            handleSelectAnswer={handleClick}
            currentQuestionIndex={currentQuestionIndex}
            selectedOptionId={selectedOptionId}
        />);
    }
}


export default CurrentContent;
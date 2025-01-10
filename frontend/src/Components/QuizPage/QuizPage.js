import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import Navbar from '../NavBar';
import CurrentContent from './CurrentContent';

import "../styles.css";
import "../../App.css";


function QuizPage() {
    const { quizId } = useParams();
    const [quiz, setQuiz] = useState({});
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [userAnswers, setUserAnswer] = useState({});   
    const [selectedOptionId, setSelectedOptionId] = useState(null);
    const [showResults, setShowResults] = useState(false);

    useEffect(() => {
        const fetchQuizzes = () => {
            fetch(`http://localhost:8080/api/v1/quizzes/quiz/${quizId}`)
                .then(response => response.json())
                .then(data => setQuiz(data));
        };
        fetchQuizzes();
    }, []);
    
    const handleClick = (questionId, optionId, isCorrect) => {
        setSelectedOptionId(optionId);
        setUserAnswer(prevAnswers => ({
            ...prevAnswers,
            [questionId]: isCorrect
        }));
    }

    const handleNextQuestion = () => {
        if (currentQuestionIndex < quiz.questions.length - 1) {
            setCurrentQuestionIndex(currentQuestionIndex + 1);
            setSelectedOptionId(null);
          } else {
            setShowResults(true);
          }
    };

    const evaluateScore = () => {                    
        const totalQuestions = quiz.questions.length;
        let totalCorrectQuestions = 0;

        for (const [_, value] of Object.entries(userAnswers)) {
            if (value) totalCorrectQuestions++;
        }

        return ((totalCorrectQuestions / totalQuestions) * 100).toFixed(1);

    }

    return (
        <div className="App">                    
        <Navbar/>
        <div className="content-container">
            <CurrentContent
                showResults={showResults}
                evaluateScore={evaluateScore}
                quiz={quiz}
                handleNextQuestion={handleNextQuestion}
                handleClick={handleClick}
                currentQuestionIndex={currentQuestionIndex}
                selectedOptionId={selectedOptionId}
            />
        </div>
        </div>
    );
}

export default QuizPage;

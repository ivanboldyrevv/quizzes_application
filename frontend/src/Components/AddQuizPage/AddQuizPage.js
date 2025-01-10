import Navbar from "../NavBar";
import Question from "./Question";
import QuestionForm from "./QuestionForm";
import QuizNameField from "./QuizNameField";
import DifficultChoosePanel from "./DifficultChosePanel";
import { AddQuestionFormButton, SubmitButton } from "./HandlerButtons";

import "../styles.css";
import "../../App.css";
import { useState } from "react";


function AddQuizPage() {    
    const [newQuiz, setNewQuiz] = useState({});
    const [questionForm, setStateQuestionForm] = useState(false);

    return (
        <div className="App">
            <Navbar />
            <div id="content-container" className="content-container">
                <div className="add-quiz-content">                
                    <QuizNameField />
                    <DifficultChoosePanel />
                    {questionForm && (<QuestionForm setNewQuiz={ setNewQuiz } setStateQuestionForm={ setStateQuestionForm }/>)}
                    <div id="created-questions-id" className="created-questions">
                        {newQuiz.questions && newQuiz.questions.map((q) => (
                            <Question key={q.question_text} questionText={q.question_text} options={q.options}/>
                        ))}
                    </div>
                    <AddQuestionFormButton
                        setStateQuestionForm={setStateQuestionForm}
                        questionForm={questionForm}
                    />
                    <SubmitButton newQuiz={newQuiz}/>
                </div>
            </div>
        </div>
    );
}

export default AddQuizPage;
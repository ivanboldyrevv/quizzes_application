import Button from "@mui/material/Button";


function AddQuestionFormButton({ setStateQuestionForm, questionForm }) {
    return (
        <Button
            id="add-question-button-id"
            className="add-button"
            variant="contained"
            onClick={() => (setStateQuestionForm(!questionForm))}
        >
            +
        </Button>
    );
}


function SubmitButton({ newQuiz }) {
    
    const sendNewQuiz = async () => {
        const quiz = {
            "quiz_name": document.getElementById("quiz-name").value,
            "questions": newQuiz.questions,
            "difficult_level": document.getElementById("difficult-level").value,
            "created_by": localStorage.getItem("userId")
        }

        const response = await fetch("http://localhost:8080/api/v1/quizzes/add_quiz",{
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(quiz)
        })

        if (response.ok) {
            alert("Викторина успешно отправлена!");
        } else {
            alert("Возникла ошибка!");
        }
    }


    return (
        <Button
            id="submit-button-id"
            className="submit-button"
            variant="contained"
            onClick={sendNewQuiz}
        >
            Отправить
        </Button>
    );
}


export { AddQuestionFormButton, SubmitButton };
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import Checkbox from "@mui/material/Checkbox";
import Button from "@mui/material/Button";


function QuestionForm({ setNewQuiz, setStateQuestionForm}) {
    function Option(optionText, isCorrect) {
        this.optionText = optionText;
        this.isCorrect = isCorrect;
    }

    function Question(questionText, options) {
        this.questionText = questionText;
        this.options = options;
    }

    const handleClick = () => {
        const options = [
            new Option(document.getElementById("option-1").value, document.getElementById("o1-correct").checked),
            new Option(document.getElementById("option-2").value, document.getElementById("o2-correct").checked),
            new Option(document.getElementById("option-3").value, document.getElementById("o3-correct").checked)
        ]
        const question = new Question(document.getElementById("question-text").value, options)

        setNewQuiz(prevQuiz => {
            return {
                ...prevQuiz,
                questions: prevQuiz.questions || [],
                questions: [...(prevQuiz.questions || []), {
                    question_text: question.questionText,
                    options: question.options.map(option => ({
                        option_text: option.optionText,
                        is_correct: option.isCorrect
                    }))
                }]
            };
        });
        setStateQuestionForm(false);
    }

    return (
        <div
            id="question-form-id"
            className="question-form"
        >
            <Stack spacing={1}>                
                <TextField id="question-text" label="Введите вопрос" variant="standard" />
                <div>
                    <TextField id="option-1" label="Введите ответ номер 1" variant="standard" />
                    <Checkbox id="o1-correct" color="success" />
                </div>
                <div>
                    <TextField id="option-2" label="Введите ответ номер 2" variant="standard" />
                    <Checkbox id="o2-correct" color="success" />
                </div>
                <div>
                    <TextField id="option-3" label="Введите ответ номер 3" variant="standard" />
                    <Checkbox id="o3-correct" color="success" />
                </div>
                <Button
                    className="black-button"
                    variant="contained"
                    onClick={handleClick}
                >
                    Подтвердить
                </Button>
            </Stack>
        </div>
    )
}

export default QuestionForm;
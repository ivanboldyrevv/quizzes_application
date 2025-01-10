import TextField from "@mui/material/TextField";


function QuizNameField() {
    return(
        <TextField
            id="quiz-name"
            className="quiz-name-form"
            label="Введите название квиза!"
            variant="standard" 
        />
    )
}

export default QuizNameField;
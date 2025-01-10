import Button from "@mui/material/Button";
import ToggleButton from '@mui/material/ToggleButton';
import Stack from "@mui/material/Stack";
import { styled } from '@mui/material/styles';


const OptionButton = styled(ToggleButton)(() => ({
    checkedBackgroundColor: "#000",
    '&.Mui-selected': {
        color: "#fff",
        backgroundColor: "#000",
    },
}));


function Questions({questions, handleNextQuestion,handleSelectAnswer,
    currentQuestionIndex, selectedOptionId}) {
    return (
        <div id="content-id" className="content_">     
        {Array.isArray(questions) && questions.length > 0 && (
        <>
            <div id="question-id" class="question">                    
                <h4>{questions[currentQuestionIndex].question_text}</h4>
            </div>
            <div id="options-id" key={currentQuestionIndex} class="options">
            <Stack
                id="stack-id"
                spacing={1}
                sx={{
                    minWidth: 100,
                    alignItems: "stretch"
                }}
            >
            {questions[currentQuestionIndex].option && questions[currentQuestionIndex].option.map((o, index) => (
                <OptionButton
                    id={index}
                    value={o.option_id}
                    selected={o.option_id === selectedOptionId}
                    onChange={() => handleSelectAnswer(questions[currentQuestionIndex].question_id, o.option_id, o.is_correct)}
                >
                    {`${o.option_name} : ${o.is_correct}`}
                </OptionButton>
            ))}
            </Stack>
            </div>
        </>
        )}
        <div id="next-container-id" class="next">
        <Button
            id="next-button-id"
            variant="contained"
            className="black-button"
            onClick={handleNextQuestion}
        >
            Далее
        </Button>
        </div>
        </div>
    );
}


export default Questions;
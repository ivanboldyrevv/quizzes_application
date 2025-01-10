import Button from "@mui/material/Button";

function Result({score, totalQuestions}) {
    return (
        <div className="content_">
            <div className="options">
                <h2>Результаты:</h2>
                <p>Общее количество вопросов: {totalQuestions}</p>
                <p>Ваш счет: {score}%</p>
                <Button
                    variant="contained"
                    className="black-button"
                    onClick={() => {window.location.reload()}}
                >
                    Повторить
                </Button>
          </div>
        </div>    
    );
};


export default Result;
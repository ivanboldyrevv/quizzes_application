import Button from "@mui/material/Button";

function AddQuizButton() {    
    const handleAddQuizClick = async () => {
        const token = localStorage.getItem("access_token")
  
        const response = await fetch("http://localhost:8080/api/v1/oauth2/verify_token",{
          method: "POST",
          headers: {"Content-Type": "application/json", "Authorization": `Bearer ${token}`}
        })
  
        if (response.status != 200) {
          alert("Вы должны быть зарегистрированны!");
          return;
        }
  
        window.location.replace("/add_quiz");
    }

    return (
        <div className="button-link">
            <Button
                id="add-quiz-button-id"
                className="black-button"
                variant="contained"
                onClick={handleAddQuizClick}
            >
                Добавить квиз
            </Button>
        </div>
    );
}

export default AddQuizButton;
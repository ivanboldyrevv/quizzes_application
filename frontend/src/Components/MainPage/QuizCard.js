import * as React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import CardActionArea from "@mui/material/CardActionArea";
import { useNavigate} from "react-router-dom";


function QuizCard({quizId, quizName, difficultLevel, createdBy, dateCreation}) {
  const navigate = useNavigate()

  const handleClick = () => {
    navigate(`/${quizId}`)
  }

  return (
    <Card sx={{ minWidth: 800 }}>
      <CardActionArea onClick={handleClick}>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {quizName}
          </Typography>
          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            Сложность: {difficultLevel}
          </Typography>
          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            Создан: {createdBy}
          </Typography>
          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            Дата создания: {dateCreation}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
}

export default QuizCard;
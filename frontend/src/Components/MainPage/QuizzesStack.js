import QuizCard from "./QuizCard";
import Stack from '@mui/material/Stack';


function QuizzesStack({ quizzes }) {
  return (
    <div className="content-container">
      <Stack>
        {quizzes && quizzes.map((quiz) => (
          <div className="content-card">
            <QuizCard
              quizId={quiz.quiz_id}
              quizName={quiz.quiz_name}
              difficultLevel={quiz.difficult_level}
              createdBy={quiz.created_by}
              dateCreation={quiz.creation_date}
            />
          </div>
        ))}
      </Stack>
    </div>
  );
}

export default QuizzesStack;
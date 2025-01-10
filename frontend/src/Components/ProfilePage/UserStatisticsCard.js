import Link from "@mui/material/Link";

function UserStatCard({ userId, username, averageRating, executedQuizzes }) {
    return (
        <div>            
            <p>ID Пользователя: {userId}</p>
            <p>Имя пользователя: {username}</p>
            <p>Средний рейтинг прохождения квизов: {averageRating} %</p>
            <div>
                <p>Пройденные квизы:</p>
                <>
                    {executedQuizzes && executedQuizzes.map((q) => (
                        <Link href={q.quiz_id} underline="hover">
                            <li>Имя: {q.quiz_name}; Процент правильных ответов: {q.accept_rate} %</li>
                        </Link>
                    ))}
                </>
            </div>
        </div>
    );
}


export default UserStatCard;
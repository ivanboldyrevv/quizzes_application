import * as React from 'react';

import Navbar from '../NavBar';
import AddQuizButton from './LinkButtons';
import QuizzesStack from './QuizzesStack';
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';

import '../../App.css';


function MainPage() {
    const [quizzes, setQuizzes] = React.useState([]);

    React.useEffect(() => {
      const fetchQuizzes = async () => {
        const response = await fetch("http://localhost:8080/api/v1/quizzes/quizzes");
        const data = await response.json();
        setQuizzes(data);
        console.log(data);
      };
      fetchQuizzes();
    }, []);

    return (
        <div className="App">
          <Navbar/>
          <AddQuizButton />
          <QuizzesStack quizzes={quizzes} />
          <div className="pagination">
            <Stack spacing={2}>
              <Pagination count={10} shape="rounded" />
            </Stack>
          </div>        
        </div>        
      );
}

export default MainPage;

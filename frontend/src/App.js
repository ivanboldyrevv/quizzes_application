import * as React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import SignInPage from "./Components/AuthHandlers/SignInPage";
import SignUpPage from './Components/AuthHandlers/SignUpPage';
import QuizPage from './Components/QuizPage/QuizPage';
import MainPage from "./Components/MainPage/MainPage";
import ProfilePage from "./Components/ProfilePage/ProfilePage";
import AddQuizPage from "./Components/AddQuizPage/AddQuizPage";
import './App.css';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/:quizId" element={<QuizPage />} />
        <Route path="/sign_in" element={<SignInPage />} />
        <Route path="/sign_up" element={<SignUpPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/add_quiz" element={<AddQuizPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import NotFoundPage from './pages/NotFoundPage';
import MainPage from './pages/MainPage';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import NotAnswered from './pages/NotAnswered';


function App() {
  return (
    <>
      <Navigation />
      <Routes>
        <Route path='*' element={<NotFoundPage />}></Route>
        <Route path='/' element={<MainPage />}></Route>
        <Route path='/ended_questions' element={<NotAnswered />}></Route>
        <Route path='/login' element={<LoginPage />}></Route>
        <Route path='/register' element={<SignUpPage />}></Route>
      </Routes>
    </>
  );
}

export default App;

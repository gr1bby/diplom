import axios, { AxiosError } from 'axios';
import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import logOut from '../hooks/logOut';
import httpClient from '../httpClient';


interface IRespAuth {
  code: string;
  username?: string;
}


const Navigation: React.FC = () => {
  const [authStatus, setAuthStatus] = useState<IRespAuth>()

  useEffect(() => {
    isAuthorized()
  }, [])


  async function isAuthorized() {
    try {
      const response = await httpClient.get('http://localhost:5000/@me')
      setAuthStatus(response.data)
      console.log(response.data)
      
  } catch (error) {
      const err = error as AxiosError
      alert(err.message)
  }
  }

  const handleQuestionsPageClick = () => {
    window.location.href = '/'
  };
  
  const handleAnswersPageClick = () => {
    window.location.href = '/ended_questions'
  };

  const handleLoginPageClick = () => {
    window.location.href = '/login'
  };

  const handleSignUpPageClick = () => {
    window.location.href = '/register'
  };

  return (
    <div className="h-16 bg-gray-900 px-4">
      {authStatus?.code === '200' ? (
        <div className='flex justify-between items-center h-16'>
          <div>
          <button className="text-white text-xl font-bold bg-gray-900 hover:bg-gray-700 px-4 py-2 rounded" onClick={handleQuestionsPageClick}>
            Вопросы
          </button>
          <button className="text-white text-xl font-bold bg-gray-900 hover:bg-gray-700 px-4 py-2 rounded" onClick={handleAnswersPageClick}>
            Завершенные вопросы
          </button>
          </div>
          <div>
            <button type="button" className="px-4 py-2 bg-white text-gray-900 rounded hover:bg-gray-100" onClick={() => logOut()}>
              Выйти
            </button>
        </div>
        </div>
      ) : (
        <div className='flex justify-end items-center h-16'>
          <button type="button" className="px-4 py-2 bg-white text-gray-900 rounded hover:bg-gray-100 mx-1" onClick={() => handleLoginPageClick()}>
            Вход
          </button>
          <button type="button" className="px-4 py-2 bg-white text-gray-900 rounded hover:bg-gray-100 mx-1" onClick={() => handleSignUpPageClick()}>
            Регистрация
          </button>
        </div>
      )}
    </div>

  )
}

export default Navigation
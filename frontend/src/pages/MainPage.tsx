import React, { useEffect, useState } from 'react';
import axios, { AxiosError } from 'axios';
import { IResponse } from '../models/models';
import httpClient from '../httpClient';


interface IResponses {
    responses: IResponse[];
}

interface IRespAuth {
    code: string;
    username: string;
  }


const MainPage: React.FC = () => {
    const [responses, setResponses] = useState<IResponses | null>(null)
    const [userAnswers, setUserAnswers] = useState<string[]>([]);
    const [authStatus, setAuthStatus] = useState<IRespAuth | null>(null)
    

    useEffect(() => {
        fetchData();
        isAuthorized();
    }, []);

    const fetchData = async () => {
        try {
            const response = await axios.get('http://localhost:5000/questions');
            setResponses(response.data);
            // console.log(responses)
        } catch (error) {
            console.error(error);
        }
    };
    
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

    const sendAnswer = async (response: IResponse, answer: string) => {
        try {
            response.user_answer = answer
            response.operator = authStatus?.username
            console.log(response)
            const resp = await axios.post('http://localhost:5000/send_answer', {
                response
            });
            if (resp.data === 'ok') {
                console.log('sended')
                fetchData();
                console.log('refreshed')
            }
        } catch (error) {
        console.error(error);
        }
    };

    const handleUserAnswerChange = (index: number, value: string) => {
        setUserAnswers((prevUserAnswers) => {
            const newUserAnswers = [...prevUserAnswers];
            newUserAnswers[index] = value;
            return newUserAnswers;
        });
    };

    return (
        <div className="bg-gray-100 p-6 rounded-md">
        {authStatus?.code === '200' ? (
            <>
            <div className="waiting">
                <h2 className="text-2xl font-semibold mb-4">Ожидающие вопросы</h2>
                {responses?.responses.map((item, index) => {
                if (item.status === 'waiting') {
                    return (
                    <div className="bg-white p-4 mb-4 rounded-md shadow-md" key={item._id}>
                        <div className="font-semibold mb-2">
                        Социальная сеть: {item.sn_id}, ID пользователя: {item.user_chat_id}
                        </div>
                        <div className="mb-2">
                        Вопрос: {item.user_question}
                        </div>
                        <div className="flex flex-row items-center">
                        <input
                            type="text"
                            value={userAnswers[index] || ''}
                            onChange={(e) => handleUserAnswerChange(index, e.target.value)}
                            placeholder="Введите ответ..."
                            className="w-60 mr-2 p-2 border border-gray-300 rounded-md"
                        />
                        <button onClick={() => sendAnswer(item, userAnswers[index] || '')} className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
                            Отправить
                        </button>
                        </div>
                    </div>
                    );
                }
                return null;
                })}
            </div>
            </>
        ) : (
            <div className="text-center text-xl text-gray-600">Войдите в аккаунт!</div>
        )}
        </div>


      
    );
};

export default MainPage;
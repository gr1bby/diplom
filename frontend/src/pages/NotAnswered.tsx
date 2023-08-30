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


const NotAnswered: React.FC = () => {
    const [responses, setResponses] = useState<IResponses | null>(null)
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

    return (
        <div className="bg-gray-100 p-6 rounded-md">
        {authStatus?.code === '200' ? (
            <>
            <div className="ended">
                <h2 className="text-2xl font-semibold mb-4">Завершенные вопросы</h2>
                {responses?.responses.map((item) => {
                if (item.status === 'ended') {
                    return (
                    <div className="bg-white p-4 mb-4 rounded-md shadow-md" key={item._id}>
                        <div className="font-semibold mb-2">
                        Социальная сеть: {item.sn_id}, ID пользователя: {item.user_chat_id}
                        </div>
                        <div className="mb-2">
                        Вопрос: {item.user_question}
                        </div>
                        <div className="mb-2">
                        Оператор: {item.operator}
                        </div>
                        <div>
                        Ответ оператора: {item.user_answer}
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

export default NotAnswered;
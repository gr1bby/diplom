import axios, { AxiosError } from 'axios'
import React, { useState } from 'react'
import httpClient from '../httpClient'

const LoginPage: React.FC = () => {
    const [credentials, setCredentials] = useState<string>("")
    const [password, setPassword] = useState<string>("")

    const signIn = async () => {
        try {
            const response = await httpClient.post(
                "http://localhost:5000/login",
                {
                    credentials,
                    password
                }
            )

            window.location.href = "/"

        } catch (err: any) {
            const error = err as AxiosError
            alert(error.message)
          }
    }

    return (
        <div className="flex container mx-auto px-96 py-32 flex-col justify-center items-center">
            <h1 className="text-2xl font-semibold mb-4">Авторизация</h1>
            <form className="flex flex-col items-center">
                <div className="flex flex-col py-2">
                <label className="text-xl">Имя пользователя:</label>
                <input
                    className="border-2 w-64 p-2 rounded-md"
                    type="text"
                    value={credentials}
                    onChange={(e) => setCredentials(e.target.value)}
                />
                </div>
                <div className="flex flex-col pb-4">
                <label className="text-xl">Пароль:</label>
                <input
                    className="border-2 w-64 p-2 rounded-md"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                </div>
                <button className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600" type="button" onClick={() => signIn()}>
                Sign In
                </button>
            </form>
        </div>

    )
}

export default LoginPage
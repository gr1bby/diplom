import axios, { AxiosError } from "axios";
import httpClient from "../httpClient";

export default async function logOut() {
    try {
        const response =await httpClient.post("http://localhost:5000/logout")
        window.location.href = "/"
    } catch (err) {
        const error = err as AxiosError
        alert(error.message)
    }
}
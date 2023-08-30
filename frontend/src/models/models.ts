export interface IResponse {
    _id: string;
    user_id: string;
    sn_id: string;
    user_chat_id: number;
    user_question: string;
    status: string;
    user_answer: string;
    operator: string | undefined;
}
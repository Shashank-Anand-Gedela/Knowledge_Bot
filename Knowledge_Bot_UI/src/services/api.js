import axios from "axios";

const api = axios.create({

    baseURL: "http://127.0.0.1:8000"

});

export async function askQuestion(question) {

    const response = await api.get("/ask", {

        params: {

            question

        }

    });

    return response.data;

}

export async function getDocuments() {

    const response = await api.get("/documents");

    return response.data.documents;

}

export default api;
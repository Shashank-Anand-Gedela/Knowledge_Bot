import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000"
});

export async function checkHealth() {
    const response = await api.get("/");
    return response.data;
}

export async function askQuestion(question, selectedDocument = null) {

    const response = await api.get("/ask", {
        params: {
            question,
            selected_document: selectedDocument
        }
    });

    return response.data;
}

export async function getDocuments() {

    const response = await api.get("/documents");

    return response.data.documents;
}

export async function uploadDocument(file) {

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/upload",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        }
    );

    return response.data;
}

export async function deleteDocument(filename) {

    const response = await api.delete(
        `/documents/${encodeURIComponent(filename)}`
    );

    return response.data;
}

export default api;
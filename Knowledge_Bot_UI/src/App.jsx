import { useEffect, useState, useRef } from "react";

import "./App.css";

import Sidebar from "./components/Sidebar/Sidebar";
import Header from "./components/Header/Header";
import Welcome from "./components/Welcome/Welcome";
import ChatWindow from "./components/Chat/ChatWindow";
import MessageInput from "./components/Chat/MessageInput";

import {
    askQuestion,
    getDocuments,
    uploadDocument,
    checkHealth
} from "./services/api";

function App() {

    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    const [documents, setDocuments] = useState([]);
    const [selectedDocument, setSelectedDocument] = useState(null);

    const [showDocuments, setShowDocuments] = useState(false);
    const [isOnline, setIsOnline] = useState(false);

    const fileInputRef = useRef(null);

    useEffect(() => {
        loadDocuments();
    }, []);

    useEffect(() => {

        async function pingBackend() {

            try {
                await checkHealth();
                setIsOnline(true);
            }
            catch {
                setIsOnline(false);
            }

        }

        pingBackend();

        const interval = setInterval(
            pingBackend,
            10000
        );

        return () => clearInterval(interval);

    }, []);

   async function loadDocuments() {

    try {

        const docs = await getDocuments();

        console.log("Updated docs:", docs);

        setDocuments([...docs]);

    }

    catch (err) {

        console.log(err);

    }

}

    async function sendMessage(question) {

        if (!question.trim()) return;

        const userMessage = {
            type: "user",
            text: question
        };

        setMessages(prev => [
            ...prev,
            userMessage
        ]);

        setLoading(true);

        try {

            const response = await askQuestion(
                question,
                selectedDocument
            );

            const botMessage = {
                type: "bot",
                text: response.answer,
                sources: response.sources || []
            };

            setMessages(prev => [
                ...prev,
                botMessage
            ]);

        }

        catch {

            setMessages(prev => [
                ...prev,
                {
                    type: "bot",
                    text: "Unable to connect to backend.",
                    sources: []
                }
            ]);

        }

        setLoading(false);

    }

    function newChat() {

        setMessages([]);
        setLoading(false);

    }

    function browseDocuments() {

        setShowDocuments(prev => !prev);

    }

    function openFilePicker() {

        fileInputRef.current.click();

    }

    async function handleFileUpload(event) {

        const file = event.target.files[0];

        if (!file) return;

        try {

            await uploadDocument(file);

            alert("Document uploaded successfully.");

            await loadDocuments();

            setShowDocuments(true);

        }

        catch (err) {

            if (err.response?.status === 400) {

                alert("Document already exists.");

            }

            else {

                alert("Upload failed.");

            }

        }

        event.target.value = "";

    }

    return (

        <div className="app">

            <Sidebar
    documents={documents}
    showDocuments={showDocuments}
    onBrowse={browseDocuments}
    onNewChat={newChat}
    onUpload={openFilePicker}
    selectedDocument={selectedDocument}
    setSelectedDocument={setSelectedDocument}
    reloadDocuments={loadDocuments}
/>

            <input
                type="file"
                ref={fileInputRef}
                style={{ display: "none" }}
                accept=".pdf,.docx,.pptx,.xlsx,.txt"
                onChange={handleFileUpload}
            />

            <div className="main">

                <Header isOnline={isOnline} />

                <div className="content">

                    {
                        messages.length === 0 ? (

                            <Welcome />

                        ) : (

                            <ChatWindow
                                messages={messages}
                                loading={loading}
                                selectedDocument={selectedDocument}
                            />

                        )
                    }

                </div>

                <MessageInput
                    onSend={sendMessage}
                    loading={loading}
                />

            </div>

        </div>

    );

}

export default App;
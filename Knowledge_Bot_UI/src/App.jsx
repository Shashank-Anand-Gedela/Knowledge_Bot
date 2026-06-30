import { useEffect, useState } from "react";

import "./App.css";

import Sidebar from "./components/Sidebar/Sidebar";
import Header from "./components/Header/Header";
import Welcome from "./components/Welcome/Welcome";
import ChatWindow from "./components/Chat/ChatWindow";
import MessageInput from "./components/Chat/MessageInput";

import {
    askQuestion,
    getDocuments
} from "./services/api";

function App() {

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    const [documents, setDocuments] = useState([]);

    const [showDocuments, setShowDocuments] = useState(false);

    useEffect(() => {

        loadDocuments();

    }, []);

    async function loadDocuments() {

        try {

            const docs = await getDocuments();

            setDocuments(docs);

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

            const response = await askQuestion(question);

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

        catch (err) {

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

    return (

        <div className="app">

            <Sidebar

                documents={documents}

                showDocuments={showDocuments}

                onBrowse={browseDocuments}

                onNewChat={newChat}

            />

            <div className="main">

                <Header />

                <div className="content">

                    {

                        messages.length === 0 ? (

                            <Welcome />

                        ) : (

                            <ChatWindow

                                messages={messages}

                                loading={loading}

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
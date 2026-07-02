import "./Chat.css";
import ChatBubble from "./ChatBubble";
import { Bot } from "lucide-react";

export default function ChatWindow({

    messages,

    loading,

    selectedDocument

}) {

    return (

        <div className="chat-window">

            {
    selectedDocument && (

        <div
            style={{
                background:"#eff6ff",
                border:"1px solid #bfdbfe",
                padding:"10px",
                borderRadius:"10px",
                marginBottom:"16px"
            }}
        >
            Asking questions only from:

            <strong>
                {" "}
                {selectedDocument}
            </strong>

        </div>

    )
}

            {messages.map((message, index) => (

                <ChatBubble

                    key={index}

                    message={message}

                />

            ))}

            {loading && (

                <div className="chat-row">

                    <div className="chat-avatar">

                        <Bot size={20} />

                    </div>

                    <div className="chat-content">

                        <div className="bubble">

                            <div className="loading">

                                <span></span>

                                <span></span>

                                <span></span>

                            </div>

                        </div>

                    </div>

                </div>

            )}

        </div>

    );

}
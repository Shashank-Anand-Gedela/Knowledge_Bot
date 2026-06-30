import "./Chat.css";
import ChatBubble from "./ChatBubble";
import { Bot } from "lucide-react";

export default function ChatWindow({

    messages,

    loading

}) {

    return (

        <div className="chat-window">

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
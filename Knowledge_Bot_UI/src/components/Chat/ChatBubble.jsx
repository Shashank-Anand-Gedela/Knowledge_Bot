import "./Chat.css";
import { Bot, User, Copy, Check } from "lucide-react";
import { useState } from "react";
import SourceCard from "./SourceCard";

export default function ChatBubble({ message }) {

    const [copied, setCopied] = useState(false);

    const isUser = message.type === "user";

    async function copyText() {

        await navigator.clipboard.writeText(message.text);

        setCopied(true);

        setTimeout(() => {

            setCopied(false);

        }, 1500);

    }

    return (

        <div className={`chat-row ${isUser ? "user" : "bot"}`}>

            <div className="chat-avatar">

                {isUser ? (

                    <User size={20} />

                ) : (

                    <Bot size={20} />

                )}

            </div>

            <div className="chat-content">

                <div className="bubble">

                    {message.text}

                    {!isUser && (

                        <div
                            style={{
                                display: "flex",
                                justifyContent: "flex-end",
                                marginTop: "18px"
                            }}
                        >

                            <button
                                onClick={copyText}
                                style={{
                                    border: "none",
                                    background: "transparent",
                                    cursor: "pointer",
                                    color: "#666"
                                }}
                            >

                                {copied ? (

                                    <Check size={18} color="#16a34a" />

                                ) : (

                                    <Copy size={18} />

                                )}

                            </button>

                        </div>

                    )}

                </div>

                {

                    !isUser &&

                    message.sources &&

                    message.sources.length > 0 &&

                    <SourceCard

                        sources={message.sources}

                    />

                }

            </div>

        </div>

    );

}
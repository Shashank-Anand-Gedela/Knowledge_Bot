import { useState } from "react";
import "./Chat.css";
import { SendHorizontal, Paperclip } from "lucide-react";

export default function MessageInput({

    onSend,

    loading

}) {

    const [message, setMessage] = useState("");

    function send() {

        if (!message.trim()) return;

        onSend(message);

        setMessage("");

    }

    function handleKeyDown(e) {

        if (e.key === "Enter" && !e.shiftKey) {

            e.preventDefault();

            send();

        }

    }

    return (

        <div className="input-area">

            <button className="attach-btn">

                <Paperclip size={20} />

            </button>

            <input

                type="text"

                value={message}

                placeholder="Ask anything about your documents..."

                onChange={(e) => setMessage(e.target.value)}

                onKeyDown={handleKeyDown}

                disabled={loading}

            />

            <button

                className="send-btn"

                onClick={send}

                disabled={loading}

            >

                <SendHorizontal size={20} />

            </button>

        </div>

    );

}
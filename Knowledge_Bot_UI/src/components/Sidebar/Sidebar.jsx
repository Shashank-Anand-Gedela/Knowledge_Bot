import "./Sidebar.css";
import {
    MessageSquarePlus,
    FolderOpen,
    Upload,
    Bot,
    FileText,
    FileSpreadsheet,
    FileType2,
    Presentation,
    FileCode2
} from "lucide-react";

export default function Sidebar({

    documents,

    showDocuments,

    onBrowse,

    onNewChat,

    onUpload

}) {

    function getIcon(type) {

        switch (type) {

            case "PDF":
                return <FileText size={16} color="#EF4444" />;

            case "DOCX":
                return <FileType2 size={16} color="#2563EB" />;

            case "XLSX":
                return <FileSpreadsheet size={16} color="#16A34A" />;

            case "PPTX":
                return <Presentation size={16} color="#EA580C" />;

            default:
                return <FileCode2 size={16} color="#6B7280" />;

        }

    }

    return (

        <aside className="sidebar">

            <div>

                <div className="sidebar-logo">

                    <div className="logo-circle">

                        KB

                    </div>

                    <div>

                        <h2>

                            Knowledge Bot

                        </h2>

                        <p>

                            Ask anything from your documents

                        </p>

                    </div>

                </div>

                <button

                    className="new-chat-btn"

                    onClick={onNewChat}

                >

                    <MessageSquarePlus size={18} />

                    <span>

                        New Chat

                    </span>

                </button>

                <div className="sidebar-title">

                    Documents

                </div>

                <button

                    className="sidebar-item"

                    onClick={onBrowse}

                >

                    <FolderOpen size={18} />

                    <span>

                        Browse Documents

                    </span>

                </button>

                {

                    showDocuments && (

                        <div className="documents-list">

                            {

                                documents.length === 0 ?

                                (

                                    <p className="empty-docs">

                                        No documents found.

                                    </p>

                                )

                                :

                                documents.map((doc,index)=>(

                                    <div

                                        className="document-item"

                                        key={index}

                                    >

                                        {getIcon(doc.type)}

                                        <span>

                                            {doc.name}

                                        </span>

                                    </div>

                                ))

                            }

                        </div>

                    )

                }

                <div className="sidebar-title">

                    Upload

                </div>

                <button

                    className="sidebar-item"

                    onClick={onUpload}

                >

                    <Upload size={18} />

                    <span>

                        Upload Files

                    </span>

                </button>

            </div>

            <div className="sidebar-footer">

                <div className="footer-avatar">

                    <Bot size={18} />

                </div>

                <div>

                    <h4>

                        Knowledge Bot

                    </h4>

                    <p>

                        Ready to help

                    </p>

                </div>

                <div className="online-status"></div>

            </div>

        </aside>

    );

}
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
    FileCode2,
    Trash2
} from "lucide-react";
import { deleteDocument } from "../../services/api";

export default function Sidebar({

    documents,

    showDocuments,

    onBrowse,

    onNewChat,

    onUpload,

    selectedDocument,

    setSelectedDocument,

    reloadDocuments

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
  async function handleDelete(filename) {

    const confirmed = window.confirm(
        `Delete ${filename}?`
    );

    if (!confirmed) return;

    try {

        await deleteDocument(filename);

if (
    selectedDocument &&
    selectedDocument.toLowerCase() === filename.toLowerCase()
) {
    setSelectedDocument(null);
}

setTimeout(async () => {
    await reloadDocuments();
}, 100);

alert("Document deleted successfully.");
        //alert("Document deleted successfully.");

    }

    catch (err) {

        console.log(err);

        alert("Failed to delete document.");

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
                            style={{
                                display:"flex",
                                alignItems:"center",
                                justifyContent:"space-between"
                            }}
                        >

                            <div
                                style={{
                                    display:"flex",
                                    alignItems:"center",
                                    gap:"8px",
                                    flex:1
                                }}
                            >

                                {getIcon(doc.type)}

                                <input
                                    type="radio"
                                    checked={
                                        selectedDocument?.toLowerCase() ===
                                        doc.name.toLowerCase()
                                    }
                                    onChange={() =>
                                        setSelectedDocument(doc.name)
                                    }
                                />

                                <a
                                    href={doc.url}
                                    target="_blank"
                                    rel="noreferrer"
                                >
                                    {doc.name}
                                </a>
                                {
                                selectedDocument && (

                                    <div
                                        style={{
                                            marginTop:"10px",
                                            fontSize:"13px",
                                            fontWeight:"600",
                                            color:"#2563eb"
                                        }}
                                    >
                                        Selected: {selectedDocument}
                                    </div>

                                )
                            }

                            </div>

                            <Trash2
                                size={16}
                                color="red"
                                style={{
                                    cursor:"pointer"
                                }}
                                onClick={() =>
                                    handleDelete(doc.name)
                                }
                            />

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
import "./Chat.css";
import {
    FileText,
    Hash,
    BookOpen
} from "lucide-react";

export default function SourceCard({ sources }) {

    if (!sources || sources.length === 0) return null;

    return (

        <div className="source-card">

            <div className="source-header">

                <FileText size={18} />

                <span>Sources</span>

            </div>

            {

                sources.map((source, index) => (

                    <div
                        className="source-item"
                        key={index}
                    >

                        <div
                            style={{
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center"
                            }}
                        >

                            <a
                                href={source.source_url}
                                target="_blank"
                                rel="noreferrer"
                                style={{
                                    fontWeight: "600",
                                    color: "#2563eb",
                                    textDecoration: "none"
                                }}
                            >
                                {source.document}
                            </a>

                        </div>

                        {

                            source.reference && (

                                <p
                                    style={{
                                        marginTop: "8px"
                                    }}
                                >

                                    <Hash
                                        size={14}
                                        style={{
                                            display: "inline",
                                            marginRight: "5px"
                                        }}
                                    />

                         

                                    <BookOpen
                                        size={14}
                                        style={{
                                            display: "inline",
                                            marginRight: "5px"
                                        }}
                                    />

                                    {source.heading}

                                </p>

                            )

                        }

                        {

                            source.preview && (

                                <div
                                    style={{
                                        marginTop: "14px",
                                        background: "#f8fafc",
                                        padding: "14px",
                                        borderRadius: "12px",
                                        lineHeight: "1.8",
                                        color: "#4b5563"
                                    }}
                                >

                                    {source.preview}

                                </div>

                            )

                        }

                    </div>

                ))

            }

        </div>

    );

}
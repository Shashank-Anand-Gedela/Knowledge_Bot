import "./Chat.css";
import {
    FileText,
    Hash,
    BookOpen,
    Star
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

                            <strong>

                                {source.document}

                            </strong>

                            {

                                source.score && (

                                    <span
                                        style={{
                                            background: "#ecfdf5",
                                            color: "#16a34a",
                                            padding: "4px 10px",
                                            borderRadius: "20px",
                                            fontSize: "12px",
                                            fontWeight: "600"
                                        }}
                                    >

                                        {(source.score * 100).toFixed(1)}%

                                    </span>

                                )

                            }

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

                                    {source.reference}

                                </p>

                            )

                        }

                        {

                            source.heading && (

                                <p
                                    style={{
                                        marginTop: "8px"
                                    }}
                                >

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

                            source.chunk && (

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

                                    {source.chunk}

                                </div>

                            )

                        }

                    </div>

                ))

            }

        </div>

    );

}
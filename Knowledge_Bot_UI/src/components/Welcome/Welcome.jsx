import "./Welcome.css";
import {
    FileText,
    FileSpreadsheet,
    Presentation,
    FileType2,
    FileCode2
} from "lucide-react";

export default function Welcome() {

    return (

        <div className="welcome">

            <div className="welcome-icon">

                👋

            </div>

            <h1>

                Hello!

            </h1>

            <p>

                Ask me anything about your documents.

            </p>

            <div className="welcome-files">

                <div className="welcome-card">

                    <FileText
                        size={20}
                        color="#ef4444"
                    />

                    <span>PDF</span>

                </div>

                <div className="welcome-card">

                    <FileType2
                        size={20}
                        color="#2563eb"
                    />

                    <span>Word</span>

                </div>

                <div className="welcome-card">

                    <FileSpreadsheet
                        size={20}
                        color="#16a34a"
                    />

                    <span>Excel</span>

                </div>

                <div className="welcome-card">

                    <Presentation
                        size={20}
                        color="#ea580c"
                    />

                    <span>PowerPoint</span>

                </div>

                <div className="welcome-card">

                    <FileCode2
                        size={20}
                        color="#6b7280"
                    />

                    <span>Text</span>

                </div>

            </div>

            <div className="today-divider">

                <div></div>

                <span>

                    Today

                </span>

                <div></div>

            </div>

        </div>

    );

}
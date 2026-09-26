import React from "react";

function WorkflowSuggestion({
    visible,
    onAutomate,
    onNotNow
}) {

    if (!visible) {
        return null;
    }

    return (

        <div className="workflow-suggestion">

            <div className="suggestion-header">

                <div className="suggestion-icon">
                    🔔
                </div>

                <div>

                    <h2>
                        Repeated Workflow Detected
                    </h2>

                    <p>
                        I noticed that you repeatedly perform
                        these steps.
                    </p>

                </div>

            </div>


            <div className="workflow-title">

                Process Customer Request

            </div>


            <div className="workflow-chain">

                <div className="workflow-node">
                    <span>✉️</span>
                    Gmail
                </div>

                <div className="arrow">
                    →
                </div>

                <div className="workflow-node">
                    <span>📎</span>
                    Attachment
                </div>

                <div className="arrow">
                    →
                </div>

                <div className="workflow-node">
                    <span>👥</span>
                    CRM
                </div>

                <div className="arrow">
                    →
                </div>

                <div className="workflow-node">
                    <span>💬</span>
                    Slack
                </div>

            </div>


            <div className="workflow-details">

                <div>
                    <span>Confidence</span>
                    <strong>98%</strong>
                </div>

                <div>
                    <span>Runs detected</span>
                    <strong>2</strong>
                </div>

                <div>
                    <span>Estimated time saved</span>
                    <strong>~15 min</strong>
                </div>

            </div>


            <div className="suggestion-message">

                <span>🤖</span>

                <p>
                    I can automate this workflow for you.
                    You remain in control and can stop it
                    whenever you want.
                </p>

            </div>


            <div className="suggestion-actions">

                <button
                    className="automate-button"
                    onClick={onAutomate}
                >
                    ⚡ Automate
                </button>

                <button
                    className="not-now-button"
                    onClick={onNotNow}
                >
                    Not Now
                </button>

            </div>

        </div>
    );
}

export default WorkflowSuggestion;
import React from "react";

function AgentPanel({ status = "Observing" }) {

    const statusInfo = {

        "Observing": {
            icon: "👁️",
            title: "Observing",
            description:
                "I'm watching your work for repeated patterns."
        },

        "Workflow Detected": {
            icon: "🧠",
            title: "Pattern Detected",
            description:
                "I found a workflow that appears to repeat."
        },

        "Executing": {
            icon: "⚡",
            title: "Executing",
            description:
                "I'm executing the approved workflow."
        }
    };

    const current =
        statusInfo[status] ||
        statusInfo["Observing"];

    return (

        <div className="agent-card">

            <div className="agent-avatar">
                {current.icon}
            </div>

            <h2>
                WorkFlowOS Agent
            </h2>

            <div className="agent-status">
                <span className="status-dot"></span>
                {current.title}
            </div>

            <p>
                {current.description}
            </p>


            <div className="agent-thinking">

                <div className="thinking-dot"></div>
                <div className="thinking-dot"></div>
                <div className="thinking-dot"></div>

            </div>


            <div className="agent-capabilities">

                <div>
                    <span>✓</span>
                    Activity observation
                </div>

                <div>
                    <span>✓</span>
                    Workflow detection
                </div>

                <div>
                    <span>✓</span>
                    AI planning
                </div>

                <div>
                    <span>✓</span>
                    Autonomous execution
                </div>

            </div>

        </div>
    );
}

export default AgentPanel;
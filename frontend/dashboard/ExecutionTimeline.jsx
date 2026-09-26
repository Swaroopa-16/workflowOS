import React, { useEffect, useState } from "react";

function ExecutionTimeline() {

    const steps = [

        {
            application: "Gmail",
            action: "Read customer email",
            icon: "✉️"
        },

        {
            application: "Gmail",
            action: "Download quotation.pdf",
            icon: "📎"
        },

        {
            application: "CRM",
            action: "Search ABC Ltd",
            icon: "👥"
        },

        {
            application: "CRM",
            action: "Update customer record",
            icon: "📝"
        },

        {
            application: "Slack",
            action: "Notify customer operations",
            icon: "💬"
        }

    ];


    const [currentStep, setCurrentStep] =
        useState(0);


    useEffect(() => {

        if (currentStep >= steps.length) {
            return;
        }

        const timer = setTimeout(() => {

            setCurrentStep(
                previous => previous + 1
            );

        }, 1200);

        return () => clearTimeout(timer);

    }, [currentStep]);


    return (

        <div className="execution-card">

            <div className="section-header">

                <div>

                    <h2>
                        Agent Execution
                    </h2>

                    <p>
                        WorkFlowOS is executing the approved workflow
                    </p>

                </div>

                <div className="executing-badge">
                    ⚡ Running
                </div>

            </div>


            <div className="timeline">

                {steps.map(
                    (step, index) => {

                        const completed =
                            index < currentStep;

                        const active =
                            index === currentStep;

                        return (

                            <div
                                className={
                                    `timeline-item ${completed
                                        ? "completed"
                                        : ""
                                    } ${active
                                        ? "active"
                                        : ""
                                    }`
                                }
                                key={index}
                            >

                                <div className="timeline-marker">

                                    {completed
                                        ? "✓"
                                        : index + 1
                                    }

                                </div>


                                <div className="timeline-content">

                                    <div className="timeline-app">

                                        <span>
                                            {step.icon}
                                        </span>

                                        {step.application}

                                    </div>

                                    <strong>
                                        {step.action}
                                    </strong>

                                    {active && (

                                        <span className="executing-text">
                                            Agent working...
                                        </span>

                                    )}

                                    {completed && (

                                        <span className="completed-text">
                                            Completed
                                        </span>

                                    )}

                                </div>

                            </div>

                        );

                    }
                )}

            </div>


            {currentStep >= steps.length && (

                <div className="execution-complete">

                    <span>🎉</span>

                    <div>

                        <strong>
                            Workflow completed
                        </strong>

                        <p>
                            All 5 actions were successfully executed.
                        </p>

                    </div>

                </div>

            )}

        </div>
    );
}

export default ExecutionTimeline;
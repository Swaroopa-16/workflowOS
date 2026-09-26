import React, { useEffect, useState } from "react";
import "./dashboard.css";

import ActivityMonitor from "./ActivityMonitor";
import AgentPanel from "./AgentPanel";
import WorkflowSuggestion from "./WorkflowSuggestion";
import ExecutionTimeline from "./ExecutionTimeline";

const API_URL = "http://127.0.0.1:5000/api";


function Dashboard() {

    const [agentStatus, setAgentStatus] =
        useState("Observing");

    const [backendConnected, setBackendConnected] =
        useState(false);

    const [workflowDetected, setWorkflowDetected] =
        useState(false);

    const [approved, setApproved] =
        useState(false);

    const [activities, setActivities] =
        useState([]);

    const [executionStarted, setExecutionStarted] =
        useState(false);


    // -------------------------------------------------
    // Check Python backend
    // -------------------------------------------------

    const checkBackend = async () => {

        try {

            const response = await fetch(
                `${API_URL}/status`
            );

            const data = await response.json();

            if (data.success) {

                setBackendConnected(true);

                console.log(
                    "🤖 WorkFlowOS backend connected"
                );

            }

        } catch (error) {

            setBackendConnected(false);

            console.error(
                "❌ WorkFlowOS backend unavailable:",
                error
            );

        }
    };


    // -------------------------------------------------
    // Simulate normal user activity
    // -------------------------------------------------

    useEffect(() => {

        // Connect to real Python backend
        checkBackend();


        const demoActivities = [

            {
                application: "Gmail",
                action: "Reading customer email",
                time: "10:42 AM"
            },

            {
                application: "Gmail",
                action: "Downloading quotation.pdf",
                time: "10:43 AM"
            },

            {
                application: "CRM",
                action: "Searching ABC Ltd",
                time: "10:44 AM"
            },

            {
                application: "CRM",
                action: "Updating customer record",
                time: "10:45 AM"
            },

            {
                application: "Slack",
                action: "Sending team notification",
                time: "10:46 AM"
            }

        ];


        let index = 0;


        const interval = setInterval(() => {

            if (index >= demoActivities.length) {

                clearInterval(interval);

                // Agent detected repetition
                setAgentStatus(
                    "Workflow Detected"
                );


                setTimeout(() => {

                    setWorkflowDetected(true);

                }, 800);


                return;
            }


            const activity =
                demoActivities[index];


            setActivities(
                previous => [

                    ...previous,

                    activity

                ]
            );


            index++;

        }, 900);


        return () => {

            clearInterval(interval);

        };

    }, []);


    // -------------------------------------------------
    // Automate
    // -------------------------------------------------

    const handleAutomate = () => {

        setWorkflowDetected(false);

        setApproved(true);

        setExecutionStarted(true);

        setAgentStatus("Executing");

    };


    // -------------------------------------------------
    // Not Now
    // -------------------------------------------------

    const handleNotNow = () => {

        setWorkflowDetected(false);

        setApproved(false);

        setExecutionStarted(false);

        setAgentStatus("Observing");

    };


    return (

        <div className="workflowos">


            {/* =========================================
                HEADER
            ========================================= */}

            <header className="topbar">


                <div className="brand">

                    <h1>
                        WorkFlowOS
                    </h1>

                    <p>
                        AI Workflow Automation Agent
                    </p>

                </div>


                <div className="status">

                    <span
                        className={
                            agentStatus === "Executing"
                                ? "status-dot executing"
                                : "status-dot"
                        }
                    />

                    {agentStatus}

                </div>

            </header>


            {/* =========================================
                BACKEND CONNECTION STATUS
            ========================================= */}

            <div
                style={{
                    padding: "8px 24px",
                    fontSize: "13px",
                    color: backendConnected
                        ? "#4ade80"
                        : "#f87171",
                    textAlign: "right"
                }}
            >

                {backendConnected
                    ? "● AI Backend Connected"
                    : "● AI Backend Offline"}

            </div>


            {/* =========================================
                MAIN DASHBOARD
            ========================================= */}

            <main className="dashboard">


                {/* =====================================
                    LEFT PANEL
                ===================================== */}

                <section className="main-panel">


                    {/* ACTIVITY MONITOR */}

                    <ActivityMonitor
                        activities={activities}
                    />


                    {/* WORKFLOW DETECTION */}

                    {workflowDetected &&
                        !approved && (

                            <WorkflowSuggestion

                                visible={true}

                                onAutomate={
                                    handleAutomate
                                }

                                onNotNow={
                                    handleNotNow
                                }

                            />

                        )}


                    {/* EXECUTION */}

                    {executionStarted && (

                        <ExecutionTimeline />

                    )}

                </section>


                {/* =====================================
                    RIGHT AGENT PANEL
                ===================================== */}

                <aside className="agent-sidebar">

                    <AgentPanel
                        status={agentStatus}
                    />

                </aside>


            </main>

        </div>

    );

}


export default Dashboard;
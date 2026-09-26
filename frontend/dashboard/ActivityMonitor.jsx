import React from "react";

function ActivityMonitor({ activities = [] }) {

    // Only render valid activity objects
    const validActivities = Array.isArray(activities)
        ? activities.filter(
            activity =>
                activity &&
                typeof activity === "object"
        )
        : [];

    return (
        <div className="activity-card">

            <div className="section-header">

                <div>
                    <h2>Live Activity</h2>

                    <p>
                        WorkFlowOS is observing your workflow
                    </p>
                </div>

                <div className="live-indicator">
                    <span></span>
                    LIVE
                </div>

            </div>


            <div className="activity-list">

                {validActivities.length === 0 ? (

                    <div className="empty-activity">

                        <div className="empty-icon">
                            👀
                        </div>

                        <p>
                            Waiting for user activity...
                        </p>

                        <span>
                            WorkFlowOS is observing
                        </span>

                    </div>

                ) : (

                    validActivities.map(
                        (activity, index) => (

                            <div
                                className="activity-item"
                                key={index}
                            >

                                <div className="activity-icon">

                                    {getApplicationIcon(
                                        activity.application
                                    )}

                                </div>


                                <div className="activity-info">

                                    <strong>
                                        {activity.application || "Unknown Application"}
                                    </strong>

                                    <span>
                                        {activity.action || "Activity detected"}
                                    </span>

                                </div>


                                <div className="activity-time">

                                    {activity.time || "Now"}

                                </div>

                            </div>

                        )
                    )

                )}

            </div>

        </div>
    );
}


// -------------------------------------------------
// Application icon
// -------------------------------------------------

function getApplicationIcon(application) {

    switch (
    application?.toLowerCase()
    ) {

        case "gmail":
            return "✉️";

        case "crm":
            return "👥";

        case "slack":
            return "💬";

        case "browser":
            return "🌐";

        case "excel":
            return "📊";

        default:
            return "🖥️";
    }
}


export default ActivityMonitor;
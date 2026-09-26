from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.main import WorkFlowOS


app = Flask(__name__)
CORS(app)

workflowos = WorkFlowOS()


# --------------------------------------------------
# STATUS
# --------------------------------------------------

@app.get("/api/status")
def status():

    return jsonify({
        "success": True,
        "agent": "WorkFlowOS",
        "status": "online"
    })


# --------------------------------------------------
# ACTIVITY
# --------------------------------------------------

@app.get("/api/activity")
def get_activity():

    try:

        sessions = workflowos.observer.get_sessions()

        return jsonify({
            "success": True,
            "sessions": sessions
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# OBSERVE
# --------------------------------------------------

@app.post("/api/observe")
def observe():

    data = request.get_json(silent=True) or {}

    try:

        # Store activity using the existing observer.
        workflowos.observer.record_activity(data)

        return jsonify({
            "success": True,
            "activity": data
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# DETECT WORKFLOW
# --------------------------------------------------

@app.post("/api/detect")
def detect():

    try:

        sessions = workflowos.observer.get_sessions()

        detection = workflowos.detect_workflow(
            sessions
        )

        return jsonify({
            "success": True,
            "detected": bool(detection),
            "workflow": detection
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# GENERATE WORKFLOW
# --------------------------------------------------

@app.post("/api/workflow")
def generate_workflow():

    try:

        data = request.get_json(silent=True) or {}

        detected_workflow = data.get(
            "detected_workflow"
        )

        if not detected_workflow:

            return jsonify({
                "success": False,
                "error": "detected_workflow is required"
            }), 400

        workflow = workflowos.generate_workflow(
            detected_workflow
        )

        return jsonify({
            "success": True,
            "workflow": workflow
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# APPROVAL
# --------------------------------------------------

@app.post("/api/approve")
def approve():

    try:

        data = request.get_json(silent=True) or {}

        workflow = data.get("workflow")

        if not workflow:

            return jsonify({
                "success": False,
                "error": "workflow is required"
            }), 400

        approved = workflowos.request_approval(
            workflow
        )

        return jsonify({
            "success": True,
            "approved": bool(approved)
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# EXECUTE
# --------------------------------------------------

@app.post("/api/execute")
def execute():

    try:

        data = request.get_json(silent=True) or {}

        workflow = data.get("workflow")

        if not workflow:

            return jsonify({
                "success": False,
                "error": "workflow is required"
            }), 400

        result = workflowos.execute_workflow(
            workflow
        )

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# MEMORY
# --------------------------------------------------

@app.get("/api/memory")
def memory():

    try:

        context = workflowos.memory.get_agent_context()

        return jsonify({
            "success": True,
            "memory": context
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# RUN COMPLETE WORKFLOW
# --------------------------------------------------

@app.post("/api/run")
def run_workflow():

    try:

        data = request.get_json(silent=True) or {}

        sessions = data.get("sessions", [])

        result = workflowos.run(
            sessions
        )

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# START SERVER
# --------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("        WorkFlowOS API")
    print("=" * 60)
    print()
    print("API running at:")
    print("http://127.0.0.1:5000")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
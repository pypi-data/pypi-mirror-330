import logging
from datetime import datetime, timedelta
from bson import ObjectId
from typing import Optional, List, Dict, Any
from talentwizer_commons.utils.db import mongo_database
from talentwizer_commons.app.engine import get_chat_engine
from celery.result import AsyncResult

logger = logging.getLogger(__name__)

# Initialize MongoDB collections
sequence_collection = mongo_database["email_sequences"]
sequence_audit_collection = mongo_database["email_sequence_audits"]
template_collection = mongo_database["templates"]

def cancel_sequence_steps(sequence_id: str, celery_app, reason: str = "Recipient replied to email") -> None:
    """Cancel remaining steps in a sequence."""
    try:
        # Find all scheduled audits for this sequence
        scheduled_audits = sequence_audit_collection.find({
            "sequence_id": sequence_id,
            "status": "SCHEDULED"
        })

        for audit in scheduled_audits:
            if audit.get("schedule_id"):
                # Revoke the Celery task
                celery_app.control.revoke(audit["schedule_id"], terminate=False)
                
            # Update audit status
            sequence_audit_collection.update_one(
                {"_id": audit["_id"]},
                {
                    "$set": {
                        "status": "CANCELLED",
                        "updated_at": datetime.utcnow(),
                        "cancel_reason": reason
                    }
                }
            )
        
        # Update sequence status
        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {
                "$set": {
                    "status": "COMPLETED",
                    "updated_at": datetime.utcnow(),
                    "completion_reason": reason
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Error cancelling sequence steps: {str(e)}")
        raise

def update_sequence_status(sequence_id: str, step_count: Optional[int] = None) -> None:
    """Update sequence status based on completed steps."""
    try:
        # Get all audits for this sequence
        audits = list(sequence_audit_collection.find({"sequence_id": sequence_id}))
        
        if not audits:
            return
        
        total_steps = step_count if step_count is not None else len(audits)
        completed_steps = sum(1 for audit in audits if audit["status"] in ["SENT", "CANCELLED"])
        failed_steps = sum(1 for audit in audits if audit["status"] == "FAILED")
        
        # Calculate new status
        if completed_steps + failed_steps == 0:
            new_status = "PENDING"
        elif completed_steps + failed_steps < total_steps:
            new_status = "IN_PROGRESS"
        else:
            new_status = "COMPLETED" if failed_steps == 0 else "FAILED"
            
        # Update sequence
        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {
                "$set": {
                    "status": new_status,
                    "updated_at": datetime.utcnow(),
                    "progress": {
                        "completed": completed_steps,
                        "failed": failed_steps,
                        "total": total_steps
                    }
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Error updating sequence status: {str(e)}")
        raise

async def create_sequence_for_profile(profile: dict, template: dict, token_data: dict, job_title: str, client_info: dict) -> dict:
    """Create and schedule email sequence for a single profile."""
    try:
        logger.info(f"Creating sequence for profile {profile.get('public_identifier')} with template {template.get('_id')}")
        logger.info(f"Template CC: {template.get('cc')}, BCC: {template.get('bcc')}")

        # Create sequence record with cc/bcc from template
        sequence = {
            "profile_id": str(profile["_id"]),
            "template_id": str(template["_id"]),
            "public_identifier": profile["public_identifier"],
            "status": "PENDING",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "thread_id": None,  # Will be set after first email
            "original_subject": None,  # Will be set after first email
            "sender": token_data["userEmail"],  # Add sender email
            "cc": template.get("cc", []),  # Copy CC from template
            "bcc": template.get("bcc", [])  # Copy BCC from template
        }
        
        sequence_result = sequence_collection.insert_one(sequence)
        sequence_id = str(sequence_result.inserted_id)
        logger.info(f"Created sequence {sequence_id} with CC: {sequence['cc']}, BCC: {sequence['bcc']}")

        # Process each step
        base_time = datetime.utcnow()
        for idx, step in enumerate(template["steps"]):
            # Calculate scheduled time
            if step['sendingTime'] == 'immediate':
                scheduled_time = base_time
            else:
                days = step.get('days', 1)
                scheduled_time = base_time + timedelta(days=days)
                if step.get('time') and step.get('timezone'):
                    # TODO: Add timezone conversion
                    pass

            logger.info(f"Processing step {idx} for sequence {sequence_id}, scheduled for {scheduled_time}")

            # Create audit record
            audit = {
                "sequence_id": sequence_id,
                "step_index": idx,
                "status": "SCHEDULED",
                "scheduled_time": scheduled_time,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_initial": idx == 0,
                "email_payload": {
                    "to_email": profile.get("email", []),
                    "subject": step["subject"],
                    "content": step["content"],
                    "sender": token_data["userEmail"],
                    "sequence_id": sequence_id,
                    "is_initial": idx == 0
                },
                "token_data": token_data
            }
            
            audit_result = sequence_audit_collection.insert_one(audit)
            audit_id = str(audit_result.inserted_id)
            logger.info(f"Created audit {audit_id} for step {idx}")
            
            # Schedule email task
            from talentwizer_commons.utils.email import schedule_email
            schedule_result = await schedule_email(
                email_payload={
                    **audit["email_payload"],
                    "audit_id": audit_id
                },
                scheduled_time=scheduled_time,
                token_data=token_data
            )
            logger.info(f"Scheduled email for step {idx} with result: {schedule_result}")

            # Update audit with schedule_id
            if schedule_result:
                sequence_audit_collection.update_one(
                    {"_id": audit_result.inserted_id},
                    {"$set": {"schedule_id": schedule_result}}
                )

        return {
            "sequence_id": sequence_id,
            "profile_id": str(profile["_id"]),
            "public_identifier": profile["public_identifier"]
        }
        
    except Exception as e:
        logger.error(f"Error creating sequence for profile {profile.get('public_identifier')}: {str(e)}", exc_info=True)
        # Cleanup any partial sequence
        if 'sequence_id' in locals():
            try:
                sequence_collection.delete_one({"_id": ObjectId(sequence_id)})
                sequence_audit_collection.delete_many({"sequence_id": sequence_id})
                logger.info(f"Cleaned up failed sequence {sequence_id}")
            except Exception as cleanup_error:
                logger.error(f"Error cleaning up failed sequence: {str(cleanup_error)}")
        raise

async def get_sequence_status(sequence_id: str) -> dict:
    """Get detailed status of a sequence."""
    try:
        sequence = sequence_collection.find_one({"_id": ObjectId(sequence_id)})
        if not sequence:
            raise ValueError(f"Sequence {sequence_id} not found")

        audits = list(sequence_audit_collection.find({"sequence_id": sequence_id}))
        
        # Get status counts
        status_counts = {
            "scheduled": sum(1 for a in audits if a["status"] == "SCHEDULED"),
            "sent": sum(1 for a in audits if a["status"] == "SENT"),
            "failed": sum(1 for a in audits if a["status"] == "FAILED"),
            "cancelled": sum(1 for a in audits if a["status"] == "CANCELLED")
        }
        
        # Get task statuses
        task_statuses = []
        for audit in audits:
            if audit.get("schedule_id"):
                task = AsyncResult(audit["schedule_id"])
                task_statuses.append({
                    "step_index": audit["step_index"],
                    "celery_status": task.status,
                    "result": str(task.result) if task.result else None
                })

        return {
            "sequence_status": sequence["status"],
            "status_counts": status_counts,
            "task_statuses": task_statuses,
            "updated_at": sequence["updated_at"]
        }

    except Exception as e:
        logger.error(f"Error getting sequence status: {str(e)}")
        raise

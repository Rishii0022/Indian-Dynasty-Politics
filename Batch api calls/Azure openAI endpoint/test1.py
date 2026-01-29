#To examine the job status details you can run:
print(batch_response.model_dump_json(indent=2))

#What to expect, input output error id files
# {
#   "id": "batch_6caaf24d-54a5-46be-b1b7-518884fcbdde",
#   "completion_window": "24h",
#   "created_at": 1722476583,
#   "endpoint": null,
#   "input_file_id": "file-9f3a81d899b4442f98b640e4bc3535dd",
#   "object": "batch",
#   "status": "completed",
#   "cancelled_at": null,
#   "cancelling_at": null,
#   "completed_at": 1722477429,
#   "error_file_id": "file-c795ae52-3ba7-417d-86ec-07eebca57d0b",
#   "errors": null,
#   "expired_at": null,
#   "expires_at": 1722562983,
#   "failed_at": null,
#   "finalizing_at": 1722477177,
#   "in_progress_at": null,
#   "metadata": null,
#   "output_file_id": "file-3304e310-3b39-4e34-9f1c-e1c1504b2b2a",
#   "request_counts": {
#     "completed": 3,
#     "failed": 0,
#     "total": 3
#   }
# }
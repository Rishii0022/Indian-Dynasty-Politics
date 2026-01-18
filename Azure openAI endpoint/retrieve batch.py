import json

output_file_id = batch_response.output_file_id

if not output_file_id:
    output_file_id = batch_response.error_file_id

if output_file_id:
    file_response = client.files.content(output_file_id)
    raw_responses = file_response.text.strip().split('\n')

    for raw_response in raw_responses:
        json_response = json.loads(raw_response)
        formatted_json = json.dumps(json_response, indent=2)
        print(formatted_json)
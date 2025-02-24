from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

groups = [
    {
        "id": 1,
        "groupName": "Group 1",
        "members": [1, 2, 3],
    },
    {
        "id": 2,
        "groupName": "Group 2",
        "members": [4, 5],
    },
]

students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "David"},
    {"id": 5, "name": "Eve"},
]

next_group_id = len(groups) + 1

@app.route('/api/groups', methods=['GET'])
def get_groups():
    """
    Route to get all groups
    return: Array of group objects
    """
    # TODO: (sample response below)
    return jsonify(groups)

@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Route to get all students
    return: Array of student objects
    """
    # TODO: (sample response below)
    return jsonify(students)

@app.route('/api/groups', methods=['POST'])
def create_group():
    """
    Route to add a new group
    param groupName: The name of the group (from request body)
    param members: Array of member names (from request body)
    return: The created group object
    """
    global next_group_id
    # Getting the request body (DO NOT MODIFY)
    group_data = request.json
    group_name = group_data.get("groupName")
    group_members = group_data.get("members")
    
    # TODO: implement storage of a new group and return their info (sample response below)
    if not group_name:
        abort(400, "Group name is required")
    # Check if all member IDs are valid by comparing against existing student IDs
    valid_members = []
    student_ids = [student["id"] for student in students]
    
    for member_id in group_members:
        if member_id not in student_ids:
            abort(400, f"Invalid student ID: {member_id}")
        valid_members.append(member_id)
    
    new_group = {
        "id": next_group_id,
        "groupName": group_name,
        "members": valid_members,
    }
    next_group_id += 1
    groups.append(new_group)

    return jsonify(new_group), 201

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """
    Route to delete a group by ID
    param group_id: The ID of the group to delete
    return: Empty response with status code 204
    """
    # TODO: (delete the group with the specified id)
    for i, group in enumerate(groups):
        if group["id"] == group_id:
            groups.pop(i)
            return '', 204
    abort(404, "Group not found")

@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """
    Route to get a group by ID (for fetching group members)
    param group_id: The ID of the group to retrieve
    return: The group object with member details
    """
    # TODO: (sample response below)
    for group in groups:
        if group["id"] == group_id:
            members_detail = []
            for member_id in group["members"]:
                for student in students:
                    if student["id"] == member_id:
                        members_detail.append(student)
                        break     

            return jsonify({
                "id": group["id"],
                "groupName": group["groupName"],
                "members": members_detail,
            })
    # TODO:
    # if group id isn't valid:
    abort(404, "Group not found")

if __name__ == '__main__':
    app.run(port=3902, debug=True)

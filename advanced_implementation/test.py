operators = {
    "available": {
        "A": {"call_id": ""},
        "B": {"call_id": ""}
    },
    "ringing": {
    },
    "busy": {
    }
}
# first_available_operator = next(iter(operators["available"].keys()))
id_op_available =  next(iter(operators["available"].keys()))
op_data = operators["available"].pop(id_op_available)
operators["ringing"][id_op_available] = op_data
print(operators)
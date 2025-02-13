from fastapi import FastAPI, HTTPException
from app.helper.calculator import evaluate_rpn, shunting_yard, tokenize
import json
from app.model.user_request import UserRequest
import os


app = FastAPI()


@app.get("/api/calc/add")
async def calc_add(op1: float, op2: float):
    result = op1 + op2
    response = {
        "expression": "{} + {}".format(op1, op2),
        "result": result,
    }
    return json.dumps(response, ensure_ascii=True)


@app.get("/api/calc/subtract")
async def calc_subtract(op1: float, op2: float):
    result = op1 - op2
    response = {
        "expression": "{} - {}".format(op1, op2),
        "result": result,
    }
    return json.dumps(response, ensure_ascii=True)


@app.get("/api/calc/multiply")
async def calc_multiply(op1: float, op2: float):
    result = op1 * op2
    response = {
        "expression": "{} * {}".format(op1, op2),
        "result": result,
    }
    return json.dumps(response, ensure_ascii=True)


@app.get("/api/calc/divide")
async def calc_divide(op1: float, op2: float):
    if op2 == 0:
        raise HTTPException(status_code=400, detail="Zero division error")
    result = op1 / op2
    response = {
        "expression": "{} / {}".format(op1, op2),
        "result": result,
    }
    return json.dumps(response, ensure_ascii=True)


@app.get("/api/calc/expression")
async def calc_expression(expr: str):
    try:
        tokens = tokenize(expr)
        rpn = shunting_yard(tokens)
        result = evaluate_rpn(rpn)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    response = {
        "expression": "".join(tokens),
        "result": result,
    }
    return json.dumps(response, ensure_ascii=True)


# homework 2
@app.post('/api/request/add')
async def add_request(request: UserRequest):
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(cur_dir, 'data', 'user_request')
    new_request_fn = os.path.join(path, "{}.json".format(request.id))
    with open(new_request_fn, 'w') as fp:
        fp.write(request.model_dump_json())
    response = {"request_id": str(request.id)}
    return json.dumps(response)

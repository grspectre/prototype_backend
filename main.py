from fastapi import FastAPI, HTTPException
from app.helper.calculator import evaluate_rpn, shunting_yard, tokenize
import json


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

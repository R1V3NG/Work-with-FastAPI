from fastapi import FastAPI, Query, Path, HTTPException
from fastapi.responses import JSONResponse
import random
import math
from enum import Enum

app = FastAPI()


class Values(str, Enum):
    C = ("celsius",)
    F = "fahrenheit"


@app.get("/about")
def about():
    student = {
        "FullName": "Хадиулин Дамир Маратович",
        "Group": "Т-333901-ИСТ",
        "Course": "3",
        "University": "НТИ УрФу",
        "GitHub": "https://github.com/R1V3NG",
    }
    return JSONResponse(content=student, media_type="application/json; charset=utf-8")


@app.get("/rnd")
def rnd(
    min: int = Query(1, description="Минимальное значение диапазона"),
    max: int = Query(100, description="Максимальное значение диапазона"),
):
    if min > max:
        raise HTTPException(
            status_code=400,
            detail="Минимальное значение не может быть больше максимального",
        )
    random_number = random.randint(min, max)

    return random_number


@app.post("/t_square/")
def t_square(
    a: float = Query(..., gt=0, description="Первая сторона треугольника"),
    b: float = Query(..., gt=0, description="Вторая сторона треугольника"),
    c: float = Query(..., gt=0, description="Третья сторона треугольника"),
):
    if not (a + b > c and a + c > b and b + c > a):
        raise HTTPException(
            status_code=400,
            detail=f"Треугольник со сторонами {a}, {b}, {c} не существует. "
            f"Сумма двух любых сторон должна быть больше третьей.",
        )

    perimeter = a + b + c
    p = perimeter / 2
    area = math.sqrt(p * (p - a) * (p - b) * (p - c))
    print(a, b, c, p)
    return f"Периметр треугольника равен {perimeter}, а площадь равна {area}"


@app.get("/convert/{from_unit}/{to_unit}/{value}")
def convert(from_unit: Values, to_unit: Values, value: float):
    if from_unit == Values.C and to_unit == Values.F:
        result = (value * 9 / 5) + 32
        return {
            "result": result,
            "from_value": value,
            "from_unit": from_unit.value,
            "to_unit": to_unit.value,
            "formatted": f"{round(value)}°C = {round(result)}°F",
        }
    elif from_unit == Values.F and to_unit == Values.C:
        result = (value - 32) * 5 / 9
        return {
            "result": result,
            "from_value": value,
            "from_unit": from_unit.value,
            "to_unit": to_unit.value,
            "formatted": f"{round(value)}°F = {round(result)}°C",
        }
    elif from_unit == to_unit:
        return {
            "result": value,
            "from_value": value,
            "from_unit": from_unit.value,
            "to_unit": to_unit.value,
            "formatted": f"{round(value)}° {from_unit.value} = {round(value)}° {from_unit.value}",
        }

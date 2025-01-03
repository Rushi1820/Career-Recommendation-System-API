from service.JobsService import get_students, createcareerpath
import logging
from model import carrer_path

from fastapi import APIRouter, Request

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("logs//user.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


router = APIRouter(tags=["Jobs"], prefix="/jobs")

@router.get("/getallstudents")
def getallstudents(careerpath: str = None):
    return get_students(careerpath)


@router.post("/addcareerpath")
def addcarerpath(request: Request):

    data =request.json()
    career_path = carrer_path(
        _id=data.get('_id'),
        role=data.get('role'),
        description=data.get('description'),
        skills=data.get('skills')
    )
    return createcareerpath(career_path)

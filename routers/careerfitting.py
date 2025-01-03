import logging


from fastapi import APIRouter
from service import carrerfittingService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("logs//user.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


router = APIRouter(tags=["Career Fitting"], prefix="/career")


@router.get("/careerfit")
def careerFit(studentId: str):
    return carrerfittingService.semwise_marks(studentId)


@router.get("/getCareerPaths")
def careerFit(studentId: str):
    return carrerfittingService.getCareerPaths()


@router.put("/careerpathupdate")
def careerpathupdate(studentId: str, careerpath: str):
    return carrerfittingService.add_careerpath(studentId, careerpath)

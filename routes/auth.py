from fastapi import APIRouter


router = APIRouter()


@router.post("/login")
def login(data: dict):

    email = data.get("email")
    password = data.get("password")


    if email == "admin@gmail.com" and password == "admin123":

        return {
            "success": True,
            "message": "Login successful"
        }


    return {
        "success": False,
        "message": "Invalid credentials"
    }
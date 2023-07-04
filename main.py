from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import timedelta
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from tortoise.queryset import Q
import shutil
from tortoise.exceptions import IntegrityError
import asyncio
from tortoise import Tortoise
from db.models import User,Profile, EmployerProfile,PostJob, ApplyForJob
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import  timedelta
from utils.token import get_user,create_access_token, password_context,authenticate_token,authenticate_employer_token
from db.models import User
from db.hash import ACCESS_TOKEN_EXPIRE_MINUTES
from tortoise import Tortoise






app = FastAPI()

  


class ProfileCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email_address: str
    city: str
    phone_number: int
    job_prefernece_title: str
    job_prefernece_type: str

    
class ProfileResponse(BaseModel):
    user: str
    first_name: str
    last_name: str
    email_address: str
    city: str
    phone_number: int
    job_prefernece_title: str
    job_prefernece_type: str


class EmployerCreateRequest(BaseModel):
    companies_name: str
    companies_number_of_employee: int
    first_name_and_last_name: str
    phone_number: int
    companies_industry: str
    

class EmployerResponse(BaseModel):
    user: str
    companies_name: str
    companies_number_of_employee: int
    first_name_and_last_name: str
    phone_number: int
    companies_industry: str
    

class PostJobCreateResponse(BaseModel):
    employer_profile_id: int
    job_title: str
    number_of_people_to_hire_for_the_job: int
    where_would_you_like_to_advertise_this_job: str
    type_of_job: str
    pay_information: int
    job_description: str
    number_of_days_to_hire: int

class PostJobResponse(BaseModel):
    user :str
    employer_profile_id: int
    job_title: str
    number_of_people_to_hire_for_the_job: int
    where_would_you_like_to_advertise_this_job: str
    type_of_job: str
    pay_information: int
    job_description: str
    number_of_days_to_hire: int

class UploadCvCreateResponse(BaseModel):
     resume_url: str

class ApplyForJobCreateResponse(BaseModel):
     job_id:int
     
class ApplyForJobResponse(BaseModel):
     user: str
     job_id:int
     resume_url: str
     
     


     

register_tortoise(
    app,
    db_url='YOUR-POSTGRES-KEY',
    modules={'models': ['db.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)






@app.post('/register')
async def register(username:str, password:str, is_employee:bool):
    existing_user = await get_user(username)
    if existing_user:
        raise HTTPException(status_code = 400, detail = 'Username already exists')
    hashed_password = password_context.hash(password)
    user = await User.create(username=username, password_hash = hashed_password, is_employee=is_employee)
    return {"message": "Registered successfuly"}


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password) or user.is_employee == True:
        raise HTTPException(status_code=401, detail="Invalid credentials, try the employer portal.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post('/employer_login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password) or user.is_employee == False:
        raise HTTPException(status_code=401, detail="Invalid credentials, try the job seeker portal.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

    
@app.get("/protected")
async def protected_route(user: User = Depends(authenticate_token)):
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        return {"message": "Protected route accessed successfully."}
    

@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password)or user.is_employee == True:
        raise HTTPException(status_code=401, detail="Invalid credentials, try the employee portal.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/employer_token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password)or user.is_employee == False:
        raise HTTPException(status_code=401, detail="Invalid credentials, try the job seeker portal.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}




@app.post("/create_profile", response_model = ProfileResponse,
                                description ='Creates a user profile' )
async def create_profile(new_profile:ProfileCreateRequest, user: User = Depends(authenticate_token)):
            try:
                create_profile = await Profile.create(user=user, first_name=new_profile.first_name, last_name = new_profile.last_name,
                                                    email_address = new_profile.email_address, city = new_profile.city, 
                                                    phone_number = new_profile.phone_number, job_prefernece_title = new_profile.job_prefernece_title,
                                                    job_prefernece_type = new_profile.job_prefernece_type
                                                        )

                response = ProfileResponse(user=user.username, first_name=new_profile.first_name, last_name = new_profile.last_name,
                                                    email_address = new_profile.email_address, city = new_profile.city, 
                                                    phone_number = new_profile.phone_number, job_prefernece_title = new_profile.job_prefernece_title,
                                                    job_prefernece_type = new_profile.job_prefernece_type )
                return response
            except IntegrityError:
                 raise HTTPException(status_code=404, detail='Profile already created')
                 
                 





@app.post("/employer_profile", response_model = EmployerResponse,
                                description ='Creates a user profile' )
async def employer_profile(new_profile:EmployerCreateRequest, user: User = Depends(authenticate_employer_token)):
            try:
                create_profile = await EmployerProfile.create(user=user, companies_name = new_profile.companies_name,
                                                            companies_number_of_employee = new_profile.companies_number_of_employee,
                                                            first_name_and_last_name = new_profile.first_name_and_last_name, phone_number = new_profile.phone_number,
                                                            companies_industry = new_profile.companies_industry
                                                        )

                response = EmployerResponse(user=user.username,companies_name = new_profile.companies_name,
                                                            companies_number_of_employee = new_profile.companies_number_of_employee,
                                                            first_name_and_last_name = new_profile.first_name_and_last_name, phone_number = new_profile.phone_number,
                                                            companies_industry = new_profile.companies_industry)
                return response
            except IntegrityError:
                 raise HTTPException(status_code=404, detail='Profile already created')
            

@app.post("/post_job", response_model = PostJobResponse,
                                description ='Creates a user profile' )
async def post_job(new_job:PostJobCreateResponse, user: User = Depends(authenticate_employer_token)):
            
            try:
                create_job = await PostJob.create(user=user, employer_profile_id = new_job.employer_profile_id, job_title = new_job.job_title, number_of_people_to_hire_for_the_job = new_job.number_of_people_to_hire_for_the_job,
                                                where_would_you_like_to_advertise_this_job = new_job.where_would_you_like_to_advertise_this_job,
                                                type_of_job = new_job.type_of_job, pay_information = new_job.pay_information,
                                                job_description = new_job.job_description, number_of_days_to_hire = new_job.number_of_days_to_hire
                                                        )

                response = PostJobResponse(user=user.username, employer_profile_id = new_job.employer_profile_id, job_title = new_job.job_title, number_of_people_to_hire_for_the_job = new_job.number_of_people_to_hire_for_the_job,
                                                where_would_you_like_to_advertise_this_job = new_job.where_would_you_like_to_advertise_this_job,
                                                type_of_job = new_job.type_of_job, pay_information = new_job.pay_information,
                                                job_description = new_job.job_description, number_of_days_to_hire = new_job.number_of_days_to_hire)
                return response
            except Exception as e:
                    raise HTTPException(status_code=400, detail=str(e))

@app.get("/jobs", description='Jobs available')
async def get_jobs():
    try:
        available_jobs = await PostJob.filter().values("job_title", "type_of_job", "pay_information", "job_description")
        return available_jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the jobs.")


@app.get("/search_jobs", description="Search for jobs")
async def search_jobs(job_title: str, type_of_job:str):
        try:    
            filters = []

            if job_title:
                filters.append(Q(job_title__icontains=job_title))
                
            if type_of_job:
                filters.append(Q(type_of_job__icontains=type_of_job))

            query = PostJob.filter(*filters)

            results = await query.filter().values("job_title",'type_of_job', 'pay_information','job_description')

            return results
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error occurred while searching jobs.")



@app.post("/apply_for_job", response_model=ApplyForJobResponse)
async def apply_for_job(
    job_id: int,
    user_id: int,
    resume: UploadFile = File(...),
    user: User = Depends(authenticate_token)
):
    try:
        with open(f"uploads/{resume.filename}", "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        
        
        post_job = await PostJob.get(id=job_id)  
        create_application = await ApplyForJob.create(
            post_job=post_job, user_id=user_id, resume_url=f"uploads/{resume.filename}"
        )

        
        response = ApplyForJobResponse(
            user=user.username,
            job_id=job_id,
            resume_url=f"uploads/{resume.filename}"
        )
        
        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))





            
            
     
     

     




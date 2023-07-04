from tortoise import fields, Model
from db.hash import password_context






class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length = 100)
    password_hash = fields.CharField(max_length = 100)
    is_employee = fields.BooleanField(default=False)

    async def verify_password(self, plain_password):
        return password_context.hash(plain_password)
    
    class PydanticMeta:
        exclude = ["password_hash"]

class Profile(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField("models.User", on_delete=fields.CASCADE, related_name="profile")
    first_name = fields.CharField(max_length = 100)
    last_name = fields.CharField(max_length = 100)
    email_address = fields.CharField(max_length= 100)
    city = fields.CharField(max_length= 100)
    phone_number = fields.IntField()
    job_prefernece_title = fields.CharField(max_length= 100)
    job_prefernece_type = fields.CharField(max_length= 100)

class EmployerProfile(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField("models.User", on_delete=fields.CASCADE, related_name="employerprofile")
    companies_name = fields.CharField(max_length = 100)
    companies_number_of_employee = fields.CharField(max_length = 100)
    first_name_and_last_name = fields.CharField(max_length= 100)
    phone_number = fields.IntField()
    companies_industry = fields.CharField(max_length= 100)
    
class PostJob(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, related_name="postjob")
    employer_profile = fields.ForeignKeyField("models.EmployerProfile", on_delete=fields.CASCADE, related_name="employerprofile")
    job_title = fields.CharField(max_length= 100)
    number_of_people_to_hire_for_the_job = fields.IntField()
    where_would_you_like_to_advertise_this_job = fields.CharField(max_length= 100)
    type_of_job = fields.CharField(max_length= 100)
    pay_information = fields.IntField()
    job_description = fields.CharField(max_length= 1000)
    number_of_days_to_hire = fields.IntField()


class ApplyForJob(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    post_job = fields.ForeignKeyField("models.PostJob", on_delete=fields.CASCADE)
    resume_url = fields.CharField(max_length= 1000)
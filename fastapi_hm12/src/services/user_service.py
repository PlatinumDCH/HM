class UserService:
    async def send_email(self, email:str):
        #loginc send email
        pass

    async def reset_password(self, email:str):
        #logic reset password
        pass

    async def send_email_via_rabbitmq(self, email:str, message:str):
        #loguc send email user rabbitmq
        pass
import tortoise.fields
from tortoise.models import Model

class User(Model):
    id = tortoise.fields.IntField(pk = True)
    telegram_id = tortoise.fields.BigIntField()
    username = tortoise.fields.TextField()
    first_answer = tortoise.fields.IntField()
    second_answer = tortoise.fields.IntField()
    third_answer = tortoise.fields.IntField()
    fourth_answer = tortoise.fields.IntField()
    fifth_answer = tortoise.fields.IntField()
    sixth_answer = tortoise.fields.IntField()
    seventh_answer = tortoise.fields.IntField()
    class Meta:
        table = 'User_questions'

class todo(Model):
    id = tortoise.fields.IntField(pk = True)
    telegram_id = tortoise.fields.BigIntField()
    username = tortoise.fields.TextField() 
    date = tortoise.fields.DateField() 
    todo_task = tortoise.fields.TextField()
    class Meta:
        table = 'todo_list'        

class Food(Model):
    id = tortoise.fields.IntField(pk = True)
    telegram_id = tortoise.fields.BigIntField()
    username = tortoise.fields.TextField()
    date = tortoise.fields.DateField()
    name = tortoise.fields.CharField(max_length = 255)
    protein = tortoise.fields.FloatField(default = 0.0)
    fats = tortoise.fields.FloatField(default = 0.0)
    carbs = tortoise.fields.FloatField(default = 0.0)
    kcal = tortoise.fields.FloatField(default = 0.0)
    quantity = tortoise.fields.FloatField()
    class Meta:
        table = 'calories'

class Products(Model):
    id = tortoise.fields.IntField(pk = True)
    name = tortoise.fields.CharField(max_length = 255)
    protein = tortoise.fields.FloatField(default = 0.0)
    fats = tortoise.fields.FloatField(default = 0.0)
    carbs = tortoise.fields.FloatField(default = 0.0)
    kcal = tortoise.fields.FloatField(default = 0.0)
    
    class Meta:
        table = 'products'    
from django.db import models

class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=100, null=True)
    cpf = models.CharField(max_length=11)
    verificado = models.BooleanField(default=False)

class Login(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)

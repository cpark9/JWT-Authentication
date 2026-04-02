from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=300)
    bio = models.CharField(max_length=300, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='user_images')
    location = models.CharField(max_length=300, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
# Django의 시그널(Signals) 시스템을 사용하여 유저(User) 모델과 프로필(Profile) 모델을 자동으로 연결하는 로직

# create_user_profile 함수
# 역할: 새로운 유저가 데이터베이스에 저장된 직후, 그 유저를 위한 프로필을 자동으로 생성합니다.
#      데이터가 처음 생성될 때만 True가 됩니다. (수정 시에는 False)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# save_user_profile 함수
# 역할: 유저가 저장될 때마다 해당 유저의 프로필도 함께 저장 
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# 시그널 연결
# post_save: "저장이 완료된 후"에 신호를 보내라는 이벤트 트리거입니다.
# create_user_profile이 신호를 받아 created=True임을 확인하고, 해당 유저용 Profile을 생성합니다.
post_save.connect(create_user_profile, sender=User)
# save_user_profile이 신호를 받아 해당 유저의 Profile을 저장합니다.
post_save.connect(save_user_profile, sender=User)
    

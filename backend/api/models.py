from django.db import models 
from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save 

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # 관리자 계정(createsuperuser)을 만들 때 username을 필수입력해야 한다는 뜻

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # User 모델과 1:1 관계를 설정하여 각 유저마다 하나의 프로필이 존재하도록 합니다. on_delete=models.CASCADE는 유저가 삭제될 때 해당 프로필도 함께 삭제되도록 합니다.
    # user = models.ForeignKey(User, on_delete=models.CASCADE) # ForeignKey는 1:N 관계를 설정하여 한 유저가 여러 프로필을 가질 수 있도록 합니다. 하지만 일반적으로 프로필은 유저당 하나씩 존재하기 때문에 OneToOneField가 더 적합합니다.
    
    full_name = models.CharField(max_length=300, null=True, blank=True)
    bio = models.CharField(max_length=300, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='user_images')
    location = models.CharField(max_length=300, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.full_name == "" or self.full_name == None:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)

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

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:30]
    

# Chat App Model
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reciever")
    

    message = models.CharField(max_length=10000000000)

    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
        verbose_name_plural = "Message"

    def __str__(self):
        return f"{self.sender} - {self.reciever}"

    @property
    def sender_profile(self):
        sender_profile = Profile.objects.get(user=self.sender)
        return sender_profile
    @property
    def reciever_profile(self):
        reciever_profile = Profile.objects.get(user=self.reciever)
        return reciever_profile
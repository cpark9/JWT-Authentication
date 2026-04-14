from api.models import User, Profile, Todo, ChatMessage
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

# 사용자 정보 시리얼라이저
# Django 안의 데이터를 JSON 형식으로 변환하거나, 반대로 사용자가 보낸 JSON 데이터를 Django 모델 객체로 변환해 주는 도구(Serializer)
# 웹 개발에서 백엔드(Django)와 프론트엔드(React, 앱 등)가 서로 대화할 때 필수적인 역할
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
 
#  Django REST Framework(DRF)와 Simple JWT 라이브러리를 사용하여, 
# 사용자가 로그인할 때 발급되는 JWT(JSON Web Token)와 응답 데이터를 커스텀하는 로직
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 클래스 인스턴스 생성 없이 호출되는 메서드로, 첫 번째 인자로 클래스 자체(cls)를 받습니다. Simple JWT 권장
    @classmethod

    # 토큰 내부에 정보 담기
    # 사용자가 로그인 성공 시 생성되는 JWT 토큰(주로 Access Token)의 Payload(내용물)에 추가 정보를 저장하는 역할
    def get_token(cls, user):
        # 1. 기본 토큰 가져오기
        token = super().get_token(user)

         # 프로필 존재 여부 체크 (안전성 확보)
        profile = getattr(user, 'profile', None)
        
        # 2. 토큰에 커스텀 정보(Claim) 추가하기
        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio
        # 데이터 변환: str(user.profile.image)처럼 이미지 경로 등을 문자열로 변환하여 JSON 직렬화가 가능하도록 처리합니다.
        token['image'] = str(user.profile.image) if profile.image else None
        token['verified'] = user.profile.verified

        return token

# 회원가입 시리얼라이저   
class RegisterSerializer(serializers.ModelSerializer):
    # 필드 정의 (입력값 설정)
    # write_only=True: 매우 중요한 설정입니다. 비밀번호를 DB에 저장할 때는 필요하지만, API 응답(JSON)에는 포함되지 않도록 보안을 유지합니다.
    # validators=[validate_password]: Django 기본 비밀번호 검증기(길이, 숫자 포함 여부 등)를 적용합니다. 
    # Django 공식 문서의 Password Validation 규칙을 따르게 됩니다.
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    # Meta 클래스 (모델 연결)
    # model = User: 이 시리얼라이저가 어떤 모델을 기반으로 하는지 정의합니다.
    # extra_kwargs: 모델 필드에 직접 손대지 않고도 required: True 같은 추가 옵션을 간편하게 부여합니다.
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }
        
    # 유효성 검사 (비밀번호 일치 여부 확인)
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    # 사용자 생성 (검증된 데이터로 새 사용자 인스턴스 생성)
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])  # 비밀번호 해싱 (암호화)
        user.save()

        return user
    
class TodoSerializer(serializers.ModelSerializer):
    # 1. user는 로그인 정보를 사용하므로 읽기 전용으로 설정
    # 2. title에 공백 허용 안 함(allow_blank=False) 설정
    title = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = Todo
        fields = ['id', 'user', 'title', 'completed']
        read_only_fields = ['user'] # 유저 정보는 직접 입력받지 않음

    # 3. 추가적인 세밀한 검증 (필요한 경우)
    def validate_title(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("제목은 최소 2글자 이상이어야 합니다.")
        return value

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [ 'id',  'user',  'full_name', 'image' ]
    
    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class MessageSerializer(serializers.ModelSerializer):
    reciever_profile = ProfileSerializer(read_only=True)
    sender_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id','sender', 'reciever', 'reciever_profile', 'sender_profile' ,'message', 'is_read', 'date']
    
    def __init__(self, *args, **kwargs):
        super(MessageSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2
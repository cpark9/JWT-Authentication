from api.models import User, Profile
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

# 사용자 정보 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
 
#   상속: JWT 발급을 담당하는 기본 시리얼라이저를 확장
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 클래스 인스턴스 생성 없이 호출되는 메서드로, 첫 번째 인자로 클래스 자체(cls)를 받습니다. Simple JWT 권장
    @classmethod
    # 부모 클래스의 메서드를 호출하여 기본적인 JWT(기본적으로 user_id 포함)를 먼저 생성합니다. 
    # 이 시점에서 표준 클레임이 담긴 토큰 객체가 생성.
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        # 데이터 삽입: 파이썬 딕셔너리처럼 token['키'] = 값 형태로 원하는 정보를 넣습니다.
        # 주의사항: 여기에 담긴 데이터는 Base64로 인코딩되어 누구나 열어볼 수 있습니다. 
        # 따라서 비밀번호 같은 민감 정보는 절대 넣으면 안 되며, 
        # 프론트엔드에서 사용자 UI 구성을 위해 바로 필요한 정보(이름, 프로필 이미지 등) 위주로 구성합니다.
        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio
        # 데이터 변환: str(user.profile.image)처럼 이미지 경로 등을 문자열로 변환하여 JSON 직렬화가 가능하도록 처리합니다.
        token['image'] = str(user.profile.image)
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
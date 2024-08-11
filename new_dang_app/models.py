from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

class User(AbstractUser):
    # 아이디
    username = models.CharField(
        max_length=25, 
        unique= True, 
        validators=[UnicodeUsernameValidator()], 
        error_messages={"unique": "이미 사용 중인 아이디입니다."},
    )
    # 닉네임
    nickname = models.CharField(max_length=25, unique=True)
    # 나이
    age = models.IntegerField(default=0, valitaros=[MaxValueValidator(100), MinValueValidator(1)])
    # 성별
    gender_choices = ((None, '선택'), ('M', '남자'), ('W', '여자'))
    gender = models.CharField(max_length=2, choices=gender_choices, default='선택')
    # 주소
    postcode = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    detailAddress = models.CharField(max_length=250)
    extraAddress = models.CharField(max_length=250)
    # 연락처
    phone_numRegex = RegexValidator(regex=r"^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$")
    phone_num = models.CharField(validators=[phone_numRegex], max_length=11, blank=True)
    is_phone_active = models.BooleanField(default=False)

class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pet')
    # 이미지
    pet_image = ProcessedImageField(
        upload_to='images/accounts_pets/',
        blank=True,
        processors=[ResizeToFill(200, 200)],
        format='JPEG',
        options={"quality": 100},
    )
    # 반려동물 이름
    pet_name = models.CharField(max_length=25)
    # 반려동물 나이
    pet_age = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    # 반려동물 성별
    pet_gender_choices = ((None, '선택'), ('M', '남아'), ('W', '여아'))
    pet_gender = models.CharField(max_length=2, choices=pet_gender_choices, default='선택')
    # 중성화 여부
    neutralization_choices = ((None, '선택'), ('Y', '중성화 완료'), ('N', '중성화 전'))
    neutralization = models.CharField(max_length=2, choices=neutralization_choices, default='선택')
    # 분류
    species_choices = ((None, '선택'), ('dog', '강아지'), ('cat', '고양이'), ('others', '❤️'))
    species = models.CharField(max_length=25, choices=species_choices ,default='선택')
    breeds = models.CharField(max_length=50)
    birthday = models.DateField(blank=True)
    vaccination_status = models.BooleanField(default=False)
    characteristics = models.CharField(max_length=100, blank=True)
    size_choices = ((None, '선택'), ('large', '대형(25kg~)'), ('middle', '중형(10kg~25kg)'), ('small', '소형(~10kg)'))
    size = models.CharField(max_length=10, choices=size_choices, default='선택')
    weight = models.FloatField(max_length=50, defalut=0)
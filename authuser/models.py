from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('0', 'Không hợp lệ'),
    ('1', 'Thành công'),
    ('2', 'Chờ xử lý'),
    ('3','Mới tạo tài khoản')
)
class UserProfile(models.Model):
    user = models.OneToOneField(User, default=None, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='images/', default="images/avatar-default.jpg")
    phone = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.user.email


class UserUpgrade(models.Model):
    user = models.OneToOneField(User, default=None, on_delete=models.CASCADE)
    upgrade = models.BooleanField(default=False)
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default='3')
    def __str__(self):
        return self.user.username + " - " + self.state

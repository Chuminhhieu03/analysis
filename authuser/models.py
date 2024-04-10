from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('0', 'Không hợp lệ'),
    ('1', 'Thành công'),
    ('2', 'Chờ xử lý'),
    ('3', 'Mới tạo tài khoản')
)

TYPE_CHOICES = (
    ('0', 'Tài khoản cá nhân'),
    ('1', 'Tài khoản doanh nghiệp')
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, default=None, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='0')
    avatar = models.ImageField(
        upload_to='images/', default="images/avatar-default.jpg")
    phone = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.user.username  + " - " +  self.user.email + " - " + TYPE_CHOICES[int(self.type)][1]


STATUS_CHOICES = (
    ('0', 'Chưa phản hồi'),
    ('1', 'Đã phản hồi'),
)

class UserUpgrade(models.Model):
    user = models.OneToOneField(User, default=None, on_delete=models.CASCADE)
    upgrade = models.BooleanField(default=False)
    state = models.CharField(
        max_length=100, choices=STATE_CHOICES, default='3')

    def __str__(self):
        return self.user.username + " - " + STATE_CHOICES[int(self.state)][1]

class FeedBack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    email = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=100, default="")
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default='0')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " - " + STATUS_CHOICES[int(self.status)][1]

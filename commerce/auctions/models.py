from django.contrib.auth.models import AbstractUser
from django.db import models


# AbstractUserから継承
class User(AbstractUser):
    pass

# 商品カテゴリ
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"

# オークションリスト
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image_url = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    active = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

# 入札
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bidder")
    title = models.CharField(max_length=64)
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} bid {self.bid} to {self.title}"

# リストに作成されたコメント
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at}"

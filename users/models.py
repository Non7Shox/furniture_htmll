from django.contrib.auth import get_user_model
from django.db import models
UserModel = get_user_model()


class VerificationCodeModel(models.Model):
    code = models.CharField(max_length=6,unique=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='verification_codes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Verification Code'
        verbose_name_plural = 'Verification Codes'


class AccountsModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='account')
    full_name = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

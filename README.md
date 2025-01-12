
# Django Walleter


## Installation

1. Run the [pip](https://pip.pypa.io/en/stable/) command to install the latest version:
```bash
 pip install django_walleter
```

2. Add `django_walleter` to your `INSTALLED_APPS` in settings.py:
```bash
 INSTALLED_APPS = (
    ...
    'django_walleter',
 )
```
3. Run the migration command:
```bash
 python manage.py migrate
```
<br>

## Usage
Add the  `HasWallet`  mixin to your model.

```python
from django.db import models
from django_walleter import HasWallet

class Profile(models.Model, HasWallet):  
	phone = models.CharField(max_length=255, verbose_name='Phone')
	address = models.TextField(max_length=512,verbose_name='Address')
```	

Then you can easily make transactions from your model.
```python
profile = Profile.objects.get(pk=1)
profile.balance // 0
  
profile.deposit(100)
profile.balance // 100

profile.withdraw(20)
profile.balance // 80

profile2 = Profile.objects.get(pk=2)
profile.transfer(profile2, 20) // or profile.transfer(profile2.wallet, 20)

```	

**Remember ,** you may use the `django_walleter.HasWallet` mixin on any of your models. You are not limited to only including it on your `Profile`model.

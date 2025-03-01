# drfkwargs
Django REST framework keywords names for extra_keyword meta attribute of serializers stored as constants

<br>

## Installing

> [!NOTE]
> It's recommended to activate
> <a href="https://docs.python.org/3/library/venv.html">Virtual Environment</a>
> before installing drfkwargs

To clone and install required packages use the following command:
```bash
# linux/macOS
$ python3 -m pip install drfkwargs

# windows
$ py -3 -m pip install drfkwargs
```

<br>

## Quick example
```py
import django.contrib.auth.models

import rest_framework.serializers

import drfkwargs


class UserSerializer(rest_framework.serializers.ModelSerializer):

    class Meta:
        model = django.contrib.auth.models.User
        fields = rest_framework.serializers.ALL_FIELDS
        extra_kwargs = {
            model.password.field.name: {drfkwargs.WRITE_ONLY: True},
            model.user_permissions.field.name: {drfkwargs.WRITE_ONLY: True},
            model.groups.field.name: {drfkwargs.WRITE_ONLY: True},
        }
```

<br>

## Class-based kwargs
For more readability you can use class-based keyword argument sets,
which are classes providing the set of the kwargs names available for a serializer.
Going with this, it's possible to replace `drfkwargs.INPUT_FORMATS` with `drfkwargs.DateFieldKwargs.INPUT_FORMATS`.
These two are the equivalents, but the second one provides more information about what is this kwarg

> [!NOTE]
> Every serializer provided by `DRF` has its own class-based kwarg set 

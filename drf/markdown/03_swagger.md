[toc]

---

# DRF - swagger

> https://github.com/axnsan12/drf-yasg
>
> https://swagger.io/

- API를 설계하고 문서화 하는데 도움을 주는 라이브러리

<br>

## 설치 및 등록

```bash
$ pip install drf-yasg
```

```bash
# settings.py

INSTALLED_APPS = [
   ...
   'drf_yasg',
   ...
]
```

<br>

---

<br>

### url 설정

```python
# articles/urls.py

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from . import views


schema_view = get_schema_view(
   openapi.Info(
        title='My API',
        default_version='v1',
        # 주석은 선택 인자입니다.
        # description="API 서비스입니다.",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="edujunho.hphk@gmail.com"),
        # license=openapi.License(name="SSAFY License"),
   ),
)

urlpatterns = [
    ...,
    path('swagger/', schema_view.with_ui('swagger')),
]
```

- http://127.0.0.1:8000/api/v1/swagger/ 확인
- 더 많은 기능들은 https://drf-yasg.readthedocs.io/en/stable/를 참고하여 도전



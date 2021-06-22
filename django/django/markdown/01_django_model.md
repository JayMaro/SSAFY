[TOC]

# 01_django_model

## Model

> 웹 어플리케이션의 데이터를 구조화하고 조작하기 위한 도구

**개념**

- 모델은 단일한 데이터에 대한 정보를 가짐
- 일반적으로 각각의 **모델(클래스)**는 하나의 데이터베이스 **테이블과 매핑**
- 모델은 부가적인 메타데이터를 가진 **DB의 구조(layout)를 의미**

<br>

### Database

> 체계화된 데이터의 모임 (집합)

**기본 구조**

- `쿼리(Query)`
  - 데이터를 조회하기 위한 명령어
  - (주로 테이블형 자료구조에서) 조건에 맞는 데이터를 추출하거나 조작하는 명령어
- `스키마 (Schema)` —> 뼈대(Structure)
  - 데이터베이스에서 자료의 구조, 표현 방법, 관계 등을 정의한 구조
  - 데이터베이스 관리 시스템(DBMS)이 주어진 설정에 따라 데이터베이스 스키마를 생성하며, 데이터베이스 사용자가 자료를 저장, 조회, 삭제, 변경할 때 DBMS는 자신이 생성한 데이터베이스 스키마를 참조하여 명령을 수행
- `테이블 (Table)` —> 관계(Relation) —> 엑셀의 sheet
  - 필드(field) : 속성, 컬럼(Column)
    - 모델 안에 정의한 클래스에서 클래스 변수가 필드가 됨
  - 레코드(record) : 튜플, 행(Row)
    - 우리가 ORM을 통해 해당하는 필드에 넣은 데이터(값)

<br>

------

<br>

### ORM

> 객체-관계 매핑

**개념**

- 객체 지향 프로그래밍 언어를 사용하여 호환되지 않는 유형의 시스템간에(Django - SQL)데이터를 변환하는 프로그래밍 기술
- OOP 프로그래밍에서 RDBMS을 연동할 때, 데이터베이스와 객체 지향 프로그래밍 언어 간의 호환되지 않는 데이터를 변환하는 프로그래밍 기법이다. 
- Django는 내장 Django ORM을 사용

<br>

**장/단점**

- 장점
  - SQL을 몰라도 DB 연동이 가능하다. (SQL 문법을 몰라도 쿼리 조작 가능)
  - SQL의 절차적인 접근이 아닌 객체 지향적인 접근으로 인해 `생산성`이 증가한다.
  - ORM은 독립적으로 작성되어 있고, 해당 객체들을 재활용할 수 있다. 
    - 때문에 모델에서 가공된 데이터를 컨트롤러(view)에 의해 뷰(template)과 합쳐지는 형태로 디자인 패턴을 견고하게 다지는데 유리
- 단점
  - ORM 만으로 완전한 서비스를 구현하기 어려운 경우가 있다.
  - 프로젝트의 복잡성이 커질 경우 설계 난이도가 상승할 수 있다.

<br>

**정리**

- 객체 지향 프로그래밍에서 DB를 편리하게 관리하게 위해 ORM 프레임워크를 도입
- **"우리는 DB를 객체(object)로 조작하기 위해 ORM을 사용한다."**

<br>

**새 프로젝트 시작**

> `01_django_model` 폴더 안에서 진행

```bash
$ django-admin startproject crud 
$ cd crud
$ python manage.py startapp articles
```

```python
# crud/settings.py

INSTALLED_APPS = [
    'articles',	
		...
]
```

<br>

**models.py 정의**

```python
# articles/models.py

class Article(models.Model): # Model class 상속
    # id는 기본적으로 처음 테이블 생성시 자동으로 만들어진다.
    title = models.CharField(max_length=10) # 클래스 변수(DB의 필드)
    content = models.TextField() 
```

- title과 content은 모델의 필드를 나타냄
  - 각 **필드**는 클래스 속성으로 지정되어 있으며, 각 **속성**은 각 데이터베이스의 열에 매핑

<br>

**사용 된 필드**

- `CharField(max_length=None, **options)`
  - 길이의 제한이 있는 문자열을 넣을 때 사용
  - CharField의 max_length는 필수 인자
    - **필드의 최대 길이(문자),** 데이터베이스 레벨과 Django의 유효성 검사(값을 검증하는 것)에서 활용
- `TextField(**options)`
  - 글자의 수가 많을 때 사용

<br>

------

<br>

## Migrations

>  django가 모델에 생긴 변화(필드를 추가했다던가 모델을 삭제했다던가 등)를 반영하는 방법

<br>

**makemigrations**

> migration 파일은 데이터베이스 스키마를 위한 버전관리 시스템이라 생각하자

- 모델을 변경한 것에 기반한 새로운 migration(설계도, 이하 마이그레이션)만들 때 사용
- 모델을 활성화 하기 전에 DB 설계도(마이그레이션) 작성

```bash
$ python manage.py makemigrations
```

- `0001_initial.py` 생성 확인

<br>

**migrate**

> 설계도를 실제 DB에 반영하는 과정

- `migrate` 는 `makemigrations` 로 만든 설계도를 실제 `db.sqlite3` DB에 반영한다.

- 모델에서의 변경 사항들과 DB의 스키마가 동기화를 이룬다.

  ```bash
  $ python manage.py migrate
  ```

<br>

**sqlmigrate**

- 해당 migrations 설계도가 SQL 문으로 어떻게 해석되어서 동작할지 미리 확인 할 수 있다.

  ```bash
  $ python manage.py sqlmigrate app_name 0001
  ```

<br>

**showmigrations**

- migrations 설계도들이 migrate 됐는지 안됐는지 여부를 확인 할 수 있다.

  ```bash
  $ python manage.py showmigrations
  ```


<br>

**변경사항 반영**

```python
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

```bash
$ python manage.py makemigrations
```

<br>

```bash
You are trying to add the field 'created_at' with 'auto_now_add=True' to article without a default; the database needs something to populate existing rows.

 1) Provide a one-off default now (will be set on all existing rows)
 2) Quit, and let me add a default in models.py
Select an option: 1
```

- `1` 입력 후 enter (추가된 필드에 대한 default 값 설정)

<br>

```bash
Please enter the default value now, as valid Python
You can accept the default 'timezone.now' by pressing 'Enter' or you can provide another value.
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
[default: timezone.now] >>>
```

- 그대로 `enter` (django가 timezone.now를 default 함수 값으로 자동 설정)

```bash
$ python manage.py migrate
```

<br>

`DateTimeField()`

- 최초 생성 일자: `auto_now_add=True`
  - django ORM이 최초 insert(테이블에 데이터 입력)시에만 현재 날짜와 시간으로 갱신(테이블에 어떤 값을 최초로 넣을 때)
- 최종 수정 일자: `auto_now=True`
  - django ORM이 save를 할 때마다 현재 날짜와 시간으로 갱신

<br>

**Model 중요 3단계**

- `models.py` : 변경사항 발생 (생성 / 수정)
- `makemigrations` : migration 파일 만들기 (설계도)
- `migrate` : DB에 적용 (테이블 생성)

<br>

**실제 DB 테이블 확인**

- vs code extension - sqlite3 검색 후 설치

- 테이블을 확인해보면 `articles_article`이라는 이름으로 테이블 생성

  - INSTALLED_APPS 중 몇몇은 최소 하나 이상의 DB 테이블을 사용하기 때문에 migrate 와 함께 테이블이 만들어진다.

  - 테이블의 이름은 app의 이름과 model 의 이름이 조합(모두 소문자)되어 자동으로 생성된다. (소문자)

    - `app이름(articles)_소문자 모델이름(article)`


<br>

------

<br>

## Database API

> DB를 조작하기 위한 도구
>
> django가 기본적으로 orm을 제공함에 따른 것으로 db를 편하게 조작할 수 있도록 도와줌

<br>

**Django shell**

- 일반 파이썬 쉘을 통해서는 장고 프로젝트 환경에 접근할 수 없음

- 그래서 장고 프로젝트 설정이 로딩된 파이썬 쉘을 활용

  ```bash
  $ pip install ipython django-extensions
  ```

  ```python
  # settings.py
  
  INSTALLED_APPS = [
      ...
      'django_extensions',
      ...
  ]
  ```

  ```bash
  $ python manage.py shell_plus
  ```

<br>

**DB API 구문**

> https://docs.djangoproject.com/en/3.1/ref/models/querysets/#queryset-api-reference
>
> https://docs.djangoproject.com/en/3.1/topics/db/queries/#making-queries

<img width="1517" alt="Screen Shot 2020-08-19 at 5 12 04 PM" src="https://user-images.githubusercontent.com/18046097/90609518-23395b80-e23f-11ea-8e04-abfc04a709f7.png">

<br>

**`objects` Manager**

> https://docs.djangoproject.com/en/3.1/topics/db/managers/#managers
>
> Django 모델에 데이터베이스 쿼리 작업이 제공되는 인터페이스

- Model Manager와 Django Model 사이의 **Query 연산의 인터페이스 역할** 을 해줌
- 즉, `models.py` 에 설정한 클래스(테이블)을 불러와서 사용할 때 DB와의 interface 역할을 하는 매니저
- Django는 기본적으로 모든 Django 모델 클래스에 대해 '`objects`' 라는 Manager(django.db.models.Manager) 객체를 자동으로 추가한다.
- Manager(objects)를 통해 특정 데이터를 조작(메서드)할 수 있다.

<br>

**QuerySet**

> 데이터베이스로부터 데이터를 읽고, 필터를 걸거나 정렬 등을 수행
>
> 쿼리(질문)를 DB에게 던져서 글을 읽거나, 생성하거나, 수정하거나, 삭제

- 데이터베이스에서 전달 받은 객체의 목록
- django orm에서 발생한 자료형
- objects를 사용하여 복수의 데이터를 가져오는 함수를 사용할 때 반환되는 객체
- 단일한 객체를 리턴할 때는 테이블(Class)의 인스턴스로 리턴됨

<br>

### CRUD

> 대부분의 컴퓨터 소프트웨어가 가지는 기본적인 데이터 처리 기능인 
> Create(생성), Read(읽기), Update(갱신), Delete(삭제)를 묶어서 일컫는 말
>
> 이러한 4개의 조작을 모두 할 수 없다면 그 소프트웨어는 완전하다고 할 수 없다. 
>
> 이들 기능은 매우 기본적이기 때문에, 한 묶음으로 설명되는 경우가 많다.
>
> https://ko.wikipedia.org/wiki/CRUD

<br>

### Create

> django shell_plus에서 진행

**데이터 객체를 만드는(생성하는) 3가지 방법**

**첫번째 방식**

- ORM을 쓰는 이유는 DB 조작을 객체 지향 프로그래밍(클래스)처럼 하기 위해
  - `article = Article()` :  클래스로부터 인스턴스 생성
  - `article.title` : 해당 인스턴스 변수를 변경
  - `article.save()` : 인스턴스로 메소드를 호출

```python
>>> article = Article() 
>>> article
<Article: Article object (None)>

>>> article.title = 'first' 
>>> article.content = 'django!' 

# save 를 하지 않으면 아직 DB에 값이 저장되지 않음
>>> article
<Article: Article object (None)>

>>> Article.objects.all()                            
<QuerySet []>

# save 를 하고 확인하면 저장된 것을 확인할 수 있다
>>> article.save()
>>> article
<Article: Article object (1)>
>>> Article.objects.all()
<QuerySet [Article: Article object (1)]>

# 인스턴스인 article을 활용하여 변수에 접근해보자
>>> article.title
'first'
>>> article.content
'django!'
```

<br>

**두번째 방식**

```python
>>> article = Article(title='second', content='django!!')
>>> article.save()
>>> article
<Article: Article object (2)>
>>> Article.objects.all()
<QuerySet [<Article: Article object (1)>, <Article: Article object (2)>]>

# 값을 확인
>>> article.pk
2
>>> article.title
'second'
>>> article.content
'django!!'
```

<br>

**세번째 방식**

- `create()` 를 사용하면 쿼리셋 객체를 생성하고 저장하는 로직이 한번의 스텝으로 가능

```python
>>> Article.objects.create(title='third', content='django!')
<Article: Article object (3)>
```

<br>

`__str__`

- 모든 모델마다 표준 파이썬 클래스의 메소드인 **str**() 을 정의하여 각각의 object가 사람이 읽을 수 있는 문자열을 반환(return)하도록 한다.

  ```python
  # articles/models.py
  
  class Article(models.Model):
      title = models.CharField(max_length=10)
      content = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  
      def __str__(self):
          return self.title
  ```

<br>

**`save()`**

> https://docs.djangoproject.com/en/3.1/ref/models/instances/#saving-objects

- `.save()` 메서드 호출을 통해 데이터를 DB에 저장한다.

<br>

### Read

`all()`

> https://docs.djangoproject.com/en/3.1/ref/models/querysets/#all

- `QuerySet` return
- QuerySet은 리스트는 아니지만 리스트와 거의 비슷하게 동작

```python
>>> Article.objects.all()
<QuerySet [<Article: Article object (1)>, <Article: Article object (2)>, <Article: Article object (3)>, <Article: Article object (4)>]>
get()
```

<br>

`get()`

>  https://docs.djangoproject.com/en/3.1/ref/models/querysets/#get

- 객체가 없으면 `DoesNotExist` 에러가 나오고 객체가 여러 개일 경우에 `MultipleObjectReturned` 오류를 띄움.
- 위와 같은 특징을 가지고 있기 때문에 unique 혹은 Not Null 특징을 가지고 있으면(ex. `pk`) 사용할 수 있다.

```python
>>> article = Article.objects.get(pk=100)
DoesNotExist: Article matching query does not exist.

>>> Article.objects.get(content='django!')
MultipleObjectsReturned: get() returned more than one Article -- it returned 2!
**filter()**
```

<br>

`filter()`

>  https://docs.djangoproject.com/en/3.1/ref/models/querysets/#filter

- 지정된 조회 매개 변수와 일치하는 객체를 포함하는 새 QuerySet을 반환

  ```python
  >>> Article.objects.filter(content='django!')
  <QuerySet [<Article: first>, <Article: fourth>]>
  
  >>> Article.objects.filter(title='first')
  <QuerySet [<Article: first>]>
  ```

<br>

**Field lookups**

- SQL WHERE 절을 지정하는 방법

- QuerySet 메서드 filter(), exclude() 및 get()에 대한 키워드 인수로 지정

  ```python
  Article.objects.filter(pk__gt=1)
  ```

<br>

**The `pk` lookup shortcut**

> https://docs.djangoproject.com/en/3.1/topics/db/queries/#the-pk-lookup-shortcut

- 또한, 우리가 `.get(id=1)` 형태 뿐만 아니라 `.get(pk=1)` 로 사용할 수 있는 이유는(DB에는 id로 필드 이름이 지정 됨에도) `.get(pk=1)` 이`.get(id__exact=1)` 와 동일한 의미이기 때문이다. 

- pk는 `id__exact` 의 shortcut 이다.

  ```python
  >>> Blog.objects.get(id__exact=14) # Explicit form
  >>> Blog.objects.get(id=14) # __exact is implied
  >>> Blog.objects.get(pk=14) # pk implies id__exact
  ```

<br>

### Update

```python
>>> article = Article.objects.get(pk=1)
>>> article.title
'first'

# 값을 변경하고 저장
>>> article.title = 'byebye'
>>> article.save()

# 정상적으로 변경된 것을 확인
>>> article.title
'byebye'
```

<br>

### Delete

```python
>>> article = Article.objects.get(pk=1)

# 삭제
>>> article.delete()
(1, {'articles.Article': 1})

# 다시 1번 글을 찾으려고 하면 없다고 나온다.
>>> Article.objects.get(pk=1)
DoesNotExist: Article matching query does not exist.
```

<br>

---

<br>

## Admin Site

> 사용자가 아닌 서버의 관리자가 활용하기 위한 페이지 

**개념**

- 사용자가 아닌 서버의 관리자가 활용하기 위한 페이지
-  Article class를 `admin.py` 에 등록하고 관리
- record 생성 여부 확인에 매우 유용하고 CRUD 로직을 확인하기에 편리하다.

<br>

**관리자 생성**

```bash
$ python manage.py createsuperuser
```

- 관리자 계정 생성 후 서버를 실행한 다음 `/admin` 으로 가서 관리자 페이지 로그인

- 모델을 등록하지 않으면 기본적인 사용자 정보만 확인 할 수 있다.

- `admin.py` 로 가서 관리자 사이트에 등록하여 내가 만든 record를 보기 위해서는 Django 서버에 등록


<br>

**model 등록**

```python
# articles/admin.py

from django.contrib import admin
from .models import Article

admin.site.register(Article)
```

<br>

**admin site확인**

- admin 사이트에 방문해서 우리가 현재까지 작성한 글들을 확인
- `admin.py` 는 관리자 사이트에 Article 객체가 관리 인터페이스를 가지고 있다는 것을 알려주는 것
- 이렇게 admin 사이트에 등록된 모습이 어딘가 익숙하다? 
- 바로 `models.py` 에 정의한 `__str__` 의 형태로 객체가 표현된다.

<br>

**ModelAdmin options**

`list_display`

- admin 페이지에서 우리가 models.py 정의한 각각의 속성(컬럼)들의 값(레코드)를 출력

  ```python
  # articles/admin.py
  
  from django.contrib import admin
  from .models import Article
  
  class ArticleAdmin(admin.ModelAdmin):
      list_display = ('pk', 'title', 'content', 'created_at', 'updated_at',)
  
  admin.site.register(Article, ArticleAdmin)
  ```

<br>

------


[TOC]

# 08_django_model_relationship

> https://docs.djangoproject.com/en/3.1/ref/models/fields/#module-django.db.models.fields

## User - Article

```python
# articles/models.py

from django.conf import settings


class Article(models.Model)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ...
```

```bash
$ python manage.py makemigrations
```

```bash
# 첫번째 상황(null 값이 허용되지 않는 user_id 가 아무 값도 없이 article 에 추가되려 하기 때문)
$ python manage.py makemigrations
You are trying to add a non-nullable field 'user' to article without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option: # 1 입력하고 enter

# 두번째 상황(그럼 기존 article 의 user_id 로 어떤 데이터를 넣을건지 물어봄)
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
>>> # 1 입력하고 enter (그럼 현재 작성된 모든 글은 1번 user가 작성한 것으로 됨)
```

```bash
$ python manage.py migrate
```

<br>

- 게시글을 작성하려 하면 user 를 선택 해야하는 불필요한 field 가 노출된다. 

- 제목과 내용만 입력하도록 필드를 설정해야한다.

  ```python
  # articles/forms.py
  
  class ArticleForm(forms.ModelForm):
      
      class Meta:
          model = Article
          fields = ('title', 'content',)
  ```

  - 글을 작성해보면 create 시에 유저 정보가 저장되지 않기 때문에 다음과 같은 에러가 발생한다.
    - `NOT NULL constraint failed: articles_article.user_id`

<br>

### CREATE

- `request.user` 라는 현재 요청의 유저 객체를 추가로 저장한다.

  ```python
  # articles/views.py
  
  @login_required
  @require_http_methods(['GET', 'POST'])
  def create(request):
      if request.method == 'POST':
          form = ArticleForm(request.POST)
          if form.is_valid():
              article = form.save(commit=False)
              article.user = request.user
              article.save()
              return redirect('articles:detail', article.pk)
  ```

<br>

### READ

- 게시글을 작성한 user가 누구인지 보기 위해 `index.html` 수정

  ```django
  <!-- articles/index.html -->
  
  {% extends 'base.html' %}
  
  {% block content %}
    ...
    {% for article in articles %}
      <p><b>작성자 : {{ article.user }}</b></p>
      <p>글 번호 : {{ article.pk }}</p>
      <p>글 제목 : {{ article.title }}</p>
      <p>글 내용 : {{ article.content }}</p>
      <a href="{% url 'articles:detail' article.pk %}">DETAIL</a>
      <hr>
    {% endfor %}
  {% endblock %}
  ```

<br>

### UPDATE

- 사용자가 자신의 글만 수정 할 수 있도록 수정

  ```python
  # articles/views.py
  
  
  @login_required
  @require_http_methods(['GET', 'POST'])
  def update(request, pk):
      article = get_object_or_404(Article, pk=pk)
      if request.user == article.user:
          if request.method == 'POST':
              form = ArticleForm(request.POST, instance=article)
              if form.is_valid():
                  form.save()
                  return redirect('articles:detail', article.pk)
          else:
              form = ArticleForm(instance=article)
      else:
          return redirect('articles:index')
      context = {
          'form': form,
      }
      return render(request, 'articles/update.html', context)
  ```


<br>

### DELETE

- 사용자가 자신의 글만 삭제 할 수 있도록 수정

```python
# articles/views.py

@require_POST
def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.is_authenticated:
        if request.user == article.user:
            article.delete()
            return redirect('articles:index')
    return redirect('articles:detail', article.pk)
```

- 해당 게시글의 작성가 아니라면, 수정/삭제 버튼을 출력하지 않도록 수정

```django
<!-- articles/detail.html -->

{% extends 'base.html' %}
{% block content %}
  ...
  {% if request.user == article.user %}
    <a href="{% url 'articles:update' article.pk %}" class="btn btn-primary">[UPDATE]</a>
    <form action="{% url 'articles:delete' article.pk %}" method="POST">
      {% csrf_token %}
      <button class="btn btn-danger">DELETE</button>
    </form>
  {% endif %}
...
```

<br>

---

<br>

## User - Comment

```python
# articles/models.py

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ...
```

```bash
$ python manage.py makemigrations

# 첫번째 상황(null 값이 허용되지 않는 user_id 가 아무 값도 없이 comment 에 추가되려 하기 때문)
You are trying to add a non-nullable field 'user' to comment without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option: # 1 입력하고 enter

# 두번째 상황 (그럼 기존 comment 의 user_id 로 뭘 넣을건지 물어봄)
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
>>> # 1 입력하고 enter (모든 댓글의 작성자를 1번 user로 하게 됨)

Migrations for 'articles':
  articles\migrations\0003_comment_user.py
    - Add field user to comment
```

```bash
$ python manage.py migrate
```

<br>

### CREATE

- 해당 view 함수를 요청한 유저의 정보를 넣고나서 저장한다. (로그인 사용자만 작성하도록)

  ```python
  # articles/views.py
  
  @require_POST
  def comments_create(request, pk):
      if request.user.is_authenticated:
          article = get_object_or_404(Article, pk=pk)
          comment_form = CommentForm(request.POST)
          if comment_form.is_valid():
              comment = comment_form.save(commit=False)
              comment.article = article
              comment.user = request.user
              comment.save()
              return redirect('articles:detail', article.pk)
          ...
  ```

<br>

### READ

- 비로그인 유저는 댓글 작성 form 을 볼 수 없도록 한다.

  ```django
  <!-- articles/detail.html -->
  
  {% extends 'base.html' %}
  {% block content %}
    ...
  <hr>
    {% if request.user.is_authenticated %}
      <form action="{% url 'articles:comments_create' article.pk %}" method="POST">
        {% csrf_token %}
        {{ comment_form }}
        <input type="submit">
      </form>
    {% else %}
      <a href="{% url 'accounts:login' %}">[댓글을 작성하려면 로그인하세요.]</a>
    {% endif %}
  {% endblock  %}
  ```
  
```python
  # articles/forms.py
  
  class CommentForm(forms.ModelForm):
  
      class Meta:
          model = Comment
          exclude = ('article', 'user',)
  ```
  
- 댓글 작성자 출력

  ```django
  <!-- articles/detail.html -->
  
  {% extends 'base.html' %}
  
  {% block content %}
    ...
    <h4>댓글 목록</h4>
    ...
    <ul>
      {% for comment in comments %}
        <li>
          {{ comment.user }} - {{ comment.content }}
          <form action="{% url 'articles:comments_delete' article.pk comment.pk %}" method="POST" class="d-inline">
            {% csrf_token %}
            <input type="submit" value="DELETE">
          </form>
        </li>
      {% empty %}
        <p>아직 댓글이 없네요...</p>
      {% endfor %}
    </ul>
    <hr>
    ...
  {% endblock %}
  ```

<br>

### DELETE

- 본인이 작성한 댓글만 삭제할 수 있도록 수정한다.

  ```python
  # articles/views.py
  
  @require_POST
  def comments_delete(request, article_pk, comment_pk):
      if request.user.is_authenticated:
          comment = get_object_or_404(Comment, pk=comment_pk)
          if request.user == comment.user:
              comment.delete()
      return redirect('articles:detail', article_pk)
  ```

  ```django
  <!-- articles/detail.html -->
  
  {% extends 'articles/base.html' %}
  {% block content %}
    ...
    <h4>댓글 목록</h4>
    ...
    <ul>
      {% for comment in comments %}
        <li>
          {{ comment.user }} - {{ comment.content }}
          {% if request.user == comment.user %}
            <form action="{% url 'articles:comments_delete' article.pk comment.pk %}" method="POST" class="d-inline">
              {% csrf_token %}
              <input type="submit" value="DELETE">
            </form>
          {% endif %}
        </li>
      {% empty %}
        <p>아직 댓글이 없네요...</p>
      {% endfor %}
    </ul>
    <hr>
    ...
  {% endblock %}
  ```

  - 본인 댓글에 대한 삭제 버튼을 볼 수 있도록 수정한다.
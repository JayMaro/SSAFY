[toc]

---

# DRF - many_to_one

> 요청 및 테스트는 [POSTMAN](https://www.postman.com/downloads/)을 사용합니다.
>
> https://www.django-rest-framework.org/

<br>

## Comment 모델 준비

```bash
# models.py

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

```bash
$ python manage.py makemigrations
$ python manage.py migrate

$ python manage.py seed articles --number=20
Seeding 20 Articles
Seeding 20 Comments
```

<br>

---

<br>

### GET - List 

- Article List와 비교하며 작성

```python
# serializers.py

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
```

```python
# urls.py

urlpatterns = [
	  ...,
    path('comments/', views.comment_list),
]
```

```python
# views.py

from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer


@api_view(['GET'])
def comment_list(request):
    comments = get_list_or_404(Comment)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
```

- http://127.0.0.1:8000/api/v1/comments/ 확인

<br>

### GET - Detail 

```python
# urls.py

urlpatterns = [
    ...,
    path('comments/<int:comment_pk>/', views.comment_detail),
]
```

```python
# views.py

@api_view(['GET'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)
```

<br>

---

<br>

### POST

- Article 생성과 달리 Create는 생성시 모델관계 객체가 필요

```python
# urls.py

urlpatterns = [
    ...,
    path('articles/<int:article_pk>/comments/', views.comment_create),
]
```

```python
# views.py

@api_view(['POST'])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data) 
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

<br>

**Passing Additional attributes to `.save()`**

- `save()` 메서드는 특정 Serializer 인스턴스를 저장하는 과정에서 추가적인 데이터를 받을 수 있음
- `CommentSerializer`를 통해 Serializing되는 과정에서 Query String Parameter로 넘어온 `article_pk`에 해당하는 article 객체를 추가적인 데이터를 넘겨 저장
- 이제 어떠한 게시글에 속하는 데이터인지 명시하여 데이터 요청을 하지 않아도 댓글 작성 가능

```python
# views.py

@api_view(['POST'])
def create_comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

http://127.0.0.1:8000/api/v1/articles/1/comments/ 댓글 작성 시도 후 에러 응답 확인

```json
{
    "article": [
        "This field is required."
    ]
}
```

- CommentSerializer에서 article field 데이터 또한 받도록 설정되어 있기 때문

<br>

**읽기 전용 필드 설정**

> https://www.django-rest-framework.org/api-guide/serializers/#specifying-read-only-fields

- `read_only=True` 속성을 사용하여 각 필드를 명시적으로 추가하는 대신 `read_only_fields`를 사용할 수 있음
- `form-data`로 데이터를 전송하는 시점에 article을 포함시키지 않도록 설정

```python
# serializers.py

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article',)
```

http://127.0.0.1:8000/api/v1/articles/1/comments/ 댓글작성 성공 확인

<br>

### DELETE & PUT

- article과 마찬가지로 comment_detail 함수가 모두 처리

```python
# views.py

@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        data = {
            'delete': f'댓글 {comment_pk}번이 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
```

<br>

---

<br>

## 1:N - Serializer

1. 특정 게시글에 작성된 댓글 목록 출력 (기존 필드 override)
2. 특성 게시글에 작성된 댓글의 개수 (새로운 필드 추가)

<br>

### 기존 필드 override

> 게시글에 달린 댓글 목록 출력 - Article Detail

- Serializer는 기존 필드를 override 하거나 추가적인 필드를 구성할 수 있음

<br>

1. PrimaryKeyRelatedField

   - pk를 사용하여 관계된 대상을 나타냄
   - 필드가 to many relationship을 나타내는 데 사용되는 경우 `many=True` 속성이 필요
   - `comment_set` 필드 값을 form-data로 받지 않으므로 `read_only=True` 작성

   ```python
   # serializers.py
   
   class ArticleSerializer(serializers.ModelSerializer):
       comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
   
       class Meta():
           model = Article
           fields = '__all__'
   ```

2. Nested relationships

   - 모델 관계 상으로 참조 된 대상은 참조하는 대상의 표현에 포함되거나 중첩(nested)될 수 있음
   - 이러한 중첩된 관계는 **serializers를 필드로 사용**하여 표현 할 수 있음

   ```python
   # serializers.py
   
   class CommentSerializer(serializers.ModelSerializer):
   
       class Meta:
           model = Comment
           fields = '__all__'
           read_only_fields = ('article',)
   
   
   class ArticleSerializer(serializers.ModelSerializer):
       comment_set = CommentSerializer(many=True, read_only=True)
   
       class Meta:
           model = Article
           fields = '__all__'
   ```

   - 두 클래스의 상하위치 변경

<br>

### 추가 필드 작성

> 게시글에 작성된 댓글 개수 - Article Detail
>
> https://www.django-rest-framework.org/api-guide/relations/#nested-relationships

- `comment_set`은 모델 관계로 인해 자동으로 구성되기 때문에 커스텀 필드를 구성하지 않아도 `comment_set`이라는 필드명을 `fields` 옵션에 작성만 해도 사용 가능함
- 하지만 `comment_count`의 경우 자동으로 구성되는 필드가 아니기 때문에 직접 필드를 추가해서 구성해야 함

```python
# serializers.py

class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
```

<br>

**`source` (serializers field's argument)**

> https://www.django-rest-framework.org/api-guide/fields/#source

- 필드를 채우는 데 사용할 속성의 이름
- 점 표기법(dotted notation)을 사용하여 속성을 탐색 할 수 있음
- `comment_set`이라는 필드에 `.` 을 통해 전체 댓글의 개수 확인(`.count()`는 built-in queryset API 중 하나)

<br>

---

|                      |      GET       |   POST    |      PUT      |    DELETE     |
| :------------------- | :------------: | :-------: | :-----------: | :-----------: |
| articles/            |  전체 글 조회  |  글 작성  | 전체 글 수정  | 전체 글 삭제  |
| articles/1/          |  1번 글 조회   |     .     |  1번 글 수정  |  1번 글 삭제  |
| comments/            | 전체 댓글 조회 |     .     |       .       |       .       |
| comments/1/          | 1번 댓글 조회  |     .     | 1번 댓글 수정 | 1번 댓글 삭제 |
| articles/1/comments/ |       .        | 댓글 작성 |       .       |       .       |
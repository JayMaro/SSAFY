import random
from faker import Faker


fake = Faker()

for i in range(5):
	User.objects.create_user(
		fake.user_name(),
		fake.email(),
		'1q2w3e4r!'
	)

for i in range(1, 11):
    Review.objects.create(
		title=f'테스트 {i}글',
    content=fake.text(),
    user_id=random.choice(range(1, 6)),
		rank=1,
    )
    
    for j in range(1, 11):
        Comment.objects.create(
            content=fake.sentence(),
            review_id=i,
            user_id=random.choice(range(1, 6))
        )

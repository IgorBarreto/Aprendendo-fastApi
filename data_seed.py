from PostDTO import PostDTO
from random import randint, choice

posts_seed = []


def postFactory(min_post=1, max_post=5):
    quantityPosts = randint(min_post, max_post + 1)
    for i in range(1, quantityPosts + 1):
        post = {
            "id": randint(0, 1000000),
            "title": f"Post {i}",
            "content": f"Conteudo {i}",
            "published": choice((True, False)),
            "rating": randint(1, 11),
        }
        posts_seed.append(post)
    posts_seed.append(
        {
            "id": 10000000,
            "title": "Meu post",
            "content": f"Meu conteudo",
            "published": True,
            "rating": 10,
        }
    )


postFactory()

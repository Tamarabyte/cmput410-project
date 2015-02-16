from django.db import models


class User(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=20)
    github_id = models.CharField(max_length=30, null=True)
    join_date = models.DateField('date joined', auto_now_add=True)
    follows = models.ManyToManyField('self', blank=True, related_name='followed_by', symmetrical=False)

    def __str__(self):
        return self.email

    # Two way following implies "real" friendship
    def getFriends(self):
        return self.follows.all() & self.followed_by.all()

    # Those which are following me but I am not following back
    def getFriendRequests(self):
        A = self.followed_by.all()
        B = self.follows.all()
        return A.exclude(pk__in=B)


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User)
    profile_image = models.ImageField(blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    privacy_level = models.IntegerField()
    text = models.TextField()


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    attached_to = models.ManyToManyField(Post)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)
    text = models.CharField(max_length=2048)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

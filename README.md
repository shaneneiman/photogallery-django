# Photo gallery

For this project, you are going to build a photo gallery application in Django. You should customize this application with your own features and ideas -- it is a real portfolio-quality project you should make your own. There are some requirements included below, along with ideas to spur your creativity and questions you should answer.

- User registration and login
    - **Idea**: Consider social login via [django-allauth](https://www.intenct.nl/projects/django-allauth/)
- Users can create photo galleries
    - These galleries have a title and photos within them
    - These galleries have a default photo -- the photo shown when looking at galleries
    - **Idea**: Make public and private galleries
    - **Idea**: Can galleries be shared so that multiple users can add photos to them?
- Users can upload photos
    - Consider whether photos need to be in a gallery or not. Can they be in multiple galleries? These are questions you need to answer.
    - Photos should have thumbnails. Look at [Django-Imagekit](https://github.com/matthewwithanm/django-imagekit) and see if it will work for your needs.
- Users have profiles where you can see their galleries
    - If you have public and private galleries, then don't show private galleries
    - What if you can have pictures not in galleries? How does that work?
    - This doesn't have to look like a list of galleries. This could be a series of updates, Facebook-style, for example.
    - **Idea**: Users can _pin_ or _spotlight_ photos or galleries to appear first.
- Users can leave comments on photos
    - When a user leaves a comment, the owner of the photo should get an email notifying them of that comment. (**Idea**: perhaps you don't get the email if you are both the owner and wrote the comment.)
- There is an API to interact with galleries and photos. This can be read-only or read-write.

In addition to these features, it is required that your application has a front-end to interact with it. This can be wholly Django views, Django views + JavaScript to enhance them (most likely), or wholly JavaScript + an API in Django.

Your application must be deployed to Heroku and use Amazon S3 to store images. You should use [Mailgun](https://elements.heroku.com/addons/mailgun) to send email in production.

## Resources

- [How to Setup Amazon S3 in a Django project](https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html) - This article is from 2017, and not 100% accurate any more, but is the best around.


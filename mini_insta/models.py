# File: mini_insta/models.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 10/10/2025
# Description: Defines what attributes the Mini Insta models 
# in the database should have.

from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """Encapsulate the data of a Mini Insta Profile."""

    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of this Profile model instance."""

        return f'{self.username} ({self.display_name})'
    
    def get_absolute_url(self):
        """Return a URL to display this Profile by default."""

        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_all_posts(self):
        """Return a QuerySet of all Posts on this Profile."""

        # Posts are ordered by newest first
        posts = Post.objects.filter(profile=self).order_by('-timestamp')

        return posts
    
    def get_followers(self):
        """Return a list of Profiles who follow this Profile."""
        
        follower_profile_list = []
        followers = Follow.objects.filter(profile=self)

        for f in followers:
            follower_profile_list.append(f.follower_profile)

        return follower_profile_list
    
    def get_num_followers(self):
        """Return how many Profiles follow this Profile."""

        return len(self.get_followers())
    
    def get_following(self):
        """Return a list of Profiles followed by this Profile."""

        following_profile_list = []
        following = Follow.objects.filter(follower_profile=self)

        for f in following:
            following_profile_list.append(f.profile)

        return following_profile_list
    
    def get_num_following(self):
        """Return how many Profiles this Profile follows."""

        return len(self.get_following())
    

class Post(models.Model):
    """Encapsulate the data of a Post on a Mini Insta Profile."""

    # the foreign key to indicate the relationship to the Profile of the creator of this post
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True) # the optional text associated with this post
    timestamp = models.DateTimeField(auto_now_add=True) # the time at which this post was created/saved

    def __str__(self):
        """Return a string representation of this Post model instance."""

        return f'{self.profile} | {self.caption}'
    
    def get_absolute_url(self):
        """Return a URL to display this Post by default."""

        return reverse('show_post', kwargs={'pk': self.pk})
    
    def get_all_photos(self):
        """Return a QuerySet of all Photos on this Post."""
    
        # Photos are ordered by newest first
        photos = Photo.objects.filter(post=self).order_by('-timestamp')

        return photos


class Photo(models.Model):
    """Encapsulate the data of an image on a Mini Insta post."""

    # the foreign key to indicate the relationship to the Post to which this Photo is associated
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True) # a valid URL to an image stored on the public world-wide web
    image_file = models.ImageField(blank=True) # an image stored as a media file
    timestamp = models.DateTimeField(auto_now_add=True) # the time at which this Photo was created/saved

    def __str__(self):
        """Return a string representation of this Photo model instance."""

        return f'{self.post.profile} | {self.post.caption} | Photo {self.pk}'
    
    def get_image_url(self):
        """Returns either the URL stored in the image_url attribute 
        (if it exists), or else the URL to the image_file attribute.
        If no photo exists, return None.
        """

        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
        else:
            return None
        

class Follow(models.Model):
    """Encapsulates the idea of an edge connecting two nodes within the 
    social network (e.g., when one Profile follows another Profile).
    """

    # which profile is being followed;
    # if a profile gets deleted, all its follows will be 'cleaned up' (as per models.CASCADE)
    profile = models.ForeignKey(Profile, related_name="profile", on_delete=models.CASCADE)

    # which profile is doing the following
    follower_profile = models.ForeignKey(Profile, related_name="follower_profile", on_delete=models.CASCADE)

    # the time at which the follower began following the other profile
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of this Follow model instance."""

        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'
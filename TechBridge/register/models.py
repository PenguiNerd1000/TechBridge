from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=80)
    website = models.URLField()
    address = models.CharField(max_length=100)
    

    class Meta:
        verbose_name_plural = 'Schools'
        ordering = ('name',)


    def __str__(self):
        return (self.name)

class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    bio = models.TextField(max_length=1000)
    img    = models.ImageField(upload_to='core/avatar', blank=True, default='core/avatar/blank_profile.png')
    friends = models.ManyToManyField('self', blank=True)
    is_member = models.BooleanField(default=False)
    
    def __str__(self):
        return (self.first_name + " " + self.last_name)

    def invite(self, invite_profile):
        invite = Invite(inviter=self, invited=invite_profile)
        invites = invite_profile.received_invites.filter(inviter_id=self.id)
        if not len(invites) > 0:    # don't accept duplicated invites
            invite.save()

    def remove_friend(self, profile_id):
        friend = User.objects.filter(id=profile_id)[0]
        self.friends.remove(friend)
    
class Member(User):
    volunteer_hours = models.IntegerField(default=0)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="students")
    
    class Meta:
        verbose_name_plural = 'Members'


class Invite(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='made_invites')
    invited = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invites')

    def accept(self):
        self.invited.friends.add(self.inviter)
        self.inviter.friends.add(self.invited)
        self.delete()

    def __str__(self):
        return str(self.inviter)

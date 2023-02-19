from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from api.localisation.models import Wilaya , Commune
from api.contacts.models import Contact
from django.utils  import timezone
class UserAccountManager(BaseUserManager):
    def create_user(self,email,prenom,nom,password=None,**extra_fields):
        if not email:
            raise ValueError('Users must have an adress email')
        if not prenom:
            raise ValueError("User must add a first name")
        if not nom:
            raise ValueError("User must add a last name")
        email = self.normalize_email(email)
        user=self.model(email=email,prenom=prenom,nom=nom,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        ############creation du contact d'utilisateur#############
        print("\n")
        print("\n")
        print(f'result: {user.pk}')
        print("\n")
        print("\n")
        contact = Contact(nom=nom+" "+prenom,email=email,utilisateur_id=user.pk)
        contact.save()
        print("\n\n welcome in user creation an his contact creation \n\n")
        return user 
    def create_superuser(self,email,prenom,nom,password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an adress email')
        if not prenom:
            raise ValueError("User must add a first name")
        if not nom:
            raise ValueError("User must add a last name")
        user=self.create_user(email,prenom,nom,password=password,**extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

def get_profile_image_filepath(self, filename):
      print("\n\n saving the new image \n\n")
      return 'profile_images/' + str(self.pk) + '/profile_image.png'  
class UserAccount(AbstractBaseUser,PermissionsMixin):
    username = None
    email = models.EmailField(max_length=255,unique=True)
    prenom = models.CharField(max_length=40)
    nom = models.CharField(max_length=40)
    date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    last_login=models.DateTimeField(verbose_name='last login', auto_now=True)
    hide_email=models.BooleanField(default=True)
    is_superuser= models.BooleanField(default=False)
    is_admin= models.BooleanField(default=False)
    is_logged_in= models.BooleanField(default=False)
    profile_image= models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,)
    
    ############################
    date_naissance=models.DateField(default=timezone.now, blank=True)
    wilaya = models.ForeignKey(Wilaya,on_delete=models.PROTECT,blank=True,null=True)
    commune = models.ForeignKey(Commune,on_delete=models.PROTECT,blank=True,null=True)
    numero_telephone=models.CharField(max_length=15,blank=True,null=True)
    #############################
    
    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['prenom','nom']
    
    def get_prenom(self):
        return self.prenom
    def get_nom(self):
        return self.nom
    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

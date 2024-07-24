from django.db import models
from account.models import User, Usine
from django.core.validators import MinValueValidator
from django.template.defaultfilters import slugify
from PIL import Image as PILImage
import os


class Setting(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=250)

    def __str__(self):
        return self.name + ' : ' + self.value

class Product(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.designation
    
class Emplacement(models.Model):
 
    REGION = [
        ('Ouest', 'Ouest'),
        ('Est', 'Est'),
        ('Centre', 'Centre'),
        ('Centre/Ouest', 'Centre/Ouest'),
    ]

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    designation = models.CharField(max_length=100)
    region = models.CharField(choices=REGION, max_length=20, default='Ouest')

    def __str__(self):
        return self.designation
    
class Complaint(models.Model):

    STATE_COMPLAINT = [
        ('Brouillon', 'Brouillon'),
        ('En traitement', 'En traitement'),
        ('Traité', 'Traité'),
        ('Clôturé', 'Clôturé'),
        ('Annulé', 'Annulé')
    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    state = models.CharField(choices=STATE_COMPLAINT, max_length=40)

    distributeur_id = models.IntegerField()
    distributeur = models.CharField(max_length=255)

    client_id = models.IntegerField()
    client = models.CharField(max_length=255)

    emplacement = models.ForeignKey(Emplacement, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    usine = models.ForeignKey(Usine, on_delete=models.CASCADE)

    project = models.CharField(max_length=500)
    n_bc = models.CharField(max_length=25)
    n_lot = models.CharField(max_length=25)
    qte = models.FloatField(default=0, validators=[MinValueValidator(0)])

    date_delivery = models.DateField()
    date_prod = models.DateField()
    observation = models.TextField(null=True, blank=True)

    treatment_labo = models.TextField(null=True, blank=True)
    treatment_site = models.TextField(null=True, blank=True)
    actions = models.TextField(null=True, blank=True)

    decision = models.TextField(null=True, blank=True)
    
    def cycles(self):
        return self.cycle_set.all()
    
    def images(self):
        return self.image_set.all()

    @property
    def n_reclamation(self):
        return f"{self.id:05d}/{self.date_created.strftime('%y')}"

    def __str__(self):
        return self.n_reclamation
    
def get_image_filename(instance, filename):
    title = instance.complaint.n_reclamation
    slug = slugify(title)
    return "complaint_images/%s-%s" % (slug, filename)  

class Image(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and os.path.exists(self.image.path):
            img = PILImage.open(self.image.path)
            max_size = (1280, 720)
            img.thumbnail(max_size, PILImage.LANCZOS)
            img.save(self.image.path, quality=50, optimize=True)
    
class Cycle(models.Model):

    STATE_COMPLAINT = [
        ('Brouillon', 'Brouillon'),
        ('En traitement', 'En traitement'),
        ('Traité', 'Traité'),
        ('Clôturé', 'Clôturé'),
        ('Annulé', 'Annulé')
    ]

    old_state = models.CharField(choices=STATE_COMPLAINT, max_length=40)
    new_state = models.CharField(choices=STATE_COMPLAINT, max_length=40)
    date = models.DateTimeField(auto_now_add=True) 
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)

    def __str__(self):
        return "Cycle - " + str(self.complaint.id) + " - " + str(self.date)
    
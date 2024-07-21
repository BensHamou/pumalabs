from django.db import models
from account.models import User, Usine
from django.core.validators import MinValueValidator

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

    def __str__(self):
        return self.designation
    
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
    
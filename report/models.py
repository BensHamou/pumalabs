from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import Usine, User, Horaire

class Poste(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    designation = models.CharField(max_length=100)
    code = models.CharField(max_length=100, null=True)
    usine = models.ForeignKey(Usine, on_delete=models.SET_NULL, null=True)
    header = models.CharField(max_length=100, null=True)
    sequence = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    active = models.BooleanField(default=True)
    
    def standards(self):
        return self.standard_set.all()
    
    def default_standard(self):
        return self.standard_set.filter(active=True).first()
    
    def __str__(self):
        return self.designation

class Fournisseur(models.Model):
    designation = models.CharField(max_length=100)
    
    def __str__(self):
        return self.designation
    
class SableType(models.Model):
    designation = models.CharField(max_length=100)
    
    def __str__(self):
        return self.designation
    
class Report(models.Model):
 
    STATE_REPORT = [
        ('Brouillon', 'Brouillon'),
        ('Confirmé', 'Confirmé'),
        ('Validé', 'Validé'),
        ('Refusé', 'Refusé'),
        ('Annulé', 'Annulé'),
    ]

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    state = models.CharField(choices=STATE_REPORT, max_length=40)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'Technicien'}, related_name='creator')
    usine = models.ForeignKey(Usine, on_delete=models.SET_NULL, null=True)
    shift = models.ForeignKey(Horaire, null=True, on_delete=models.SET_NULL)
    gp_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'Gestionnaire de production'}, related_name='gp_user')
    fournisseur = models.ForeignKey(Fournisseur, null=True, on_delete=models.SET_NULL)
    type_sable = models.ForeignKey(SableType, null=True, on_delete=models.SET_NULL)
   
    n_report = models.IntegerField()
    n_lot = models.IntegerField(null=True)
    date_prelev = models.DateTimeField()
    variateur = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    debit =  models.FloatField(default=0, validators=[MinValueValidator(0)])
    t_consigne =  models.FloatField(default=0)
    t_real =  models.FloatField(default=0)
    freq_b1 =  models.FloatField(default=0)
    variateur_b1 =  models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    freq_b2 =  models.FloatField(default=0)
    variateur_b2 =  models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    freq_b3 =  models.FloatField(default=0, null=True, blank=True)
    variateur_b3 =  models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    retour_2_5 = models.BooleanField(default=True)
    retour_1_3 = models.BooleanField(default=True)
    retour_0_6 = models.BooleanField(default=True)
    observation = models.TextField(null=True, blank=True)
    
    def validations(self):
        return self.validation_set.all()
    
    def samples(self):
        return self.sample_set.all()
    
    def __str__(self):
        return str(self.n_report) + " (" + str(self.date_created) +")"
    
class Sample(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    poste = models.ForeignKey(Poste, null=True, on_delete=models.SET_NULL)
    value_2_5 = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    value_1_25 = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    value_0_6 = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    value_0_3 = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    value_0_06 = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    value_0 = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    value_h = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.poste.designation + " (R" + str(self.report.id) +")"

class Standard(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    poste = models.ForeignKey(Poste, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    max_2_5_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_1_25_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_0_6_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_0_3_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_0_06_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    max_0_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    min_2_5_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    min_1_25_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    min_0_6_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    min_0_3_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    min_0_06_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    min_0_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.poste.designation + " - N° " + str(self.id) 

class Validation(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    STATE_REPORT = [
        ('Brouillon', 'Brouillon'),
        ('Confirmé', 'Confirmé'),
        ('Validé', 'Validé'),
        ('Refusé', 'Refusé'),
        ('Annulé', 'Annulé'),
    ]

    old_state = models.CharField(choices=STATE_REPORT, max_length=40)
    new_state = models.CharField(choices=STATE_REPORT, max_length=40)
    date = models.DateTimeField(auto_now_add=True) 
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    refusal_reason = models.TextField()
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return "Validation - " + str(self.report.id) + " - " + str(self.date)


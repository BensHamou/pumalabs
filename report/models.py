from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import Usine, User, Horaire

class Poste(models.Model):
    designation = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def standards(self):
        return self.standard_set.all()
    
    def __str__(self):
        return self.designation

class Report(models.Model):
 
    STATE_REPORT = [
        ('Brouillon', 'Brouillon'),
        ('Confirmé', 'Confirmé'),
        ('Validé par Validateur', 'Validé par TechnicienV'),
        ('Refusé par Validateur', 'Refusé par TechnicienV'),
        ('Annulé', 'Annulé'),
    ]
 
    SAND_TYPE = [
        ('Gris', 'Gris'),
        ('Blanc', 'Blanc'),
    ]

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    state = models.CharField(choices=STATE_REPORT, max_length=40)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'Technicien'})
    usine = models.ForeignKey(Usine, on_delete=models.SET_NULL, null=True)
    shift = models.ForeignKey(Horaire, null=True, on_delete=models.SET_NULL)
   
    n_report = models.IntegerField()
    date_prelev = models.DateTimeField()
    type_sable = models.CharField(choices=SAND_TYPE, max_length=40)
    variateur = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    debit =  models.FloatField(default=0, validators=[MinValueValidator(0)])
    t_consigne =  models.FloatField(default=0)
    t_real =  models.FloatField(default=0)
    freq_b1 =  models.FloatField(default=0)
    freq_b2 =  models.FloatField(default=0)
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
    
    poste = models.ForeignKey(Poste, null=True, on_delete=models.SET_NULL)
    value_2_5 = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    value_1_25 = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    value_0_6 = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    value_0_3 = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    value_0 = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    value_h = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.poste.designation + " (R" + str(self.report.id) +")"

class Standard(models.Model):

    poste = models.ForeignKey(Poste, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    max_2_5_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_1_25_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_0_6_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_0_3_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_0_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    min_2_5_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    min_1_25_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    min_0_6_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    min_0_3_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    min_0_value = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.poste.designation + " (R" + str(self.report.id) +")"

class Validation(models.Model):

    STATE_REPORT = [
        ('Brouillon', 'Brouillon'),
        ('Confirmé', 'Confirmé'),
        ('Validé par Validateur', 'Validé par TechnicienV'),
        ('Refusé par Validateur', 'Refusé par TechnicienV'),
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
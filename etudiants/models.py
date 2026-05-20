from django.db import models
from django.contrib.auth.models import User

class Etudiant(models.Model):
    FILIERES = [
        ('genie_logiciel', 'Génie logiciel'),
        ('gsi', 'GSI'),
        ('e_com', 'E-COM'),
        ('iwd', 'IWD'),
        ('iia', 'IIA'),
        ('bat', 'BAT'),
        ('autre', 'Autre'),
    ]

    STATUS = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='etudiant'
    )

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    filiere = models.CharField(
        max_length=50,
        choices=FILIERES,
        default='autre'
    )

    #FileField = champ pour uploader un fichier
    portfolio_fichier = models.FileField(
        upload_to='portfolio/',#fichier stockées dans media/portfolio
        blank=True,
        null=True
    )

    portfolio_lien = models.URLField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='en_attente'
    )

    date_inscription = models.DateTimeField(auto_now_add=True)

    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    class Meta:
        verbose_name = 'Etudiant'
        verbose_name_plural = 'Etudiants'
        ordering = ['-date_inscription']


from django.db import models
from account.models import Account, experiment, Enotebook
from cloudinary.models import CloudinaryField


class experimentData(models.Model):
    experiment = models.ForeignKey(experiment, on_delete=models.CASCADE)
    procedure = models.CharField(null=True, default=" ")
    tlc = models.ImageField(null=True)
    result = models.CharField(null=True, default=" ")


class reactionTable(models.Model):
    experimentData = models.OneToOneField(experimentData, on_delete=models.CASCADE)
    compound = models.CharField(null=True, default=" ")
    molecular_formula = models.IntegerField(null=True, blank=True)
    molecular_weight = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    moles = models.IntegerField(null=True, blank=True)
    ratio = models.IntegerField(null=True, blank=True)
    density = models.IntegerField(null=True, blank=True)


class reactionScheme(models.Model):
    experimentData = models.OneToOneField(experimentData, on_delete=models.CASCADE)
    catalyst = models.CharField(null=True, default=" ")
    solvent = models.CharField(null=True, default=" ")
    equation = models.CharField(null=True, default=" ")
    compound_images = CloudinaryField("image", null=True, blank=True)


class resultTable(models.Model):
    experimentData = models.OneToOneField(experimentData, on_delete=models.CASCADE)
    compound_id = models.CharField(null=True, default=" ")
    compound = models.CharField(null=True, default=" ")
    compound_amount = models.IntegerField(null=True, blank=True)
    compound_yield = models.IntegerField(null=True, blank=True)
    compund_moles = models.IntegerField(null=True, blank=True)
    compound_purity = models.IntegerField(null=True, blank=True)
    remarks = models.CharField(null=True, default=" ")


class analyticalData(models.Model):
    experimentData = models.OneToOneField(experimentData, on_delete=models.CASCADE)


def createNewExperimentInNotebook(expdata):
    reactionTable.objects.create(experimentData_id=expdata.id)
    resultTable.objects.create(experimentData_id=expdata.id)
    reactionScheme.objects.create(experimentData_id=expdata.id)
    analyticalData.objects.create(experimentData_id=expdata.id)
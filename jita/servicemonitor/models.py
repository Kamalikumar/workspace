# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class SmDclog(models.Model):
    entryid = models.IntegerField(primary_key=True)
    downstart = models.DateTimeField()
    downend = models.DateTimeField()
    totaltimedown = models.IntegerField()
    upstart = models.DateTimeField()
    upend = models.DateTimeField()
    totaltimeup = models.IntegerField()
    downby = models.CharField(max_length=10)
    upby = models.CharField(max_length=10)
    reason = models.CharField(max_length=100, blank=True, null=True)
    totaldowntime = models.IntegerField()
    type = models.CharField(max_length=1)
    createddate = models.DateTimeField()
    createdby = models.CharField(max_length=10, blank=True, null=True)
    modifieddate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sm_dclog'


class SmImpact(models.Model):
    entryid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=1)
    start = models.IntegerField()
    end = models.IntegerField()
    createddate = models.DateTimeField()
    createdby = models.CharField(max_length=10, blank=True, null=True)
    modifieddate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sm_impact'


class SmMstdependservices(models.Model):
    dependid = models.AutoField(primary_key=True)
    esid = models.IntegerField()
    affectingesid = models.IntegerField()
    createddate = models.DateTimeField()
    createdby = models.CharField(max_length=10, blank=True, null=True)
    modifieddate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sm_mstdependservices'


class SmMstmonitorwindow(models.Model):
    year = models.TextField(primary_key=True)  # This field type is a guess.
    weekday = models.CharField(max_length=2)
    weeklyoff = models.CharField(max_length=1)
    starttime = models.TimeField()
    endtime = models.TimeField()
    breaktime = models.TimeField()
    monitoringtime = models.TimeField()
    createddate = models.DateTimeField()
    createdby = models.CharField(max_length=10, blank=True, null=True)
    modifieddate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sm_mstmonitorwindow'


class SmMstservice(models.Model):
    status = models.BooleanField(default=1)
    esid = models.AutoField(primary_key=True)
    shortname = models.CharField(max_length=20)
    esname = models.CharField(max_length=30)
    category = models.CharField(max_length=1)
    minorcategory = models.CharField(max_length=15)
    importance = models.CharField(max_length=1)
    units = models.IntegerField()
    mis = models.CharField(max_length=3)  # This field type is a guess.
    plandowntime = models.IntegerField()
    expectuptime = models.IntegerField()
    acceptuptime = models.IntegerField()
    createddate = models.DateTimeField()
    createdby = models.CharField(max_length=10, blank=True, null=True)
    modifieddate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sm_mstservice'


class SmMstserviceuptime(models.Model):
    esid = models.IntegerField(primary_key=True)
    monthyear = models.DateField()
    expectuptime = models.IntegerField()
    plandowntime = models.IntegerField()
    acceptuptime = models.IntegerField()
    createddate = models.DateTimeField()
    createdby = models.CharField(max_length=10, blank=True, null=True)
    modifieddate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sm_mstserviceuptime'
        unique_together = (('esid', 'monthyear'),)


class SmTrnregister(models.Model):
    entryid = models.AutoField(primary_key=True)
    startdate = models.DateTimeField(auto_now=True)
    entryby = models.CharField(max_length=10)
    esid = models.ForeignKey(SmMstservice, models.DO_NOTHING, db_column='esid',null=True,blank=True)
    category = models.CharField(max_length=1)
    importance = models.CharField(max_length=1)
    description = models.CharField(max_length=50)
    downtypetime = models.CharField(max_length=1,null=True,blank=True)
    source = models.CharField(max_length=10)
    impact = models.CharField(max_length=1, blank=True, null=True)
    enddate = models.DateTimeField(null=True,blank=True)
    downtime = models.IntegerField(null=True,blank=True)
    closemailsent = models.IntegerField()
    closeby = models.CharField(max_length=10,null=True,blank=True)
    rc = models.CharField(max_length=255, blank=True, null=True)
    ca = models.CharField(max_length=255)
    mis = models.TextField()  # This field type is a guess.
    createddate = models.DateTimeField()
    createdby = models.CharField(max_length=10, blank=True, null=True)
    modifieddate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sm_trnregister'

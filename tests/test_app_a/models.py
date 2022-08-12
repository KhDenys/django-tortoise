from django.db import models


class ModelA(models.Model):
    id = models.AutoField(primary_key=True)
    binary = models.BinaryField()
    boolean = models.BooleanField()
    char = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
    datetime = models.DateTimeField(auto_now=True)
    decimal = models.DecimalField(max_digits=10, decimal_places=8)
    duration = models.DurationField()
    float = models.FloatField()
    ip = models.GenericIPAddressField()
    integer = models.IntegerField()
    small_int = models.SmallIntegerField()
    json = models.JSONField()
    positive_big_int = models.PositiveBigIntegerField()
    positive_int = models.PositiveIntegerField()
    positive_small_int = models.PositiveSmallIntegerField()
    slug = models.SlugField(max_length=20, db_index=True)
    text = models.TextField()
    time = models.TimeField(auto_now=True)
    url = models.URLField()
    uuid = models.UUIDField()


class ModelARel(models.Model):
    id = models.BigAutoField(primary_key=True)
    one = models.OneToOneField('ModelA', related_name='one', on_delete=models.CASCADE)
    foreign = models.ForeignKey('ModelA', related_name='foreigns', on_delete=models.SET_NULL, null=True)
    many = models.ForeignKey('ModelA', related_name='many', on_delete=models.SET_NULL, null=True)

from django.db import models

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

class Doc(models.Model):
    DOC_TYPE_CHOICES = (("D", "document"),
                 ("V", "video"),
                )
    name = models.CharField(max_length=100)
    doc_type = models.CharField(max_length=1, choices = DOC_TYPE_CHOICES)
    asset = models.FileField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return "%s (%s)" % (self.name, sizeof_fmt(self.asset.size))


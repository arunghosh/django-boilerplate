from django.db import models


class ModelBase(models.Model):

    def display_as_div(self, fields=None):
        ''' Display for model fields in div format
        '''
        result = ''
        for field in self._meta.fields:
            value =  getattr(self, field.name)
            is_excluded = fields and field.name not in fields
            if is_excluded or not value:
                continue
            result += '<div class="form-display">'
            result += '<div class="text">%s</div>' % field.verbose_name
            result += '<div class="value">%s</div>' % value
            result += '</div>'

        return result

    def display_as_table(self, fields=None):
        ''' Display for model fields in table format
        '''
        output = "<table>"
        for field in self._meta.fields:
            if fields and field.name not in fields:
                continue
            output += '<tr class="form-display"><td class="text">%s</td><td class="value">%s</td></tr>' % (
                field.verbose_name, 
                getattr(self, field.name))
        output += "</table>"
        return output

    class Meta:
        abstract = True


class NameOnlyModelBase(ModelBase):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=64, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']

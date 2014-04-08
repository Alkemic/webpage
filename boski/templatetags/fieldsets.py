# -*- coding:utf-8 -*-
#
# Use the tag like this:
#
# {% draw_form form fieldsets %}
#
# Where 'form' is the form to be draw and 'fieldsets' is a tuple containing the
# fieldsets and the contained fields.
#
# Example on how to build the fieldsets parameter
#
# fiedsets = (
#     ('Personal Data', {'fields':('name','gender'), 'id':'personal_data'}),
#     ('Address', {'fields':('street','number','city','zip_code'), 'id':'address'}),
# )
#

from django.template import Library

register = Library()

@register.simple_tag
def draw_form(form, fieldsets=False):

    def get_fields_html(fields, f):
        fields_html = []
        append = fields_html.append
        for field_name in fields:
            field = f[field_name]
            cls = []
            help_text = ''
            errors = ''
            if f.fields[field_name].required:
                cls.append('required')
            if field.help_text:
                help_text = '<span>%s</span>' % field.help_text
            if f[field_name].errors:
                errors = str(f[field_name].errors)
                cls.append('error')
            cls = ' class="%s"' % " ".join(cls)
            #append('<li%s>%s<label for="%s">%s:</label> %s %s</li>' % (cls, errors, field_name, field.label, str(field), help_text))
            append('<li%s>%s<label for="%s">%s:</label> %s %s</li>' % (cls, errors, field_name, unicode(field.label), unicode(field), help_text))
        return "".join(fields_html)

    form_html = []
    append_to_form = form_html.append
    form.auto_id = True

    fieldset_template = '<fieldset%(id)s><legend>%(legend)s</legend><ul>%(fields)s</ul></fieldset>'

    if fieldsets:
        for fieldset in fieldsets:
            context = {}
            id = fieldset[1].get('id')
            if id:
                context['id'] = ' id="%s"' % id
            else:
                context['id'] = ''
            context['legend'] = fieldset[0]
            fields = fieldset[1]['fields']
            context['fields'] = get_fields_html(fields, form)
            append_to_form(fieldset_template % context)
        return "".join(form_html)
    else:
        fields = form.fields.keys()
        return get_fields_html(fields, form)

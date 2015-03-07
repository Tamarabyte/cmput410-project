from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils import six

class TemplateMixin(object):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    def as_bootstrap_form(self):
        "Returns this form rendered as HTML <p>s."
        return self._div_output(
            normal_row='''<div class="form-group">
                <div class="input-container">
                    %(label)s
                    <div class="col-lg-12">
                        %(field)s
                    </div>
                    %(help_text)s
                </div>
                <div class="error-container error">
                    %(errors)s
                    %(top_errors)s
                </div>
            </div>''',
            error_row='%s',
            row_ender='</div>',
            help_text_html='%s',
            top_errors_with_first = True,
            empty_errors = '&nbsp;'
            )
        
    def _div_output(self, normal_row, error_row, row_ender, help_text_html, top_errors_with_first = False,
                    limit_errors=1, empty_errors=''):
        "Helper function for outputting HTML."
        
        top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        count = 0
        for name, field in self.fields.items():
            
            count += 1
            
            bf = self[name]
            # Escape and cache in local variable.
            
            if limit_errors is not None:
                bf_errors = self.error_class([conditional_escape(error) for error in bf.errors][:limit_errors])
            else:
                bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
            
            top_errors_text = ''
            if count == 1 and top_errors_with_first:
                if len(bf_errors) < limit_errors:
                    top_errors_text = ', '.join([force_text(e) for e in top_errors][:limit_errors - len(bf_errors)])
            
            html_class_attr = ''
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        ['(Hidden field %(name)s) %(error)s' % {'name': name, 'error': force_text(e)}
                         for e in bf_errors])
                hidden_fields.append(six.text_type(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if bf.label:
                    label = conditional_escape(force_text(bf.label))
                    label = '<label for="%s" class="col-lg-12 control-label" >%s</label>'% (bf.html_name, label)
                else:
                    label = ''

                if field.help_text:
                    help_text = '<div class="help-text">%s</div>' % (help_text_html % force_text(field.help_text))
                else:
                    help_text = ''

                output.append(normal_row % {
                    'errors': ', '.join([force_text(e) for e in bf_errors]) or empty_errors,
                    'label': force_text(label),
                    'field': six.text_type(bf.as_widget(attrs={"class":"form-control"})),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'field_name': bf.html_name,
                    'top_errors' : top_errors_text,
                })

        if top_errors and not top_errors_with_first:
            output.insert(0, error_row % force_text(top_errors))

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {'errors': '', 'label': '',
                                              'field': '', 'help_text': '',
                                              'html_class_attr': html_class_attr})
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe('\n'.join(output))
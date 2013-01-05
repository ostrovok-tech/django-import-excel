# coding:utf-8
from django import forms
from django.contrib import messages
from django.forms.util import ErrorList
from django.shortcuts import redirect
from django.utils import simplejson
from django.utils.datastructures import MergeDict
from django.views.generic.simple import direct_to_template
from forms import ImportExcelForm
import datetime


def import_excel(request, FormClass=ImportExcelForm, template_name='import_excel/import_excel.html', with_good=True, next_url='.'):
    comment_initial = {'comment': 'Imported %s' % datetime.datetime.now()}
    form = FormClass(data=request.POST or None, files=request.FILES or None, initial=comment_initial)
    form_class_name = FormClass.__name__
    extra_context = {}
    if form.is_valid():
        cleaned_data = form.cleaned_data
        try:
            converted_items = form.get_converted_items(cleaned_data)
        except Exception, e:
            error_message = u'Error with excel file: %s' % str(e)
            form.errors['excel_file'] = ErrorList([error_message])
        else:
            if not with_good or form.cleaned_data['is_good']:
                form.update_callback(request, converted_items)
                messages.success(request, 'Excel Data is succefully imported')
                next_url = request.GET.get('next', next_url) or '.'
                return redirect(next_url)
            initial = MergeDict(comment_initial, {
                'converted_items': simplejson.dumps(converted_items),
            }, cleaned_data)
            form = FormClass(initial=initial)
            form.fields['is_good'].widget = forms.CheckboxInput()
            form.fields['excel_file'].widget = forms.HiddenInput()
            extra_context['converted_items'] = converted_items
    extra_context.update({
        'form': form, 'form_class_name': form_class_name, 'with_good': with_good,
    })
    return direct_to_template(request, template_name, extra_context)

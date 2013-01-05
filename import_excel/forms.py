# coding:utf-8
from django import forms
from django.forms.util import ErrorList
from django.utils import simplejson
import xlrd


class ImportExcelForm(forms.Form):

    excel_file = forms.FileField(required=False)
    converted_items = forms.CharField(widget=forms.HiddenInput, required=False)
    comment = forms.CharField(required=False)
    is_good = forms.BooleanField(widget=forms.HiddenInput, required=False)

    def clean_converted_items(self):
        converted_items = self.cleaned_data['converted_items']
        if not converted_items:
            return None
        try:
            converted_items = simplejson.loads(converted_items)
        except ValueError:
            raise forms.ValidationError(u'Bad converted data')
        return converted_items

    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get('excel_file') and not cleaned_data.get('converted_items'):
            self.errors['excel_file'] = ErrorList([u'Required Field'])
        return cleaned_data

    def get_converted_items(self, data):
        if data['converted_items']:
            return data['converted_items']
        excel_file = data['excel_file']
        book = xlrd.open_workbook(
            file_contents=excel_file.read(), encoding_override='utf-8'
        )
        sheet = book.sheet_by_index(0)
        converted_items = []
        for rx in range(sheet.nrows):
            row = sheet.row(rx)
            if not row:
                continue
            values = map(lambda cell: cell.value, row)
            converted_items.append(values)
        return converted_items

    def update_callback(self, request, converted_items):
        raise NotImplementedError

from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='如果你想要使用你自己 YAKIN, 你先選擇你的 YAKIN.tar.gz, 然後點選上傳檔案, 檔案會在已上傳的 YAKIN 中',
        help_text = '(e.q., xxxxx.tar.gz)'
    )

    def clean(self):
        docfile = self.cleaned_data.get('docfile')
        if not docfile:
            raise forms.ValidationError('File is required.')  
        # if not docfile.name.startswith('filename'):
        #     raise forms.ValidationError('Incorrect file name.')
        if not docfile.name.endswith('gz'):
            raise forms.ValidationError('Incorrect file format.')
        
        return super(DocumentForm, self).clean()
from django import forms
class NewRepoForm(forms.Form):
    repo_name = forms.CharField(
                                widget=forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'placeholder' : 'مثلا MyFirstRepo'
                                    }
                                ),
                                label='نام مخزن',
                                max_length=50
    )

    desc = forms.CharField(
                            widget=forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'rows' : '4',
                                    'placeholder' : 'توضیحی در مورد مخزن خود بنویسید'
                                }
                            ),
                            label='توضیحات مخزن',
                            max_length=500
    )

class FileUploadForm(forms.Form):
    commit = forms.CharField(
                                widget=forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'placeholder' : 'عنوان کامیت خود را وارد کنید'
                                    }
                                ),
                                label='عنوان کامیت',
                                max_length=100
    )

    files = forms.FileField(
                                    widget=forms.ClearableFileInput(
                                        attrs={
                                            'class' : 'form-control-file',
                                            'multiple': True,
                                        }
                                    )
    )
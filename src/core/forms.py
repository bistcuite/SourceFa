from django import forms

# form for create new repository
class NewRepoForm(forms.Form):
    # repository's name
    repo_name = forms.CharField(
                                widget=forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'placeholder' : 'مثلا MyFirstRepo'
                                    }
                                ),
                                label='نام مخزن',
                                max_length=50
    )
    
    # repository's description
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

# form for upload file to repository
class FileUploadForm(forms.Form):
    # files to upload
    files = forms.FileField(
                                widget=forms.ClearableFileInput(
                                    attrs={
                                        'class' : 'form-control-file',
                                        'multiple': True,
                                    }    
                                ),
                                label='فایل ها را انتخاب کنید'
    )
    
    # commit title
    commit = forms.CharField(
                                widget=forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'placeholder' : 'عنوان کامیت خود را وارد کنید'
                                    }
                                ),
                                label='عنوان کامیت',
                                max_length=100
    )
    
    # commit description
    # ...
    
    # uploads to which dir
    # ...
    
# form for create new repository
class EditFileRepoForm(forms.Form):
    # file name to edit
    filename = forms.CharField(widget=forms.TextInput)
    
    # content to replace with current file contetn
    content = forms.CharField(widget=forms.Textarea)

    # commit title
    commit = forms.CharField(widget=forms.TextInput)
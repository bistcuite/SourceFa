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
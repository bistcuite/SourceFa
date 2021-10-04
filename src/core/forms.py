from django import forms

class NewRepoForm(forms.Form):
    user_id = forms.CharField(
                                widget=forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'readonly' : 'readonly',
                                        'placeholder' : '{{ user.username}}'
                                    }
                                ),
                                max_length=100
    )
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
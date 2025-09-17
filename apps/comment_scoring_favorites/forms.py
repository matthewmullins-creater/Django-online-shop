from django import forms

# parent_id : or we say on which product
# comment_id : or we say on which comment
# widget=forms.HiddenInput() : this field is hidden

class CommentForm(forms.Form):
    
    product_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    comment_text = forms.CharField(label="", error_messages={'required':'This field cannot be empty'} ,widget=forms.Textarea(attrs={'class': 'form-control' , 'placeholder': 'Comment text' , 'rows': '4'}))
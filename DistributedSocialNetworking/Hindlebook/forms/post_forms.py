from django import forms

class PostForm(forms.Form):
		post_text = forms.CharField(label="",widget=forms.Textarea)
		post_privacy = forms.ChoiceField(label = "Privacy", widget=forms.Select(),
										choices = ([(0,"Self Only"),
													(1,"Selected author"),
													(2,"Friends"),
													(3,"Friends of Friends"),
													(4,"Friends on host"),
													(5,"Public")]),required=True)

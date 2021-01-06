# from django import forms
# from .models import ProjectPhase


# class ProjectForm(forms.Form):
#     name = forms.CharField()
#     start_date = forms.CharField()
#     end_date = forms.CharField()
#     phase = forms.ChoiceField(choices=[
#         (item.pk, item.phase) for item in ProjectPhase.objects.all()
#     ])
#     labels = ['チェック','複数チェック','ラジオボタン','動的選択肢１','動的選択肢２']
#     CHOICE = [
#         ('1','選択肢＜１＞'),
#         ('2','選択肢＜２＞'),
#         ('3','選択肢＜３＞')]
#     two = forms.MultipleChoiceField(
#         label=labels[1],
#         required=False,
#         disabled=False,
#         initial=[],
#         choices=CHOICE,
#         widget=forms.CheckboxSelectMultiple(attrs={
#             'id': 'two','class': 'form-check-input'}))

from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class NotesForm(forms.ModelForm):
    class  Meta:
       model = Notes
       fields = ['title', 'description']


class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':DateInput()}
        fields=['subject','title','description','due','is_finished']

class DashboardForm(forms.Form):    
    text=forms.CharField(max_length=100, label='Enter your search')


class TodoForm(forms.ModelForm):
    class  Meta:
        model = Todo
        fields=['title','is_finished']

# 


class ConversionForm(forms.Form):
    CHOICES = [
        ('length', 'Length'),
        ('mass', 'Mass'),
        ('temperature', 'Temperature'),
        ('volume', 'Volume'),
        ('speed', 'Speed')
    ]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [
        ('yard', 'Yard'),
        ('foot', 'Foot'),
        ('meter', 'Meter'),
        ('inch', 'Inch')
    ]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter value'}
    ))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))

class ConversionMassForm(forms.Form):
    CHOICES = [
        ('pound', 'Pound'),
        ('kilogram', 'Kilogram'),
        ('gram', 'Gram'),
        ('ounce', 'Ounce')
    ]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter value'}
    ))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))

class ConversionTemperatureForm(forms.Form):
    CHOICES = [
        ('celsius', 'Celsius'),
        ('fahrenheit', 'Fahrenheit'),
        ('kelvin', 'Kelvin')
    ]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter value'}
    ))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))

class ConversionVolumeForm(forms.Form):
    CHOICES = [
        ('liter', 'Liter'),
        ('milliliter', 'Milliliter'),
        ('gallon', 'Gallon'),
        ('cup', 'Cup')
    ]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter value'}
    ))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))

class ConversionSpeedForm(forms.Form):
    CHOICES = [
        ('kmph', 'Kilometers per Hour'),
        ('mph', 'Miles per Hour'),
        ('mps', 'Meters per Second'),
        ('fps', 'Feet per Second')
    ]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter value'}
    ))
class ConversionTimeForm(forms.Form):
    CHOICES = [
        ('second', 'Second'),
        ('minute', 'Minute'),
        ('hour', 'Hour'),
        ('day', 'Day')
    ]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type': 'number', 'placeholder': 'Enter value'}
    ))
class UserRegistrationForm(UserCreationForm):
     class Meta:
        model=User
        fields=['username','password1','password2']
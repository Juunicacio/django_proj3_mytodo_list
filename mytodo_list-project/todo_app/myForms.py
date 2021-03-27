# Create a form to the user create a Todo
# we need to pass all values that will be insert to the db
from django.forms import ModelForm
# import your model
from .models import Todo

# this needs to be inherit from a specific file (ModelForm)
class TodoForm(ModelForm):      
    # specify what class are we working with, and which fields do we want
    class Meta:
        # say which model you want this form to be insert
        model = Todo
        # specify the fields that we want as a list
        fields = ['title', 'note', 'importantCheck']
        # changing the field key name
        labels = {
            'importantCheck': ('Important')
        }
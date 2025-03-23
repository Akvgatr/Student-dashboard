from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User  # Import User model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .forms import *

from .models import Notes
from django.views import generic
from django.views.generic import DetailView


from youtubesearchpython import VideosSearch

import requests

import wikipedia

def home(request):
    return render(request, 'dashboard/home.html')


def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
            messages.success(request, f"Notes added by {request.user.username} successfully!")
            return redirect('notes')  # Redirect to avoid form resubmission
    else:
        form = NotesForm()
    
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, "form": form}
    return render(request, 'dashboard/notes.html', context)

def delete_note(request , pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')



class NotesDetailView(DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'  # specify the template to render
    context_object_name = 'note'  # optional, but useful to customize the context name





def homework(request):
    if request.method=="POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finsihed=request.POST['is_finished']
                if finsihed=='on':
                    finished= True
                else:
                    finished=False
            except:
                finished=False
            homeworks=Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(request, f"homework added by {request.user.username} successfully!")
    else:
            form=HomeworkForm()    
    form=HomeworkForm()
    homework=Homework.objects.filter(user=request.user)
    if len(homework)==0:
        homework_done=True
    else:
        homework_done=False
    context={'homeworks':homework,'homeworks_done':homework_done,'form':form}
    return render(request, 'dashboard/homework.html',context)

def update_homework(request , pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished==True:
        homework.is_finished=False
    else:
        homework.is_finished=True
    homework.save()
    return redirect('homework')
    
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")


def youtube(request):
    form = DashboardForm()  # Define the form initially
    result_list = []  # Store results here

    if request.method == "POST":
        form = DashboardForm(request.POST)  # Bind form data
        text = request.POST.get('text', '').strip()  # Get text safely

        if text:  # Ensure text is not empty
            try:
                video = VideosSearch(text, limit=30)
                video_results = video.result()

                if video_results and 'result' in video_results:  # Ensure results exist
                    for i in video_results['result']:
                        result_dict = {
                            'input': text,
                            'title': i['title'],
                            'duration': i['duration'],
                            'thumbnail': i['thumbnails'][0]['url'],
                            'channel': i['channel']['name'],
                            'link': i['link'],
                            'views': i['viewCount']['short'],
                            'published': i.get('publishedTime', 'N/A'),  # Handle missing data
                        }

                        # Extract description snippet
                        desc = ''
                        if i.get('descriptionSnippet'):  # Use `.get()` to avoid KeyError
                            for j in i['descriptionSnippet']:
                                desc += j['text'] + " "
                        result_dict['description'] = desc.strip()

                        result_list.append(result_dict)

            except Exception as e:
                return render(request, 'dashboard/youtube.html', {'form': form, 'error': f'Error: {e}'})

    # Pass results to template
    context = {'result_list': result_list, 'form': form}
    return render(request, "dashboard/youtube.html", context)

def todo(request):
    if request.method=='POST':
        form =TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST["is_finished"]
                if finished =='on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            todos=Todo(
                user=request.user,
                title=request.POST["title"],
                is_finished=finished
            )
            todos.save()
            messages.success(request, f"Todo added from {request.user.username}!!")
    form=TodoForm()
    todo=Todo.objects.filter(user=request.user)
    if len(todo)==0:
        todos_done=True
    else:
        todos_done=False
    context={
        'form':form,
        'todos':todo,
        'todos_done':todos_done
    }
    return render(request,"dashboard/todo.html",context)


def update_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished==True:
        todo.is_finished=False
    else:
        todo.is_finished=True
    todo.save()
    return redirect('todo')

def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')





def books(request):
    if request.method == "POST":  
        form = DashboardForm(request.POST)
        text = request.POST.get('text', '')  # Use .get() to avoid KeyError
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()

        result_list = []
        for i in range(min(10, len(answer.get('items', [])))):  # Avoid IndexError
            volume_info = answer['items'][i]['volumeInfo']
            
            # Get the rating and convert to integer if possible
            rating = volume_info.get('averageRating', 'N/A')
            rating_value = 0
            try:
                if rating != 'N/A':
                    rating_value = int(float(rating))
            except (ValueError, TypeError):
                rating_value = 0
                
            result_dic = {
                'title': volume_info.get('title', 'N/A'),
                'subtitle': volume_info.get('subtitle', 'N/A'),
                'description': volume_info.get('description', 'N/A'),
                'count': volume_info.get('pageCount', 'N/A'),
                'categories': volume_info.get('categories', 'N/A'),
                'rating': rating,
                'rating_value': rating_value,  # Add integer rating for template use
                'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                'preview': volume_info.get('previewLink', ''),
            }
            result_list.append(result_dic)

        context = {
            'form': form,
            'results': result_list
        }
        return render(request, "dashboard/books.html", context)

    else:
        form = DashboardForm()
    
    context = {'form': form}  
    return render(request, "dashboard/books.html", context)



def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get('text', '')

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()

        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']

            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        except (KeyError, IndexError):
            context = {'form': form, 'input': '', 'error': 'Invalid word or API issue.'}

        return render(request, "dashboard/dictionary.html", context)

    else:
        form = DashboardForm()
        return render(request, "dashboard/dictionary.html", {'form': form})


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        
        try:
            search = wikipedia.page(text)
            context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'details': search.summary
            }
        except wikipedia.DisambiguationError as e:
            context = {
                'form': form,
                'error': "Your search term is ambiguous. Please refine your query.",
                'options': e.options  # Display possible options for the user
            }
        except wikipedia.PageError:
            context = {
                'form': form,
                'error': "No matching page found. Please try another term."
            }
        except Exception as e:
            context = {
                'form': form,
                'error': f"An unexpected error occurred: {str(e)}"
            }

        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        return render(request, 'dashboard/wiki.html', {'form': form})

def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        measurement_type = request.POST.get('measurement')

        answer = ''
        if measurement_type == 'length':
            measurement_form = ConversionLengthForm()
            if 'input' in request.POST:
                first = request.POST.get('measure1')
                second = request.POST.get('measure2')
                input_value = request.POST.get('input')

                # Safe float conversion
                try:
                    input_value = float(input_value) if input_value.strip() else 0
                    
                    conversions = {
                        'yard': {'foot': 3, 'meter': 0.9144, 'inch': 36},
                        'foot': {'yard': 1/3, 'meter': 0.3048, 'inch': 12},
                        'meter': {'yard': 1.09361, 'foot': 3.28084, 'inch': 39.3701},
                        'inch': {'foot': 1/12, 'yard': 1/36, 'meter': 0.0254},
                        'mile': {'km': 1.60934},
                        'km': {'mile': 0.621371}
                    }

                    if first in conversions and second in conversions[first]:
                        result = input_value * conversions[first][second]
                        answer = f'{input_value} {first} = {result:.4f} {second}'
                except ValueError:
                    answer = "Please enter a valid number"

        elif measurement_type == 'mass':
            measurement_form = ConversionMassForm()
            if 'input' in request.POST:
                first = request.POST.get('measure1')
                second = request.POST.get('measure2')
                input_value = request.POST.get('input')

                # Safe float conversion
                try:
                    input_value = float(input_value) if input_value.strip() else 0
                    
                    conversions = {
                        'pound': {'kilogram': 0.453592, 'gram': 453.592, 'ounce': 16},
                        'kilogram': {'pound': 2.20462, 'gram': 1000},
                        'gram': {'kilogram': 0.001, 'pound': 0.00220462},
                        'ounce': {'pound': 1/16},
                        'ton': {'kilogram': 907.184, 'pound': 2000}
                    }

                    if first in conversions and second in conversions[first]:
                        result = input_value * conversions[first][second]
                        answer = f'{input_value} {first} = {result:.4f} {second}'
                except ValueError:
                    answer = "Please enter a valid number"

        elif measurement_type == 'temperature':
            measurement_form = ConversionTemperatureForm()
            if 'input' in request.POST:
                first = request.POST.get('measure1')
                second = request.POST.get('measure2')
                input_value = request.POST.get('input')

                # Safe float conversion
                try:
                    input_value = float(input_value) if input_value.strip() else 0
                    
                    if first == 'Celsius' and second == 'Fahrenheit':
                        result = (input_value * 9/5) + 32
                    elif first == 'Fahrenheit' and second == 'Celsius':
                        result = (input_value - 32) * 5/9
                    elif first == 'Celsius' and second == 'Kelvin':
                        result = input_value + 273.15
                    elif first == 'Kelvin' and second == 'Celsius':
                        result = input_value - 273.15
                    elif first == 'Fahrenheit' and second == 'Kelvin':
                        result = (input_value - 32) * 5/9 + 273.15
                    elif first == 'Kelvin' and second == 'Fahrenheit':
                        result = (input_value - 273.15) * 9/5 + 32
                    else:
                        result = input_value  # If same units

                    answer = f'{input_value} {first} = {result:.2f} {second}'
                except ValueError:
                    answer = "Please enter a valid number"

        elif measurement_type == 'time':
            measurement_form = ConversionTimeForm()
            if 'input' in request.POST:
                first = request.POST.get('measure1')
                second = request.POST.get('measure2')
                input_value = request.POST.get('input')

                # Safe float conversion
                try:
                    input_value = float(input_value) if input_value.strip() else 0
                    
                    conversions = {
                        'second': {'minute': 1/60, 'hour': 1/3600, 'day': 1/86400},
                        'minute': {'second': 60, 'hour': 1/60, 'day': 1/1440},
                        'hour': {'second': 3600, 'minute': 60, 'day': 1/24},
                        'day': {'second': 86400, 'minute': 1440, 'hour': 24, 'week': 1/7, 'month': 1/30, 'year': 1/365},
                        'week': {'day': 7, 'month': 1/4.345, 'year': 1/52},
                        'month': {'day': 30, 'year': 1/12},
                        'year': {'day': 365, 'month': 12}
                    }

                    if first in conversions and second in conversions[first]:
                        result = input_value * conversions[first][second]
                        answer = f'{input_value} {first} = {result:.2f} {second}'
                except ValueError:
                    answer = "Please enter a valid number"

        elif measurement_type == 'volume':
            measurement_form = ConversionVolumeForm()
            if 'input' in request.POST:
                first = request.POST.get('measure1')
                second = request.POST.get('measure2')
                input_value = request.POST.get('input')

                # Safe float conversion
                try:
                    input_value = float(input_value) if input_value.strip() else 0
                    
                    conversions = {
                        'liter': {'milliliter': 1000, 'cubic meter': 0.001, 'gallon': 0.264172},
                        'milliliter': {'liter': 0.001},
                        'cubic meter': {'liter': 1000},
                        'gallon': {'liter': 3.78541, 'quart': 4},
                        'quart': {'gallon': 1/4, 'pint': 2},
                        'pint': {'quart': 1/2}
                    }

                    if first in conversions and second in conversions[first]:
                        result = input_value * conversions[first][second]
                        answer = f'{input_value} {first} = {result:.2f} {second}'
                except ValueError:
                    answer = "Please enter a valid number"
        elif measurement_type == 'speed':
            measurement_form = ConversionSpeedForm()  # You'll need to create this form class
            if 'input' in request.POST:
                first = request.POST.get('measure1')
                second = request.POST.get('measure2')
                input_value = request.POST.get('input')

                # Safe float conversion
                try:
                    input_value = float(input_value) if input_value.strip() else 0
                    
                    conversions = {
                        'mph': {'kph': 1.60934, 'm/s': 0.44704, 'knot': 0.868976},
                        'kph': {'mph': 0.621371, 'm/s': 0.277778, 'knot': 0.539957},
                        'm/s': {'mph': 2.23694, 'kph': 3.6, 'knot': 1.94384},
                        'knot': {'mph': 1.15078, 'kph': 1.852, 'm/s': 0.514444}
                    }

                    if first in conversions and second in conversions[first]:
                        result = input_value * conversions[first][second]
                        answer = f'{input_value} {first} = {result:.2f} {second}'
                    else:
                        answer = "Conversion not available"
                except ValueError:
                    answer = "Please enter a valid number"

        else:
            measurement_form = None

        context = {
            'form': form,
            'm_form': measurement_form,
            'input': True,
            'answer': answer
        }
    
    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }

    return render(request, "dashboard/conversion.html", context)




def register(request):
    if request.method=="POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"Account created for {username}!!")
            return redirect("login")
    else:
        form=UserRegistrationForm()
    context={'form':form}
    return render(request, "dashboard/register.html",context)


def profile(request):
    homeworks=Homework.objects.filter(is_finished=False, user=request.user)
    todos=Todo.objects.filter(is_finished=False, user=request.user)
    if len(homeworks)==0:
        homework_done=True
    else:
        homework_done=False

    if len(todos)==0:
        todos_done=True
    else:
        todos_done=False
    context={
        'homeworks': homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done

    }
    return render(request,"dashboard/profile.html",context)



def custom_logout(request):
    logout(request)  # Log out the user
    return render(request,"dashboard/logout.html")
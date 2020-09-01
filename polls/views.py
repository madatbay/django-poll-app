from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from .forms import QuestionForm, ChoiceForm

from .models import Question

# Create your views here.

def index(request):
    all_votes = []
    def get_total():
        total_votes = 0
        all_questions = Question.objects.all()
        for q in all_questions:
            for c in q.choice_set.all():
                total_votes += c.votes
            all_votes.append(total_votes)
            total_votes = 0
        return all_votes
        
    get_total()
    all_polls = Question.objects.order_by('-pub_date')
    context = {'all_polls': all_polls,'all_votes': all_votes}
    return render(request, 'polls/index.html', context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404( Question, pk = question_id)
    try:
        selected = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected.votes += 1
        selected.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('polls:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('polls:index')
            else:
                messages.error(request, 'Username or Password is incorrect')

        return render(request, 'polls/login.html')



def register(request):
    if request.user.is_authenticated:
        return redirect('polls:index')
    else:
        form = UserCreationForm()

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account was successefully created')
                return redirect('polls:login')

        context = {'form': form}
        return render(request, 'polls/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('polls:login')

@login_required(login_url='polls:login')
def createPoll(request):
    form = QuestionForm
    form2 = ChoiceForm

    if request.method == 'POST':
        form2 = ChoiceForm(request.POST)
        form = QuestionForm(request.POST)
        if form.is_valid() and form2.is_valid():
            form2.question = form.question
            form2.save()
            form.save()
            return redirect('polls:index')

    context = {'form': form,'form2': form2}
    return render(request, 'polls/createPoll.html', context)
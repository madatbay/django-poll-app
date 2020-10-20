from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from .forms import AddPoll
from .models import Question, Choice, Voter

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

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    labels = []
    data = []
    queryset = Question.objects.filter(pk = question_id)
    for question in queryset:
        for choice in question.choice_set.all():
            labels.append(choice.choice_text)
            data.append(choice.votes)


    return render(request, 'polls/results.html', {
        'question': question,
        'labels': labels,
        'data': data
        })

def vote(request, question_id):
    question = get_object_or_404( Question, pk = question_id)
    if Voter.objects.filter(poll_id = question_id, user_id = request.user.id).exists():
        return render(request, 'polls/detail.html', {
        'question': question,
        'error_message': "Sorry, but you have already voted."
        })
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
        Voter.objects.create(poll_id = question_id, user_id = request.user.id)
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
    form = AddPoll(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        choices = request.POST.getlist('morechoices', None)
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()
        choice = {}
        for i in range(1,3):
            choice['choice{0}'.format(i)] = Choice(question = new_form, choice_text = form.cleaned_data['choice{0}'.format(i)]).save()
        for c in choices:
            if c != "":
                counter = 3
                choice['choice{0}'.format(counter)] = Choice(question = new_form, choice_text = c.encode('utf8')).save()
                counter += 1
        return redirect('polls:index')
    else:
        form = AddPoll()

    context = {'form': form}
    return render(request, 'polls/createPoll.html', context)
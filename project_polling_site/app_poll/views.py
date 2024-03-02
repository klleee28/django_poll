from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from . models import Question, Choice
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'app_poll/index.html'
    context_object_name = 'latest_question'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'app_poll/detail.html'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'app_poll/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {'question':question, 'error_message':'You did not select a choice'}

        return render(request,'app_poll/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:url_results', args=(question.id,)))

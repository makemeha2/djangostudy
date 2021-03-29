from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from polls.models import Question, Choice
import logging
logger = logging.getLogger(__name__)

class IndexView(generic.ListView) :
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self) :
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView) :
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView) :
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id) :
    logger.debug("vote().question_id : %s" % question_id)

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message' : "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))
        #return render(request, 'polls/result.html', {'question' : question})


'''
def index(request) :
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list' : latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question' : question})

def vote(request, question_id) :
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message' : "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        #return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))
        return render(request, 'polls/result.html', {'question' : question})

def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question' : question})
'''
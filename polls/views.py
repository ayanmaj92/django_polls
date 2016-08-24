from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.utils import timezone
#from django.template import loader
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.db.models import F
from django.views import generic
'''
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#template = loader.get_template('polls/index.html')
	context = {'latest_question_list':latest_question_list,}
	#return HttpResponse(template.render(context,request))
	#render() is a shortcut, it takes the request, renders the template html and passes the context to it
	return render(request, 'polls/index.html', context)

def detail(request, question_id):
	#try:
	#	question = Question.objects.get(pk=question_id)
	#except:
	#	raise Http404("Question does not exist")
	#Now we do all of that with a simple function get_object_or_404
	question = get_object_or_404(Question, pk=question_id)
	#return HttpResponse("You're looking at question %s." %question_id)
	return render(request, "polls/detail.html", {'question': question})

def results(request, question_id):
	#response = "You're looking at the results of question %s."
	#return HttpResponse(response % question_id)
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question':question})
'''
# NOW we are gonna use Django Generic Views

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		'''return last five published questions not including those set to be published in future'''
		#return Question.objects.order_by('-pub_date')[:5]
		#__lte means less than or equal to
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def vote(request, question_id):
	#return HttpResponse("You're voting on question %s." %question_id)
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay question voting form
		return render(request, 'polls/detail.html', {'question': question,
		'error_message':"You didn't select a choice.",
		})
	else:
		#selected_choice.votes += 1
		selected_choice.votes = F('votes') + 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
		

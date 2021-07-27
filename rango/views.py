import rango
from django.shortcuts import render
from django.http import HttpResponse

#what users see on Index page
def index(request):
    #constrcut a dictionary to pass to the template engine as its context
    #note the key boldmessage matches to {{boldmessage}} in the template!
    context_dic = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    #return a rendered response to sent to the client.
    #we make use of teh short cut funcation to make our lives easier.
    #notes that the first parameter is the template we wish to use.
    return render(request,'rango/index.html', context=context_dic)

#ch3 Exercises 
#what users see on About page
def about(request):
    return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>") #ch3 ex. added a hyperlink to the index page
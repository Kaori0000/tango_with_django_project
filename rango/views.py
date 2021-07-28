import rango
from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category #importing required models


#what users see on Index page
def index(request):
    #Query the database for a list of All categories currently stored. 
    #order the categories by the number of likes in descending order.
    #Retrieve the top 5 only -- or all if less than 5
    #Place teh list in our context_dic dictionary (with our boldmessage)
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]


    #constrcut a dictionary to pass to the template engine as its context
    #note the key boldmessage matches to {{boldmessage}} in the template!
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    # Render the response and send it back!
    #return a rendered response to sent to the client.
    #we make use of the short cut funcation to make our lives easier.
    #notes that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)



    
    
   

#ch4 Exercises 
#what users see on About page
def about(request):
    return render(request, 'rango/about.html')
   # return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>") #ch3 ex. added a hyperlink to the index page
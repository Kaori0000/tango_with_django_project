import rango
from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category #importing required models
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect


#what users see on Index page
def index(request):
    #Query the database for a list of All categories currently stored. 
    #order the categories by the number of likes in descending order.
    #Retrieve the top 5 only -- or all if less than 5
    #Place teh list in our context_dic dictionary (with our boldmessage)
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]

    page_list = Page.objects.order_by('-views')[:5] 


    #constrcut a dictionary to pass to the template engine as its context
    #note the key boldmessage matches to {{boldmessage}} in the template!
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    
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


#new view
def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    
    try:
        #Check if we can find a category name slug with the given name.
        #If can't, the .get() method raises a DoesNotExist exception 
        #The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
 
    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()#create a CategoryForm

    # check if the HTTP request was a a HTTP POST (did the user submit data via the form)?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
        # Save the new category to the database.
           form.save(commit=True)
        # Now that the category is saved, we could confirm this.
        # For now, just redirect the user back to the index view.
           return redirect('/rango/')
        else:
        # The supplied form contained errors -
        # just print them to the terminal.
            print(form.errors)

   # Will handle the bad form, new form, or no form supplied cases.
   # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})



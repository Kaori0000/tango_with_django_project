import rango
from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category #importing required models
from rango.models import Page
from rango.forms import CategoryForm, PageForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm


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
    return render(request, 'rango/about.html',{})
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

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None
    
    # You cannot add a page to a Category that does not exist
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


#ch 9
def register(request):
    #A boolean value for teling the template whether the registeration was successful.
    #Set to False initially. Code changes value to True when registeration succeeds.
    registered = False

    #If it's a HTTP POST, we are interested in processing form data
    if request.method == 'POST':
        #Try to grab information from the raw form information.
        #Note that we make use of both UserForm and UserProfileForm
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        #If they two forms are valid:
        if user_form.is_valid() and profile_form.is_valid():
            #save the user's form data to the database.
            user = user_form.save()

            #Now we hash the password with set_password method.
            #Once hashed, we can update the user object. 
            user.set_password(user.password)
            user.save()

            #Now sort out the UserProfile instance.
            #Since we need to set the user attribute ourselves, we set commit = False. 
            #This delays saving the model until we are ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            #Did the user provide a profile picture?
            #If yes, we need to get it from the inpit form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            #Now we save the UserProfile model instance.
            profile.save()

            #Update our variable to indicate that the template registeration was successful.
            registered = True
        else:
            #invalid form/forms - mistake or something.
            #Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        #Not a HTTP POST, so we render out form using two ModelForm instances.
        #There forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    #render the template depending on the context.
    return render(request, 'rango/register.html', context = {'user_form': user_form,'profile_form': profile_form,'registered': registered})

                   

    







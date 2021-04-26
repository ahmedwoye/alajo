from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
# Create your views here.
from .models import*
from .forms import OrderForm,CreateUserForm, CustomerForm
from .decorators import unauthenticated_user,allowed_users, admin_only

#pdf for exporting of data using xhtml2pdf

from django.template.loader import get_template
from xhtml2pdf import pisa
#import views for customer
from django.views.generic import ListView
from .models import Customer
from .filters import OrderFilter



@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

     
    
    context = {'orders' :orders, 'customers' :customers, 'total_orders' :total_orders, 'delivered' :delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()


    #total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()



    print('ORDERS:', orders)    
    context = {'orders': orders, 'total_orders' :total_orders, 'delivered' :delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render( request, 'accounts/products.html', {'products': products})




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) 
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()


    myFilter = OrderFilter()
    context = {'customer': customer, 'orders':orders, 'order_count': order_count, 'myFilter': myFilter }
    return render(request, 'accounts/customer.html', context)


def sales(request):
    return render(request, 'accounts/sales.html')



@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR passwprd is incorrect')

    context = {}
    return render(request,'accounts/login.html',  context)


def logoutUser(request):
    logout(request)
    return redirect('login')

    


    context = {}
    return render(request, 'accounts/login.html', context )


@unauthenticated_user
def registerpage(request):
    
    form = CreateUserForm()



    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            
            user.groups.add(group)
            Customer.objects.create(

                user=user,

                )
            
            messages.success(request,'Account creation is successful for' + username )
            return redirect('login')
    context = {'form' : form}
    return render(request, 'accounts/register.html', context)

 
def status(request):
    return render(request, 'accounts/status.html')
 
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)

    form = OrderForm()
    if request.method == 'POST':
         #print('Printing POST:', request.POST)
        form = OrderForm()
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form' : form}
    return render(request, 'accounts/order_form.html', context)
 
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form =  OrderForm(instance=order)
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form' : form}
    return render(request, 'accounts/order_form.html', context)
 
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

class CustomerListView(ListView):
    model = Customer
    template_name= 'accounts/test.html'



def customer_render_pdf_view(request,args, **kwargs):
    pk = kwargs.get('pk')
    customer = get_object_or_404(Customer, pk=pk)


    template_path = 'accounts/pdf.html'
    context = {'customer': customer}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download use this
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #if view the pdf use this
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def render_pdf_view(request):
    template_path = 'accounts/pdf.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download use this
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #if view the pdf use this
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if form.is_valid():
        form.save()


    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()




    context = {'form': form}
    return render( request, 'accounts/account_settings.html', context)


def payment(request):

    context = { }
    return render(request, 'accounts/payment.html', context)


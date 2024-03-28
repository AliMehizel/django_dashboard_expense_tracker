from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse,HttpResponse
import csv
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from .utils import *
from reportlab.lib.pagesizes import letter
from io import BytesIO 
from reportlab.platypus import Image
from django.contrib.auth.hashers import check_password


# Create your views here.


def index(request):
    """ 
    - base page with user authentication view
    """
    signin_form = SigninForm()
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        if request.method == 'POST':
            form = SigninForm(request.POST)
            if form.is_valid():
                user = authenticate(username = form.cleaned_data['username'], password= form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('/home/') 
                else:
                    messages.error(request, 'Ooops ! Invalid input, try again.')
                    return redirect('/')
    return render(request, 'index.html', {'signin_form': signin_form})



def signup_view(request):
    """ 
    - register new user based on username,email and password
    """
    register_form = SignupForm()
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                check_user = User.objects.filter(email=form.cleaned_data.get('email'))
                print(check_user)
                if check_user.exists():
                    messages.error(request,'The email address exist before.')
                    return redirect('/signup/')
                else:
                    form.save()
                    messages.success(request,'Congratulations ! The account hase been created.')
                    return redirect('/') 
    return render(request, 'signup.html', {'register_form':register_form})

@login_required(login_url='/')
def custom_password_change(request):
    """ 
    - this logic is for setting new password.
    - the logic check current password with hashed password on userDB.
    """
    password_form = CustomPasswordChangeForm()
    user = User.objects.filter(username=request.user).first()
    if request.method == 'POST':
        
        form_pass = CustomPasswordChangeForm(request.POST)
        
        if form_pass.is_valid():
            
            password_test = check_password(form_pass.cleaned_data['current_password'], user.password)
            new_pass = form_pass.cleaned_data['new_password']
            new_pass_conf = form_pass.cleaned_data['new_password_confirm']
            
            if password_test and new_pass == new_pass_conf:
                user.set_password(new_pass)
                user.save()
                messages.success(request,'Your password have been changed succefuly.')
                return redirect('/home/')
            else: 
                messages.error(request,'Something is wrong ! try again.')
                return redirect('/change_password/')
        else: 
            messages.error(request,'Form is invalid, try again.')
    return render(request, 'custom_password_change_form.html', {'password_form':password_form})


def reset_password(request):
    """ 
    - this logic for reset password with email address
    """
    return render(request, 'rest_password.html')   
    
def logout_view(request):
    """ 
    - end user session 
    [logout view]
    """
    logout(request)
    return redirect('/')


@login_required(login_url='/')
def home(request):
    """ 
    - filter all transactions list by user
    """
    tran_list = Transaction.objects.filter(user=request.user).all()
    query = request.GET.get('query')
    
    
    message = ''
    if query:
        """ check if the query made by user exists """
        tran_list = Transaction.objects.filter(user=request.user,desc__contains=query).all()
        
    if tran_list.exists():
        
        total_inc = 0
        total_exp = 0        
        for tran in tran_list:
            if tran.transac_type == 'INCOME':
                total_inc += tran.amount
            else: 
                total_exp += tran.amount
                
        data = {
        'query_form': PostSearchForm(),
        'transactions': tran_list,
        'total_inc': total_inc,
        'total_exp': total_exp,
        }
        return render(request, 'home.html', data)
    else: 
        message = 'you have not any transactions yet !'
        return render(request, 'home.html', {'message':message,'query_form': PostSearchForm()})

    
  
def get_transaction_amount(request):
    """
    - api view to get the expense & income amout list for chart.js
    """
    
    if request.user.is_authenticated:
        tran_list = Transaction.objects.filter(user=request.user).all()
        exp_list = []
        inc_list = [] 
        desc_inc = []
        desc_exp = []
        if tran_list.exists():
            for tran in tran_list:
                
                if tran.transac_type == 'INCOME':
                    inc_list.append(tran.amount)
                    desc_inc.append(tran.desc)
                else:
                    exp_list.append(tran.amount)
                    desc_exp.append(tran.desc)
            return JsonResponse({'desc_inc': desc_inc,'desc_exp': desc_exp, 'inc_list':inc_list, 'exp_list':exp_list},safe=False)
        return JsonResponse({'message':'Ooops ! you have not transaction yet','desc_inc': desc_inc,'desc_exp': desc_exp, 'inc_list':inc_list, 'exp_list':exp_list},safe=False)
    return JsonResponse({"message":"Please, signin to you account"},safe=False)

@login_required(login_url='/') 
def add_new_transaction(request):
    """ 
    - render transationForm
    - add new transaction
    - saved by user
    """
    tran_form = TransactionForm()
    message = ''
    if request.method == 'POST':
        form_submited = TransactionForm(request.POST)
        if form_submited.is_valid():
            transaction = Transaction.objects.create(
                user = request.user,
                desc=form_submited.cleaned_data['desc'],
                amount=form_submited.cleaned_data['amount'],
                transac_type=form_submited.cleaned_data['transac_type'],
                )
            transaction.save()
            return redirect('/home/')
        else:
            message = 'Try Again please !'
            return render(request, 'new_transaction.html', {'tran_form':tran_form, 'message':message})
    return render(request, 'new_transaction.html', {'tran_form':tran_form, 'message':message})

@login_required(login_url='/') 
def edit_transaction(request,desc):
    """ 
    - get the form_transaction by description
    - edit the transaction
    """
    transaction = get_object_or_404(Transaction,desc=desc, user=request.user)
    
    if request.method == 'GET':
        form_transaction = TransactionForm(instance=transaction)
        return render(request, 'edit_transaction.html', {'form':form_transaction, 'desc':transaction.desc})
    
    elif request.method == 'POST':
        form_sub = TransactionForm(request.POST, instance=transaction)
        if form_sub.is_valid():
            form_sub.save()
            return redirect('/home/')
        else:
            messages.error(request, 'Ooops ! does not work, try again.')
            return render(request, 'edit_transaction.html', {'form':form_transaction,'desc':transaction.desc})
    
    


def delete_transaction(request,desc):
    """
    - get && delete transasction by description
    """
    transaction = get_object_or_404(Transaction, desc=desc,user=request.user)
    transaction.delete()
    return redirect('/home/')
    

def transactions_csv(request):
    """ 
    - this is basic view to generate csv file based on user data. 
    """
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="table_csv.csv"'},
    )

    writer = csv.writer(response)
    
    writer.writerow(["Description", "Amount", "Category", "Date"])
    transaction_list = Transaction.objects.filter(user=request.user).all()

    if transaction_list.count() > 0 :
        # for loops here
        for transaction in transaction_list:
            writer.writerow([transaction.desc, transaction.amount, transaction.transac_type, transaction.date_pub])
    else: 
        writer.writerow(["not yet", "not yet", "not yet", "not yet"])
    return response









def transactions_pdf(request):
    # Create a response object with the appropriate PDF headers
    buffer = BytesIO()
    
    elements = []
    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    transaction_list = Transaction.objects.filter(user=request.user).all()
    
    if transaction_list.count() > 1:
        data = [
            ['Description','Amount','Category','Date'],
        ]
        for transaction in transaction_list:
            data.append([transaction.desc,transaction.amount,transaction.transac_type,transaction.date_pub])
        table = Table(data)
    else:
        table = Table(data)
    
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), (0.7, 0.7, 0.7)),
                       ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 1)),
                       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                       ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                       ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
                       ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
                       ])  
    table.setStyle(style)
    
    elements.append(table)
    
    #plot generating
    plot_buffer = create_plot(request)
    plot_img = Image(plot_buffer, width=400, height=300)
    elements.append(plot_img)
    # Build the PDF document and return the response
    doc.build(elements)
    # Move the buffer's cursor to the beginning
    buffer.seek(0)

    # Create a FileResponse with the PDF content
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="charttablepdf.pdf"'
    return response






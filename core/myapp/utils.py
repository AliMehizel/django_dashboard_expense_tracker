import matplotlib.pyplot as plt
from .models import *
from io import BytesIO 
def create_plot(request):
    """ 
    - plot bar chart based user data
    - recieve request from transaction
    for generating a pdf file.
    """
    
    transaction_list = Transaction.objects.filter(user=request.user).all()
    if transaction_list.count() > 1:
        x = []
        y = []
        data = [
            ['Description','Amount','Category','Date'],
        ]
        for transaction in transaction_list:
            if transaction.transac_type == 'EXPENSE':
                x.append(transaction.desc)
                y.append(transaction.amount)
      
    else:
        x = []
        y  = []
    

    # Create a bar plot
    plt.bar(x, y,color='red')
    plt.xlabel('Expense')
    plt.ylabel('Amount')
    plt.title('Expense bar chart')
    plt.xticks(x,x)

    # Save the plot as a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return buffer
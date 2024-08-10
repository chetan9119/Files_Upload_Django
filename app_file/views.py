from django.shortcuts import render, redirect
import pandas as pd
from .models import *
# Create your views here.
def model_form_upload(request):
    if request.method == 'POST':
        description = request.POST['description']
        file = request.FILES['file']
        fs = Document(description=description,document=file)
        fs.save()
        file_path = fs.document.path
        
        if file.name.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            print("Invalid file format")
            
        desired_columns = ['Cust State', 'Cust Pin', 'DPD']
        available_columns = [col for col in desired_columns if col in df.columns]
        df_selected = df[available_columns]
    
        summary = {
            'data': df_selected.to_html(index=False),
        }
        return render(request, 'summary.html', {
            'summary': summary
        })    
    return render(request, 'upload.html')
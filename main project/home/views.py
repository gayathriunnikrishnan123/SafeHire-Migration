from django.shortcuts import *
from django.contrib.auth import authenticate, login as auth_login, logout
from django.core.mail import send_mail
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import *
from django.views.decorators.cache import *

@never_cache
@login_required(login_url='login')
def verify_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method=='POST':
        user.is_active=True
        user.is_verified = True
        user.save()
    
    return render(request, 'varify_user.html', {'user': user})










def verifyuser(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.is_active=True
        user.is_verified = True
        user.save()
       
        return redirect('users') 

    return render(request, 'varifyuser.html', {'user': user})


def rejectuser(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.is_active=False
        user.is_verified = False
        user.is_rejected = True  
        user.save()
        
        return redirect('users') 




# Create your views here.
def index(request):
    return render(request,'index.html')


def about(request):
    return render(request,'about.html')


def services(request):
    return render(request,'services.html')

@never_cache
@login_required(login_url='login')
def users(request):
    users = CustomUser.objects.all()
    user_count = users.count()  # Calculate the count of users
   
    context = {
        'users': users,
        'user_count': user_count, 
       # Pass the user count to the template
        
    }
    return render(request,'users.html',context)



from django.shortcuts import render
from django.http import JsonResponse
from .models import WorkCategory
from django.views.decorators.csrf import csrf_exempt

@never_cache
@login_required(login_url='login')
def workcategory(request):
    if request.method == 'POST':
        name = request.POST.get('category-name')
        description = request.POST.get('category-description')
        
        if name:  
            category = WorkCategory(name=name, description=description)
            category.save()
            return redirect("workcategory") 
        
    
    categories = WorkCategory.objects.all()
    return render(request, 'workcategory.html', {'categories': categories})

@never_cache
@login_required(login_url='login')
def delete_category(request, category_id):
    category = get_object_or_404(WorkCategory, pk=category_id)
    if request.method == 'GET':
        category.delete()
        return redirect('workcategory')  # Redirect to the workcategory view after deletion

    return render(request, 'workcategory.html', {'categories': WorkCategory.objects.all()})

@never_cache
@login_required(login_url='login')
def edit_category(request, category_id):
    category = get_object_or_404(WorkCategory, pk=category_id)
    
    if request.method == 'POST':
        # Assuming you have form fields with 'name' and 'description'
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        # Update category fields
        category.name = name
        category.description = description
        category.save()
        
        return redirect('workcategory')  # Redirect to workcategory view after editing
    
    return render(request, 'edit_category.html', {'category': category})
    



@never_cache
@login_required(login_url='login')
def userpage(request):
    # Your view logic goes here
    return render(request, 'userpage.html')

from .models import UserProfile  

from django.core.files.uploadedfile import InMemoryUploadedFile

@never_cache
@login_required(login_url='login')
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Update the user profile fields
        user_profile.user.name = request.POST.get('name')
        user_profile.user.email = request.POST.get('email')
        user_profile.user.phone = request.POST.get('phone')
        user_profile.user.adhar_number = request.POST.get('adhar_number')

        # Handle profile picture
        if request.FILES.get('profile_picture'):
            user_profile.profile_picture = request.FILES.get('profile_picture')

        user_profile.gender = request.POST.get('gender')

        # Save the changes
        user_profile.user.save()
        user_profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')

    return render(request, 'user_profile.html', {'user_profile': user_profile})



@never_cache
@login_required(login_url='login')
def agent_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Update the agent profile fields
        user_profile.user.name = request.POST.get('name')
        user_profile.user.email = request.POST.get('email')
        # Add other fields specific to agent profile editing

        # Save the changes
        user_profile.user.save()
        user_profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('agent_profile')

    return render(request, 'agent_profile.html', {'user_profile': user_profile})
 
@never_cache
@login_required(login_url='login')
def worker_list(request):
    
    workers = MigratoryWorker.objects.filter( is_verified=True)
     
    context = {'workers': workers}
    return render(request, 'worker_list.html', context)

   
from django.shortcuts import get_object_or_404, redirect
from home.models import CustomUser 
@never_cache
@login_required(login_url='login')
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'GET':
        user.delete()
        return redirect('adminpanel')  

    
    return render(request, 'adminpanel.html', {'user': user})






from  django.shortcuts import render
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from .tokens import account_activation_token
from .models import CustomUser, UserProfile  # Make sure to import your models
from django.contrib.sites.models import Site

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Check if the user is already active
        if user.is_active:
            messages.warning(request, "Your account is already activated. You can log in.")
            return redirect('login')

        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, "Thank you for confirming your email. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid or has expired. Please request a new one.")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Activation link is invalid. Please request a new one.")

    return redirect('login')
def activateEmail(request, user):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    to_email = user.email  # Get the user's email from the user object
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user.username}</b>, please go to your email <b>{to_email}</b> inbox and click on \
                the received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')



from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import CustomUser, UserProfile  # Import your models




from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')
        role = request.POST.get('user_type')

        adhar_number = request.POST.get('adharNumber')
        license_number = request.POST.get('licenseNumber')
        police_id = request.POST.get('policeId')
        uploaded_file = request.FILES.get('imageToUpload')

       

        if uploaded_file:
            try:

                # Determine role
                is_employer = role == 'employer'
                is_agent = role == 'agent'
                is_police = role == 'police'

                

                # Assuming CustomUser is an extension of the Django User model
                custom_user = CustomUser(
                    name=name,
                    username=username,
                    email=email,
                    phone=phone,
                    user_type=role,
                    is_employer=is_employer,
                    is_agent=is_agent,
                    is_police=is_police,
                    is_active=False,
                    adhar_number=adhar_number,
                    license_number=license_number,
                    police_id=police_id,
                    uploaded_file= uploaded_file
                )
                custom_user.set_password(password)  # Hash the password
                custom_user.save()

                user_profile = UserProfile(user=custom_user)
                user_profile.save()

                # activateEmail(request, user)

                return redirect('login')
            except Exception as e:
                print(f"Registration failed: {e}")
                return render(request, 'register.html', {'error': 'Registration failed'})
        else:
            return render(request, 'register.html', {'error': 'No file uploaded'})

    return render(request, 'register.html')





def registration_success(request):
    return render(request, 'registration_success.html')


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)

        if username and password:
            user = authenticate(request, username=username, password=password)
            print("authenticated")

            if user is not None:
                request.session['username']=username 
                auth_login(request, user)
                # Redirect based on user_type
                if user.is_admin==True:
                    return redirect('/adminpanel')
                elif user.is_agent==True:
                    return redirect('agentpage')
                elif user.is_employer==True:
                    return redirect('userpage')
                elif user.is_police==True:
                    return redirect('policepage')
                # else:
                #     return redirect('/userpage')
                
            else:
                return HttpResponseRedirect(reverse('login') + '?alert=invalid_credentials')
        else:
            return HttpResponseRedirect(reverse('login') + '?alert=fill_fields')

    # For GET requests or if authentication fails, display the login form
    return render(request, 'login.html')


@never_cache
@login_required(login_url='login')
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

@never_cache
@login_required(login_url='login')
def agentpage(request):
    # Your view logic goes here
    return render(request, 'agentpage.html') 
from django.core.files.uploadedfile import InMemoryUploadedFile


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MigratoryWorker
from django.db import transaction
@never_cache
@login_required(login_url='login')
def addworker(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        dob = request.POST.get('dob_0')
        gender=request.POST.get('gender')
        nationality = request.POST.get('nationality')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        adhar_number = request.POST.get('adhar_number')

        category_id = request.POST.get('work_assign')
        category = WorkCategory.objects.get(id=category_id) if category_id else None

        profile_image = request.FILES.get('profile_image')
        document = request.FILES.get('document')

        worker = MigratoryWorker(
            agent=request.user,
            first_name=first_name,
            dob=dob,
            gender=gender,
            nationality=nationality,
            address=address,
            contact_number=contact_number,
            adhar_number=adhar_number,
            category=category,
            profile_image=profile_image,
            document=document,
        )
        worker.save()
        return redirect('viewworker')

    categories = WorkCategory.objects.all()
    return render(request, 'addworker.html', {'categories': categories})

    

    

@never_cache
@login_required(login_url='login')
def workerprofile(request):
    workers = MigratoryWorker.objects.all()  # Query your model to get the workers
    
    return render(request, 'workerprofile.html', {'workers': workers}) 
@never_cache
@login_required(login_url='login')
def viewprofile(request,worker_id):
    worker = MigratoryWorker.objects.get(id=worker_id)  # Fetch the worker by ID from the database
    
    return render(request, 'viewprofile.html', {'worker': worker})

@never_cache
@login_required(login_url='login')
def workeragent(request, agent_id):
    agent = get_object_or_404(CustomUser, id=agent_id)
    return render(request, 'workeragent.html', {'agent': agent})




@never_cache
@login_required(login_url='login')
def viewworker(request):
    # Assuming 'agent' field in MigratoryWorker model represents the user who added the worker
    user = request.user
    workers = MigratoryWorker.objects.filter(agent=user)  # Filter workers added by the logged-in user
    categories = WorkCategory.objects.all()
    return render(request, 'viewworker.html', {'workers': workers, 'categories': categories})


def verify_worker(request, worker_id):
    worker = get_object_or_404(MigratoryWorker, id=worker_id)
    worker.work_permit_verified = True
    worker.is_verified = True
    worker.is_rejected = False
    worker.save()
    return render(request, 'viewprofile.html', {'worker': worker})

def reject_worker(request, worker_id):
    worker = get_object_or_404(MigratoryWorker, id=worker_id)
    worker.work_permit_verified = False
    worker.is_verified = False
    worker.is_rejected = True
    worker.save()
    return render(request, 'viewprofile.html', {'worker': worker})




@never_cache
@login_required(login_url='login')
def update_worker(request, worker_id):
    worker = get_object_or_404(MigratoryWorker, id=worker_id)

    categories = WorkCategory.objects.all()

    if request.method == 'POST':

        worker.first_name = request.POST['first_name']
        worker.dob = request.POST['dob']
        worker.nationality = request.POST['nationality']
        worker.address = request.POST['address']
        worker.contact_number = request.POST['contact_number']
        worker.adhar_number = request.POST['adhar_number']

        category_id = request.POST.get('work_assign')
        selected_category = WorkCategory.objects.get(pk=category_id)
        worker.category = selected_category

        worker.gender = request.POST.get('gender')

        if 'profile_image' in request.FILES:
            worker.profile_image = request.FILES['profile_image']

        if 'document' in request.FILES:
            worker.document = request.FILES['document']

        worker.save()
        return redirect('viewworker')
    return render(request, 'update_worker.html', {'worker': worker, 'categories': categories})

from django.shortcuts import render, redirect, get_object_or_404
@never_cache
@login_required(login_url='login')
def delete_worker(request, worker_id):
   
    worker = get_object_or_404(MigratoryWorker, id=worker_id)
    if request.method == 'GET':
       
        worker.delete()
       
        return redirect('viewworker')  

    return render(request, 'viewworker.html', {'worker': worker})


@never_cache
@login_required(login_url='login')
def policepage(request):
    # Your view logic goes here
    return render(request, 'policepage.html') 

@never_cache
@login_required(login_url='login')
def incidentreported(request):
    total_added = MigratoryWorker.objects.count()  # Total number of workers added
    total_verified = MigratoryWorker.objects.filter(is_verified=True).count()  # Total number of workers verified
    total_rejected = MigratoryWorker.objects.filter(is_rejected=True).count()  # Total number of workers rejected

    return render(request, 'incidentreported.html', {
        'total_added': total_added,
        'total_verified': total_verified,
        'total_rejected': total_rejected
    })
   
@never_cache
@login_required(login_url='login')
def activeofficers(request):
    # Fetch all police officers
    police_officers = CustomUser.objects.filter(user_type='police')


    return render(request, 'activeofficers.html', {'police_officers': police_officers})
    


@never_cache
@login_required(login_url='login')
def adminpanel(request):
    users = CustomUser.objects.all()
    user_count = users.count()  # Calculate the count of users
   
    context = {
        'users': users,
        'user_count': user_count, 
       # Pass the user count to the template
        
    }
    
    return render(request,'adminpanel.html',context)

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse
from .models import MigratoryWorker  # Import your model
from datetime import date

@csrf_exempt
def generate_work_permit_pdf(request, worker_id):
    worker = MigratoryWorker.objects.get(id=worker_id)

    permit_data = {
        'worker_id': worker.id,
        'name': worker.first_name,
        'dob': str(worker.dob),
        'nationality': worker.nationality,
        'contact_number': worker.contact_number,
        'adhar_number': worker.adhar_number,
        'work_assigned': worker.category.name,
        'issue_date': str(date.today()),
        'expiry_date': str(worker.dob.year + 60),
        'issuing_authority': 'Local Immigration Office',
        'additional_details': 'Valid for employment with the specified employer and in the specified occupation.',
    }

    template = get_template('work_permit_template.html')
    html = template.render({'permit_data': permit_data})

    # Create a response object with appropriate headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="work_permit_{worker.id}.pdf"'

    # Generate PDF and write it to the response
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('PDF generation error', status=500)

    return response

from django.shortcuts import render, get_object_or_404
from .models import CustomUser, MigratoryWorker, JobSubmission


@never_cache
@login_required(login_url='login')


def agent_contact(request, agent_id, worker_id):
    
    agent = get_object_or_404(CustomUser, id=agent_id)

    worker = get_object_or_404(MigratoryWorker, id=worker_id)


    assigned_job = JobSubmission.objects.filter(title=worker.category.id, employer=request.user)
    
    context = {'agent': agent, 'worker': worker, 'jobs': assigned_job}
    return render(request, 'agent_contact.html', context)





from django.shortcuts import render, redirect, get_object_or_404
from .models import JobSubmission
from .models import WorkCategory  # Import WorkCategory model if not imported already
from .models import JobSubmission, WorkCategory, CustomUser, MigratoryWorker

def works_available(request):
    employer = request.user

    if request.method == 'POST':
        # Extract form data
        category_name = request.POST.get('jobTitle')
        work_type = request.POST.get('workType')
        from_date = request.POST.get('fromDate')
        to_date = request.POST.get('toDate')
        district = request.POST.get('district')  # Ensure correct district retrieval
        city = request.POST.get('city')
        category = get_object_or_404(WorkCategory, name=category_name)

        # Create and save JobSubmission instance
        job_submission = JobSubmission(
            title=category,  # Assign the category object
            work_type=work_type,
            from_date=from_date,
            to_date=to_date,
            district=district,
            city=city,
            employer=employer,
        )
        job_submission.save()

        # Redirect to joblist view with employer ID
        return redirect('joblist', employer_id=employer.id)

    return render(request, 'works_available.html', {'categories': WorkCategory.objects.all(),'employer':employer})





        

from django.shortcuts import render
from .models import JobSubmission

def jobs(request):
    # Fetch submitted jobs from the database
     submitted_jobs = JobSubmission.objects.all()

     return render(request, 'jobs.html', {'submitted_jobs':submitted_jobs})

 
from django.shortcuts import render, redirect
from .models import SalaryPayment
from datetime import datetime
def salary(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        worker_name = request.POST.get('name')
        worker_id = request.POST.get('id')
        amount = request.POST.get('amount')
        worker = get_object_or_404(MigratoryWorker, id=worker_id)
        worker.status=None
        worker.save()
        payment_date = datetime.now()
        card_holder_name = request.POST.get('card_name')
        card_number = request.POST.get('card_no')
        cvv = request.POST.get('cvv')
        payment_status = 'Completed'  # Assume payment is successful by default

        # Create SalaryPayment instance
        salary_payment = SalaryPayment.objects.create(
            name=worker_name,
            amount=amount,
            payment_date=payment_date,
            card_holder_name=card_holder_name,
            card_number=card_number,
            cvv=cvv,
            payment_status=payment_status,
            worker=worker
        )

        # Update the status of the corresponding BookingWorker object
        booking_worker = BookingWorkers.objects.exclude(worker=worker, status='Paid').first()

        booking_worker.status = 'Paid'
        booking_worker.save()

        return redirect('salary')  # Redirect to a success page or another URL

    return render(request, 'salary.html')


from django.shortcuts import render
from .models import SalaryPayment

def payment_details(request):
    payments = SalaryPayment.objects.all()
    return render(request, 'payment_details.html', {'payments': payments})


def setting(request):
    payments = SalaryPayment.objects.all()
    return render(request, 'setting.html', {'payments': payments})


@never_cache
@login_required(login_url='login')

def book_worker(request, agent_id, worker_id):
    if request.method == 'POST':
        jobid = request.POST.get('job_submission_id')
        print(jobid)
        employer = request.user
        agent = get_object_or_404(CustomUser, id=agent_id)  # Get the agent
        worker = get_object_or_404(MigratoryWorker, id=worker_id)  # Get the worker
        job_submission = get_object_or_404(JobSubmission, id=jobid)  # Get the job submission
        
        # Create a booking record
        booking = BookingWorkers.objects.create(
            employer=employer,
            agent=agent,
            worker=worker,
            job_submission=job_submission  # Assign the job submission instance
        )
        worker.status = "onduty"
        worker.employer = employer
        worker.save()
        return redirect('agent_contact', agent_id=agent_id, worker_id=worker_id)


def booking_workers_view(request, user_id):
    booking_workers = BookingWorkers.objects.filter(agent=user_id)
    return render(request, 'booking_workers.html', {'booking_workers': booking_workers})




from django.shortcuts import render
from django.http import HttpResponse

def document_verification(request):
    verification_result = None
    
    if request.method == 'POST' and request.FILES.get('document'):
       
        verification_result = "Document verified successfully."
        
    return render(request, 'document.html', {'verification_result': verification_result})


def joblist(request, employer_id):
   
    employer_jobs = JobSubmission.objects.filter(employer=employer_id)

    return render(request, 'joblist.html', {'job_submissions': employer_jobs})

def bookings(request, user_id):
    # Filter bookings based on the employer and where the status is not 'Paid'
    bookings = BookingWorkers.objects.filter(employer=user_id).exclude(status='Paid')

    return render(request, 'bookings.html', {'bookings': bookings})


# import numpy as np
# from PIL import Image
# import tensorflow as tf
# from tensorflow.keras.applications import VGG16
# from tensorflow.keras.applications.vgg16 import preprocess_input
# from scipy.spatial.distance import cosine

# # Load pre-trained VGG16 model
# base_model = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))

# # Remove the classification layers
# feature_extractor = tf.keras.Model(inputs=base_model.input, outputs=base_model.layers[-1].output)

# # Load and preprocess new image
# def preprocess_image(image_path):
#     img = Image.open(image_path)
#     img = img.resize((150, 150))
#     img_array = np.expand_dims(np.array(img), axis=0)
#     return preprocess_input(img_array)

# new_image_path = 'sample.jpg'
# new_image_features = feature_extractor.predict(preprocess_image(new_image_path))

# # Load dataset features
# def load_dataset_features():
#     # Your code to load the features of your dataset
#     # Replace this with your actual code to load the features
#     dataset_features = [...]  # Replace [...] with your actual dataset features
#     return dataset_features

# # Load dataset features
# dataset_features = load_dataset_features()

# # Compute similarity with images in dataset
# threshold = 0.5  # Adjust this threshold based on your dataset
# verified = False
# for image_features in dataset_features:
#     # Check if image_features is ellipsis
#     if isinstance(image_features, Ellipsis):
#         continue

#     similarity = 1 - cosine(new_image_features.flatten(), image_features.flatten())
#     if similarity > threshold:
#         verified = True
#         break

# if verified:
#     print("Image verified.")
# else:
#     print("Image not verified.")


def pay_salary(request, booking_id):
    booking = get_object_or_404(BookingWorkers, id=booking_id)
    
    # Check if the status is not 'Paid'
    if booking.status != 'Paid':
        return render(request, 'salary.html', {'booking': booking})
    else:
        return render(request, 'bookings.html')
        


def worker_tracked(request):

    # Filter bookings based on the employer
    bookings = BookingWorkers.objects.all()
    print(bookings)
    return render(request, 'worker_tracked.html', {'bookings': bookings})



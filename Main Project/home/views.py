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

@never_cache
@login_required(login_url='login')
def agent_contact(request, agent_id, worker_id):
    agent = CustomUser.objects.get(id=agent_id) 
    worker = MigratoryWorker.objects.get(id=worker_id)  
    context = {'agent': agent,
               'worker':worker}
    return render(request, 'agent_contact.html', context)

from django.shortcuts import render, redirect
from .models import BookingWorker, CustomUser, MigratoryWorker
from django.http import JsonResponse


@never_cache
@login_required(login_url='login')
def book_worker(request, agent_id, worker_id):
    if request.method == 'POST':
        duration = request.POST.get('duration')
        duration_unit = request.POST.get('durationUnit')

        employer = request.user  # Assuming the user making the request is the employer
        agent = CustomUser.objects.get(id=agent_id)  # Get the agent
        worker = MigratoryWorker.objects.get(id=worker_id)  # Get the worker

        # Create a booking record
        booking = BookingWorker.objects.create(
            employer=employer,
            agent=agent,
            worker=worker,
            duration=duration,
            duration_unit=duration_unit,
            status='pending'  # You might want to set an initial status
        )

        # You can add additional logic here, such as sending notifications to the agent, etc.

        return redirect('agent_contact', agent_id=agent_id, worker_id=worker_id)
    
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import BookingWorker
from django.contrib.auth.decorators import login_required

@never_cache
@login_required(login_url='login')
def notification(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(BookingWorker, id=booking_id)

        if request.POST.get('action') == 'accept':
            # Accept the booking
            booking.is_accepted = True
            booking.status = 'accepted'
            booking.save()
        elif request.POST.get('action') == 'reject':
            # Reject the booking
            booking.is_rejected = True
            booking.status = 'rejected'
            booking.save()

    agent_id = request.user.id
    bookings = BookingWorker.objects.filter(agent__id=agent_id)

    return render(request, 'notification.html', {'bookings': bookings})


@never_cache
@login_required(login_url='login')
def bookings(request):
    employer = request.user
    bookings = BookingWorker.objects.filter(employer=employer)

    # Create a list to store booking and payment information
    booking_data = []

    for booking in bookings:
        # Assuming each booking has a related Payment, you can fetch it like this
        payment = Payment.objects.filter(booking=booking).first()

        # Add a dictionary with booking and payment information to the list
        booking_data.append({'booking': booking, 'payment': payment})

    return render(request, 'bookings.html', {'booking_data': booking_data})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
import razorpay
import logging

logger = logging.getLogger(__name__)


def handle_payment(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        worker_id = request.POST.get('worker_id')

        booking = get_object_or_404(BookingWorker, id=booking_id)
        worker = MigratoryWorker.objects.get(id=worker_id)
        print("id is",booking_id)

        # Define your fixed security amount here
        fixed_security_amount = 50000  # Adjust this amount as needed

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        try:
            # Verify the Razorpay payment
            payment = client.payment.fetch(razorpay_payment_id)
            logger.info(f'Razorpay Payment Response: {payment}')

            if payment['order_id'] == razorpay_order_id:
                # Check if payment is successful
                if payment['status'] in ['authorized', 'captured']:
                    # Calculate the actual payment amount (subtract the security amount)
                    actual_payment_amount = (50000) / 100

                    # Ensure the actual payment amount is at least zero
                   

                    # Payment successful
                    Payment.objects.create(
                        employer=request.user, worker=worker,
                        booking=booking,
                        amount=actual_payment_amount,
                        razorpay_order_id=razorpay_order_id,
                        razorpay_payment_id=razorpay_payment_id,
                        is_paid=True
                    )

                    # Update booking status or perform other actions as needed
                    booking.status = 'accepted'  # Update to the correct status
                    booking.save()

                    return redirect('bookings')
                else:
                    logger.error('Payment verification failed. Payment status: {}'.format(payment['status']))
                    return JsonResponse({'success': False, 'message': 'Payment verification failed'})
            else:
                logger.error('Invalid order ID')
                return JsonResponse({'success': False, 'message': 'Invalid order ID'})
        except Exception as e:
            logger.error(f'Razorpay Verification Error: {e}')
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request'})
    

    
    
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_payment_receipt_pdf(request, booking_id):
    # Get the booking and related data
    booking_data = get_object_or_404(BookingWorker, id=booking_id)

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object using the BytesIO buffer
    pdf = canvas.Canvas(buffer)

    # Generate the PDF content
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 800, f"Payment Receipt")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(100, 780, f"Worker: {booking_data.worker}")
    pdf.drawString(100, 760, f"Agent: {booking_data.agent}")

    payment = Payment.objects.get(booking=booking_data)

    pdf.drawString(100, 720, f"Payment Date: {payment.date}")
    pdf.drawString(100, 700, f"Payment Amount: Rs. {payment.amount}")
    pdf.drawString(100, 740, f"Note: You have paid a security deposit of Rs. 500 for the worker.")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    
    # Set content type to 'application/pdf' and provide the PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=payment_receipt_booking_{booking_data.id}.pdf'
    response.write(buffer.getvalue())
    
    return response
   




from rest_framework.generics import ListAPIView


class WorkerListView(ListAPIView):
    queryset = MigratoryWorker.objects.all()
    template_name = 'worker_list.html'

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
       

 


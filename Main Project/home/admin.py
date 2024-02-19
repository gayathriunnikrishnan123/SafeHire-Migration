from django.contrib import admin
from .models import *



admin.site.register(CustomUser)
admin.site.register(MigratoryWorker)
admin.site.register(WorkCategory)
admin.site.register(Police)
admin.site.register(BookingWorker)
admin.site.register(Payment)
admin.site.register(JobSubmission)
admin.site.register(SalaryPayment)


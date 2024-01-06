from django.contrib import admin

from portfolioapp.models import Education, Experience, Testimonial, Projects, Skills, Emails, Badge

# Register your models here.

admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Testimonial)
admin.site.register(Projects)
admin.site.register(Skills)
admin.site.register(Emails)
admin.site.register(Badge)

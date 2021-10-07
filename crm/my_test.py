# import os
# import django
# import math
#
#
# # def toFixed(numObj, digits=0):
# #     return f"{numObj:.{digits}f}"
#
# os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings'
# django.setup()
# from crm.models import Company, Project
#
# companies = Company.objects.all()
# for company in companies:
#     print(company.short_name)
# projects = Project.objects.all()
# print(projects.filter(company=companies[4]))
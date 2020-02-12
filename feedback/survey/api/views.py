from rest_framework.generics import ListAPIView

from survey.models import Department

class DepartmentListAPIView(ListAPIView):
    queryset = Department.objects.all()

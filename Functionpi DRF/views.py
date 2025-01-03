from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer

@api_view(["GET", "POST", "PUT", "DELETE"])
def studentapi(request, pk=None):
    if request.method == "GET":
        if pk is not None:
            student = Student.objects.filter(id=pk).first()
            if student is None:
                return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        if pk is not None:
            student = Student.objects.filter(id=pk).first()
            if student is None:
                return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if pk is not None:
            student = Student.objects.filter(id=pk).first()
            if student is None:
                return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
            student.delete()
            return Response({"message": "Student deleted successfully"}, status=status.HTTP_200_OK)

    return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

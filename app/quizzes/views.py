# from django.core.mail import send_mail
# from rest_framework.views import APIView
# from rest_framework import generics, status
# from rest_framework.response import Response

# class QuizParticipantsView(generics.GenericAPIView):
#     serializer_class = GoogleCalendarIntegrationSerializer
#     permission_classes = (AvatarPermission,)

#     def post(self, request, format=None):
#         to_email = request.data.get("to_email")
#         serializer = self.get_serializer(obj, data=request.data)
#         send_mail(
#             'Subject here',
#             'Here is the message.',
#             'from@example.com',
#             ['to_email'],
#             fail_silently=False,
#         )
#         return Response({"message": "e-mail has been sent successfully"},
#                         status=status.HTTP_200_OK)

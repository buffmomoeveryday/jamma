# import re
# from datetime import timedelta

# from django.utils import timezone

# from track.models import Session, PageView, Website
# from track.tasks import create_session


# class SessionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)

#         if request.method == "GET":
#             self.process_request(request)

#         return response

#     def process_request(self, request):
#         ip_address = request.META.get("REMOTE_ADDR")
#         user_agent = request.META.get("HTTP_USER_AGENT")
#         current_time = timezone.now()
#         website = self.get_website(request)

#         if not website:
#             return

#         try:
#             session = Session.objects.filter(
#                 website=website,
#                 ip_address=ip_address,
#                 user_agent=user_agent,
#                 end_time__isnull=True,
#             ).latest("start_time")

#             if current_time - session.start_time > timedelta(minutes=30):
#                 session.end_time = current_time
#                 session.save()
#                 self.create_new_session(
#                     request, website, ip_address, user_agent, current_time
#                 )
#             else:
#                 session.end_time = current_time
#                 session.save()
#         except Session.DoesNotExist:
#             self.create_new_session(
#                 request, website, ip_address, user_agent, current_time
#             )

#     def create_new_session(
#         self, request, website, ip_address, user_agent, current_time
#     ):
#         create_session.delay(
#             website=website.id,
#             ip_address=ip_address,
#             user_agent=user_agent,
#             start_time=current_time,
#             end_time=None,
#         )

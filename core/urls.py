from django.urls import path
from . import views
urlpatterns = [
    path('profile/',views.profile,name = 'profile'),
    path('update_profile/',views.Update_profile.as_view(),name = 'update_profile'),
    path('book_details/<int:pk>',views.Book_Details.as_view(),name = 'book_details'),
    path('deposite/',views.DipositeView.as_view(),name= 'deposite'),
    path('borrowing/<int:id>',views.borrowing,name = 'borrowing'),
    path('return/<int:id>',views.return_book,name = 'return'),
    path('add_review/<int:book_id>',views.add_review,name = 'review'),
    path('show_review/',views.show_review,name = 'show_review'),
]
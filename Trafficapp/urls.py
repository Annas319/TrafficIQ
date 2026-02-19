from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Public Pages
    path('', views.landing_page, name='landing'),
    path('rules/', views.rules, name='rules'),
    path('tutorials/', views.tutorials, name='tutorials'),
    # path("tutorials/road-signs/", views.road_signs, name="road_signs"),
    # path("tutorials/driving-tips/", views.driving_tips, name="driving_tips"),
    # path("tutorials/safety-rules/", views.safety_rules, name="safety_rules"),

# Tutorials (Admin)
path("manage-tutorials/", views.manage_tutorials, name="manage_tutorials"),
path("manage-tutorials/add/", views.add_tutorial, name="add_tutorial"),
path("manage-tutorials/delete/<int:tutorial_id>/", views.delete_tutorial, name="delete_tutorial"),



    
    # Quiz (User side)
    path('quiz/', views.quiz_list, name='quiz_list'),          # ✅ show tests (Test 1, Test 2, ...)
    path("quiz/<int:test_id>/", views.take_quiz, name="take_quiz"),  # ✅ show questions inside test
    path("start-quiz/", views.start_quiz, name="start_quiz"),
    path("quiz-result/<int:test_id>/", views.quiz_result, name="quiz_result"),

    # Auth
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),

    #Forget Password
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<str:username>/", views.reset_password, name="reset_password"),
    
    # Admin Dashboard
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("manage-users/", views.manage_users, name="manage_users"),
    path("add-content/", views.add_content, name="add_content"),
    path("reports/", views.reports, name="reports"),

    # Quiz Management (Admin only)
    
    path("quiz_tests/", views.quiz_tests, name="quiz_tests"),
    path("admin-dashboard/add-test/", views.add_quiz_test, name="add_quiz_test"),
    path("admin-dashboard/<int:test_id>/questions/", views.quiz_questions, name="quiz_questions"),
    path("admin-dashboard/<int:test_id>/questions/add/", views.add_quiz_question, name="add_quiz_question"),
    
    # Admin Quiz Management
    path("admin-dashboard/quiz-tests/", views.quiz_tests, name="quiz_tests"),
    path("admin-dashboard/quiz-tests/<int:test_id>/edit/", views.edit_quiz_test, name="edit_quiz_test"),
    path("admin-dashboard/quiz-tests/<int:test_id>/delete/", views.delete_quiz_test, name="delete_quiz_test"),
    
    path("admin-dashboard/<int:test_id>/questions/", views.quiz_questions, name="quiz_questions"),
    path("admin-dashboard/<int:test_id>/questions/add/", views.add_quiz_question, name="add_quiz_question"),
    path("admin-dashboard/<int:test_id>/questions/<int:question_id>/edit/", views.edit_quiz_question, name="edit_quiz_question"),
    path("admin-dashboard/<int:test_id>/questions/<int:question_id>/delete/", views.delete_quiz_question, name="delete_quiz_question"),

    # User Management (Admin only)
    path("manage-users/", views.manage_users, name="manage_users"),
    path("manage-users/remove/<int:user_id>/", views.remove_user, name="remove_user"),
    path("manage-users/report/<int:user_id>/", views.user_report, name="user_report"),
    
    path("manage-users/create-admin/", views.create_admin, name="create_admin"),
    path("manage-users/create-user/", views.create_user, name="create_user"),


    path("manage-rules/", views.manage_rules, name="manage_rules"),
    path("manage-rules/add/", views.add_rule, name="add_rule"),
    path("manage-rules/edit/<int:rule_id>/", views.edit_rule, name="edit_rule"),
    path("manage-rules/delete/<int:rule_id>/", views.delete_rule, name="delete_rule"),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone
from datetime import timedelta
from .models import *

from .forms import FeedbackForm, AvatarUploadForm
import requests
from django.contrib.auth.decorators import login_required
import json
from decimal import Decimal

# views.py
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

import openai

from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models import Q
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password


# lấy danh sách các bài viết và trang hiện tại

def get_articles_page(request):
    articles = Article.objects.filter(IsApproved=True).order_by('-ArticleID')
    paginator = Paginator(articles, 5)

    # Lấy số trang từ tham số truy vấn trong URL
    page_number = request.GET.get('page')

    # Lấy đối tượng trang (page) từ đối tượng Paginator dựa trên số trang
    page = paginator.get_page(page_number)

    # Trả về đối tượng trang để sử dụng trong template
    return page


# lấy danh sách các vùng trồng
def get_growing_regions():
    growing_regions = GrowingRegion.objects.all()
    return growing_regions


openai_api_key = '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'
openai.api_key = openai_api_key


# gọi chat_gpt
def ask_openai(message):
    print('hello')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            # {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )

    answer = response.choices[0].message.content.strip()
    return answer


# chuyển đổi kiểu Decimal(số thập phân) thành kiểu str
def decimal_to_str(obj):
    if isinstance(obj, Decimal):
        return str(obj)


# đếm sl thông báo bài viết/bình luận
def count_unread_notifications(user):
    user_articles = Article.objects.filter(User=user)
    # Lấy danh sách các thông báo liên quan đến bài viết của người đăng và bình luận của họ
    notification_counts = Feedback.objects.filter(
        (Q(Article__in=user_articles) & ~Q(User=user)) |
        (Q(ParentFeedback__User=user) & ~Q(User=user))
    )

    # is_notification=True người bình luận ko phải là người đăng bài viết
    # ParentFeedback__isnull=Fals bình luận cha có giá trị

    # Lọc chỉ những thông báo chưa đọc
    unread_notifications = notification_counts.filter(is_read=False).count()

    return unread_notifications


# hiển thị nội dung thông báo bài viết/bình luận
def display_notifications(request):
    if request.user.is_authenticated:

        # Lấy danh sách các bài viết do người đăng hiện tại tạo
        user_articles = Article.objects.filter(User=request.user)

        # Lọc các thông báo chỉ lấy những thông báo liên quan đến bài viết của người đăng hoặc phản hồi bình luận của mình 
        notifications = Feedback.objects.filter(
            (Q(Article__in=user_articles) & ~Q(User=request.user)) |
            (Q(ParentFeedback__User=request.user) & ~Q(User=request.user))
        ).order_by('-FeedbackID')

        return notifications

    # Trả về một danh sách trống nếu người dùng chưa đăng nhập hoặc không có thông báo nào.
    return []


# @login_required(login_url='/login')
def home(request):
    articles = get_articles_page(request)
    growing_regions = get_growing_regions()
    notifications = Notification.objects.all()
    locations = Location.objects.filter(
        fruits__article__IsApproved=True
    ).distinct()

    # mùa vụ
    seasonPlan = SeasonPlan.objects.all()

    if request.user.is_authenticated:
        chats = Chat.objects.filter(user=request.user)
    else:

        chats = []

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})

    # Chuyển đổi danh sách locations thành chuỗi JSON và trả về nó bằng JsonResponse
    locations_json = [
        {
            'fruit_name': fruit.FruitName,
            'id_article': articl.ArticleID,
            'Name': location.Name,
            'FruitType': location.FruitType,
            'Latitude': decimal_to_str(location.Latitude),
            'Longitude': decimal_to_str(location.Longitude)
        }
        for location in locations

        # Sử dụng all() để lấy tất cả các đối tượng Fruit liên quan
        for fruit in location.fruits.all()
        for articl in fruit.article.all()

    ]

    # gọi hàm để hiển thị thông báo
    display_notification = display_notifications(request)

    # gọi hàm để hiển thị số lượng thông báo
    if request.user.is_authenticated:
        unread_count = count_unread_notifications(request.user)
    else:
        unread_count = 0

    # giá nông sản
    ProductPrices = ProductPrice.objects.all()

    # avtUser
    if request.user.is_authenticated:
        user = request.user
        try:
            avt = UserAvatar.objects.get(user=user)
        except UserAvatar.DoesNotExist:
            avt = None
    else:
        avt = None
    items = Items.objects.all()
    newspapers = Newspaper.objects.all()

    return render(request, 'quantri/index.html', {
        'count': unread_count,
        'chats': chats,
        'seasonPlan': seasonPlan,
        'notifications': notifications,
        'articles': articles,
        'growing_regions': growing_regions,
        'locations_json': json.dumps(locations_json),
        'display_notification': display_notification,
        'ProductPrices': ProductPrices,
        'avt': avt,
        'items': items,
        'newspapers': newspapers,
    })


# hàm hiển thị thông báo của admin
def notification(request, id):
    notification = get_object_or_404(Notification, NotificationID=id)

    # gọi hàm để hiển thị số lượng thông báo
    user = request.user

    if user.is_authenticated:
        count = count_unread_notifications(user)
        display_notification = display_notifications(request)
    else:
        count = 0
        display_notification = None

    return render(request, 'quantri/notification.html',
                  {'display_notification': display_notification, 'count': count, 'notification': notification, })


# hiển thị ra chị tiết bài viết
def article_detail(request, id):
    article = get_object_or_404(Article, ArticleID=id)

    fruitid = article.FruitID
    fruit_conte = FruitContent.objects.filter(fruit=fruitid)

    # images = Image.objects.filter(FruitID=article.FruitID_id)
    user_article = User.objects.get(id=article.User.id)
    try:
        user_avt = UserAvatar.objects.get(user=user_article)
    except UserAvatar.DoesNotExist:
        user_avt = None  # Hoặc có thể thiết lập một giá trị mặc định khác

    videos = Video.objects.filter(FruitID=article.FruitID_id)
    Location = fruitid.Location
    growing_region = Location.GrowingRegion

    # Lấy tất cả các đối tượng Location của GrowingRegion
    all_locations = growing_region.location_set.all()
    all_locations_info = []
    for location in all_locations:
        fruits_info = location.fruits.all()

        for fruit in fruits_info:

            articles = Article.objects.filter(FruitID=fruit.FruitID)

            for article in articles:
                fruit_info = {
                    'fruit_name': fruit.FruitName,
                    'location_name': location.Name,
                    'latitude': decimal_to_str(location.Latitude),
                    'longitude': decimal_to_str(location.Longitude),
                    'FruitType': location.FruitType,
                    'id_article': article.ArticleID,
                }
                all_locations_info.append(fruit_info)

    # location_names = [info['location_name'] for info in all_locations_info]
    feedbacks = Feedback.objects.filter(Article=article)
    feedback_form = FeedbackForm()
    reply_form = FeedbackForm()
    user_avatars = {}

    for feedback in feedbacks:
        # Lấy thông tin người dùng từ trường User của Feedback
        user = feedback.User

        try:
            user_avatar = UserAvatar.objects.get(user=user)
            if user_avatar.avatar:
                user_avatars[user.id] = user_avatar.avatar.url
            else:
                user_avatars[user.id] = None
        except UserAvatar.DoesNotExist:
            user_avatars[user.id] = None

    growing_regions = get_growing_regions()

    # Chuyển đổi giá trị Decimal thành kiểu float hoặc str trước khi đưa vào JSON
    latitude_value = decimal_to_str(Location.Latitude)
    longitude_value = decimal_to_str(Location.Longitude)

    # Tạo một từ điển chứa thông tin về Location
    location_info = {
        'name': Location.Name,
        'latitude': latitude_value,
        'longitude': longitude_value,
        'fruit_name': fruit.FruitName,
        'FruitType': Location.FruitType,

    }

    # Chuyển từ điển thành chuỗi JSON
    # location_json = json.dumps(location_info)
    user = request.user  # Lấy thông tin người dùng hiện tại

    # gọi hàm để hiển thị số lượng thông báo
    if request.user.is_authenticated:
        unread_count = count_unread_notifications(request.user)
    else:
        unread_count = 0
    # gọi hàm để hiển thị thông báo
    display_notification = display_notifications(request)

    # bài viết liên quan
    related_articles = Article.objects.filter(FruitID=fruitid.FruitID).exclude(ArticleID=id)[:5]

    return render(request, 'quantri/article_list.html', {
        'article': article,
        # 'images': images,
        'growing_region': growing_region,
        'feedbacks': feedbacks,
        'feedback_form': feedback_form,
        'reply_form': reply_form,
        'growing_regions': growing_regions,
        'user_avatars': user_avatars,
        'fruit': fruitid,  # Truyền user_avatars vào context để truyền đến template
        'Location': Location,
        'location_json': json.dumps(location_info),
        'user': user,
        'videos': videos,
        'count': unread_count,
        'display_notification': display_notification,
        'related_articles': related_articles,
        'fruit_conte': fruit_conte,
        'user_article': user_article,
        'user_avt': user_avt,
        'all_locations': all_locations,
        'all_locations_info': json.dumps(all_locations_info),
        # 'location_names': location_names,

    })


# thêm bình luận bài viết
@login_required(login_url='/login')
def add_comment(request, id):
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            try:
                article = Article.objects.get(ArticleID=id)
                parent_comment_id = request.POST.get('EditCommentID')  # Lấy ID của bình luận cha (nếu có)

                if parent_comment_id:
                    # Nếu có ID của bình luận cha, tạo một phản hồi cho nó
                    parent_comment = Feedback.objects.get(FeedbackID=parent_comment_id)
                    feedback = feedback_form.save(commit=False)  # commit=False thực hiện thêm các bước trước khi lưu
                    feedback.User = request.user
                    feedback.Article = article
                    feedback.ParentFeedback = parent_comment  # Gán bình luận cha
                    feedback.save()

                    # Tạo thông báo cho tác giả bài viết
                    # if request.user != article.User:
                    #     # feedback.is_notification = True #phân biệt người đăng với người dùng
                    #     feedback.notification_message = f"{request.user.username} đã phản hồi bình luận của bạn."
                    #     feedback.save()

                    # Tạo thông báo cho người phản hồi cha nếu người phản hồi không phải là người phản hồi cha
                    if parent_comment.User != request.user:
                        # feedback.is_notification = True
                        feedback.notification_message = f"{request.user.username} đã phản hồi bình luận của {parent_comment.User.username}."
                        feedback.save()
                else:
                    # Nếu không có ID của bình luận cha, tạo bình luận gốc
                    feedback = feedback_form.save(commit=False)
                    feedback.User = request.user
                    feedback.Article = article
                    feedback.save()

                    # Tạo thông báo cho tác giả bài viết
                    if request.user != article.User:
                        # feedback.is_notification = True
                        feedback.notification_message = f"{request.user.username} đã bình luận vào bài viết của bạn."
                        feedback.save()
            except Article.DoesNotExist:
                # Xử lý khi bài viết không tồn tại
                pass
    return redirect('post:article_detail', id=id)


# sửa bình luận
def edit_comment(request):
    if request.method == 'POST':
        edit_comment_id = request.POST.get('EditCommentID')
        comment = get_object_or_404(Feedback, FeedbackID=edit_comment_id)

        # Kiểm tra quyền truy cập của người dùng
        if comment.User == request.user:
            feedback_form = FeedbackForm(request.POST, instance=comment)  # instance chỉ định from đang chỉnh sửa
            if feedback_form.is_valid():
                feedback = feedback_form.save()
                # messages.success(request, 'Bình luận đã được chỉnh sửa thành công.')

                # Tạo thông báo cho tác giả bài viết
                article = comment.Article  # Lấy bài viết liên quan đến bình luận
                if request.user != article.User:
                    # feedback.is_notification = True
                    feedback.is_read = False
                    feedback.notification_message = f"{request.user.username} đã chỉnh sửa bình luận về bài viết của bạn."
                    feedback.save()
                return redirect('post:article_detail', id=comment.Article_id)
            else:
                messages.error(request, 'Có lỗi xảy ra khi chỉnh sửa bình luận.')
        else:
            messages.error(request, 'Bạn không có quyền chỉnh sửa bình luận này.')

    return redirect('post:article_detail', id=comment.Article_id)


# xóa bình luận bài viết
def delete_comment(request, comment_id):
    # Lấy bình luận bằng cách sử dụng get_object_or_404 để xử lý trường hợp không tồn tại
    comment = get_object_or_404(Feedback, FeedbackID=comment_id)

    # Lấy article_id từ trường feeaback của bình luận để hiển thị lại trang bài viết đấy
    article_id = comment.Article_id

    # Kiểm tra xem người dùng có quyền xóa bình luận không
    if comment.User == request.user:
        article = comment.Article  # Lấy bài viết liên quan đến bình luận
        feedbacks = Feedback.objects.filter(Article=article)

        # thông báo
        # Lặp qua từng feedback liên quan đến bài viết và tạo thông báo
        for feedback in feedbacks:
            if request.user != article.User:
                # feedback.is_notification = True
                feedback.notification_message = f"{request.user.username} đã xóa bình luận về bài viết của bạn."
                feedback.save()

        comment.delete()

        # Tạo một thông báo thành công
        # messages.success(request, 'Bình luận đã được xóa thành công.')
    else:
        # Tạo một thông báo lỗi
        messages.error(request, 'Bạn không có quyền xóa bình luận này.')

    # Chuyển hướng đến trang bài viết sau khi xóa, sử dụng article_id
    return redirect('post:article_detail', id=article_id)


# tìm kiếm
def search_view(request):
    query = request.GET.get('q')

    if not query:
        return redirect('post:home')
    if query:
        results = Article.objects.filter((Q(Title__icontains=query) | Q(Content__icontains=query) |
                                          Q(FruitID__FruitName__icontains=query)) & Q(IsApproved=True)).order_by(
            '-ArticleID')  # icontains tìm kiêm skhoong phân biệt hoa thường
    growing_regions = get_growing_regions()

    # Chuyển đổi danh sách locations thành chuỗi JSON và trả về nó bằng JsonResponse
    locations_json = [
        {
            'fruit_name': article.FruitID.FruitName,
            'Name': article.FruitID.Location.Name,
            'FruitType': article.FruitID.Location.FruitType,
            'Latitude': decimal_to_str(article.FruitID.Location.Latitude),
            'Longitude': decimal_to_str(article.FruitID.Location.Longitude),
            'id_article': article.ArticleID,
        }
        for article in results
    ]

    # gọi hàm để hiển thị số lượng thông báo

    if request.user.is_authenticated:
        unread_count = count_unread_notifications(request.user)
    else:
        unread_count = 0

    # gọi hàm để hiển thị thông báo bình luận
    display_notification = display_notifications(request)
    # hiển thị thông báo hệ thống
    notifications = Notification.objects.all()

    return render(request, 'quantri/search_results.html', {
        'results': results,
        'query': query,
        'growing_regions': growing_regions,
        'locations_json': json.dumps(locations_json),
        'count': unread_count,
        'display_notification': display_notification,
        'notifications': notifications,

    })


# lọc bài viết theo vùng
def show_related_articles(request):
    selected_vung = request.GET.get('region_id')
    try:
        growing_region = GrowingRegion.objects.get(GrowingRegionID=selected_vung)
        name = growing_region.RegionName

        related_articles = Article.objects.filter(
            Q(FruitID__Location__GrowingRegion=selected_vung) & Q(IsApproved=True)
        ).order_by('-ArticleID')
    except GrowingRegion.DoesNotExist:
        name, related_articles = "", []

    growing_regions = get_growing_regions()

    # locations = Location.objects.filter(GrowingRegion=growing_region)
    locations_json = [
        {
            'fruit_name': article.FruitID.FruitName,
            'Name': article.FruitID.Location.Name,
            'FruitType': article.FruitID.Location.FruitType,
            'Latitude': decimal_to_str(article.FruitID.Location.Latitude),
            'Longitude': decimal_to_str(article.FruitID.Location.Longitude),
            'id_article': article.ArticleID,
        }
        for article in related_articles
    ]

    # gọi hàm để hiển thị số lượng thông báo
    if request.user.is_authenticated:
        unread_count = count_unread_notifications(request.user)
    else:
        unread_count = 0

    # gọi hàm để hiển thị thông báo bình luận
    display_notification = display_notifications(request)
    # hiển thị thông báo hệ thống
    notifications = Notification.objects.all()

    return render(request, 'quantri/related_articles.html', {
        'display_notification': display_notification,
        'name': name,
        'related_articles': related_articles,
        'growing_regions': growing_regions,
        'locations_json': json.dumps(locations_json),
        'count': unread_count,
        'notifications': notifications,
    })


# hàm đăng ký
def register(request):
    if request.method == 'POST':
        # Check if 'otp' is present in the request.POST dictionary
        if 'otp' in request.POST:
            user_otp = request.POST['otp']
            stored_otp = request.session.get('otp', None)

            # Lấy thời điểm khi OTP được tạo từ session
            # Lấy thời điểm khi OTP được tạo từ session
            otp_created_at_str = request.session.get('otp_created_at')
            otp_created_at = timezone.datetime.fromisoformat(otp_created_at_str)
            if (timezone.now() - otp_created_at) < timedelta(minutes=10):
                # Kiểm tra xem mã xác thực có khớp với mã đã lưu trong session không
                if user_otp == stored_otp:
                    # Đăng ký người dùng và đăng nhập
                    username = request.POST['username']
                    if User.objects.filter(username=username).exists():
                        return render(request, 'quantri/SignUpForm.html', {'messages': 'Tên người dùng đã tồn tại'})
                    password = request.POST['password1']
                    user = User(username=username)
                    user.set_password(password)

                    # Lấy giá trị từ ô nhập Email
                    user.email = request.POST['email']
                    user.save()
                    login(request, user)

                    # Xóa OTP khỏi session sau khi đăng ký
                    if 'otp' in request.session:
                        del request.session['otp']

                    return redirect('post:login')
                return render(request, 'quantri/SignUpForm.html', {'message': 'Mã otp không trùng khớp'})
            return render(request, 'quantri/SignUpForm.html', {'message': 'Mã OTP đã hết hạn.'})

        else:
            return render(request, 'quantri/SignUpForm.html', {'message': 'Mã otp không hợp lệ'})

    return render(request, 'quantri/SignUpForm.html')


def gmail_verification(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        dk_email_1 = email.find("@")
        dk_email_2 = email.find(".")

        if int(dk_email_1) > 0 and int(dk_email_2) > 0:
            check_user = User.objects.filter(email=email)

            if not check_user:
                try:
                    otp = str(random.randint(1000, 9999))

                    subject = 'Xác thực Gmail'
                    message = f'Mã xác thực của tài khoản NONGSANVIETNAM bạn là: {otp} Có hiệu lực trong vòng 10 phút'
                    from_email = 'DefaultDonotReply@gmail.com'
                    #Thay thế bằng địa chỉ email của bạn
                    recipient_list = [email]
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                    #Lưu thời điểm hiện tại khi OTP được tạo dưới dạng chuỗi ISO 8601
                    request.session['otp_created_at'] = timezone.now().isoformat()
                    request.session['otp'] = otp

                    #Truyền giá trị email và thông báo thành công vào template
                    return render(request, 'quantri/SignUpForm.html',
                                  {'email': email, 'message': 'Mã xác thực đã được gửi đến email của bạn.'})
                except Exception as e:
                    messages.error(request, f'Có lỗi xảy ra trong quá trình gửi email xác thực: {e}')
            else:
                messages.error(request, 'Gmail đã được đăng ký.')
        else:
            messages.error(request, 'Vui lòng nhập đúng định dạng .@')

    # Nếu có lỗi hoặc không phải phương thức GET, chuyển hướng về trang đăng ký
    return redirect('post:register')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('post:home')
        return render(request, 'quantri/login.html', {'message': 'Tên người dùng hoặc mật khẩu không đúng.'})
    return render(request, 'quantri/login.html')


def forgot_password(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email_or_username')
        user = User.objects.filter(email=email_or_username).first()

        if user:
            user_id = user.id
            return redirect('post:reset_password', user_id=user_id)
        else:
            messages.error(request, 'Không tìm thấy tài khoản với địa chỉ Email này.')

    return render(request, 'quantri/forgot_password.html')


def reset_password(request, user_id):
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Mật khẩu đã được đặt lại thành công. Hãy đăng nhập bằng mật khẩu mới của bạn.')
        return redirect('post:login')

    return render(request, 'quantri/reset_password.html', {'user': user})


def logout_view(request):
    logout(request)
    return redirect('post:home')


def upload_avatar(request):
    try:
        # Kiểm tra xem đã có avatar cho người dùng hiện tại chưa
        avatar, created = UserAvatar.objects.get_or_create(user=request.user)
    except UserAvatar.DoesNotExist:
        avatar = None

    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid():
            form.save()
            return redirect('post:home')
    else:
        form = AvatarUploadForm(instance=avatar)

    return render(request, 'quantri/upload_avatar.html', {'form': form, 'avatar': avatar, })


def weather(request):
    context = {}
    city_mapping = {
        "Tỉnh Thừa Thiên Huế": "Huế",
        "Hoà Bình": "Hòa Bình",
        "Hải Dương": "Hai Duong",
        "Tỉnh Lai Châu": "Lai Châu",
        "Tỉnh Hoà Bình": "Tỉnh Hòa Bình",
        "Tỉnh Nam Định": "Nam Định",
        "Tỉnh Bình Định": "Bình Định",
        "Tỉnh Bà Rịa - Vũng Tàu": "Vung Tau",
        "Hồ Chí Minh": "Ho Chi Minh",
        "Tỉnh Điện Biên": "Điện Biên Phủ",
        "Tỉnh Đắk Lắk": "Buôn Ma Thuột",
        "Tỉnh Đắk Nông": "Gia Nghĩa",
        "Tỉnh Lâm Đồng": "Đà Lạt",
        "Tỉnh Đồng Nai": "Biên Hòa",
        "Tỉnh Đồng Tháp": "Cao Lãnh",
        "Tỉnh Kiên Giang": "Rạch Giá",
        "Tỉnh Hậu Giang": "Hà Giang",

    }

    if request.method == 'POST':
        # Lấy tên thành phố từ form
        selected_city_name = request.POST.get('city')
        selected_city_name = selected_city_name.replace("Thành phố ", "")
        # print(f'selected_city_name: {selected_city_name}')

        if selected_city_name in city_mapping:
            selected_city_name = city_mapping[selected_city_name]
        # print(f'selected_city_name: {selected_city_name}')

    else:
        selected_city_name = "Hà Nội"

    api_key = 'f8f72aafea7018cb394ec15dfb353902'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={selected_city_name}&appid={api_key}'

    response = requests.get(url)
    data = response.json()

    daily_forecast = []
    if data['cod'] == '200':

        # Lấy thông tin thời tiết cho 7 ngày tiếp theo
        daily_forecast = data['list'][:35]

        # Chuyển đổi độ K thành độ C
        for forecast in daily_forecast:
            forecast['main']['temp_C'] = round(forecast['main']['temp'] - 273.15, 2)

    else:
        if data['cod'] == '404':
            context = {'error': 'Không tìm thấy tỉnh/thành phố.'}
        else:
            context = {'error': 'Không thể lấy dữ liệu thời tiết.'}

    # hiển thị danh sách các tỉnh
    # URL của API danh sách tỉnh thành
    api_url = 'https://provinces.open-api.vn/api/'
    response = requests.get(api_url)
    if response.status_code == 200:
        city_list = response.json()

    # gọi hàm để hiển thị thông báo
    display_notification = display_notifications(request)

    # gọi hàm để hiển thị số lượng thông báo
    if request.user.is_authenticated:
        unread_count = count_unread_notifications(request.user)
    else:
        unread_count = 0

    # Vùng
    growing_regions = get_growing_regions()

    return render(request, 'quantri/weather.html', {
        'display_notification': display_notification,
        'count': unread_count,
        'city_list': city_list,
        'selected_city_name': selected_city_name,
        'daily_forecast': daily_forecast,
        'growing_regions': growing_regions,
        **context,  # Truyền biến context vào template

    })


@login_required(login_url='/login')
def create_article(request):
    # lấy danh sách các vùng trồng
    growing_regions = get_growing_regions()

    error_message = None
    if request.method == 'POST':
        print('111')
        # Lấy dữ liệu từ biểu mẫu HTML
        # Lấy user_id từ người dùng hiện tại
        user_id = request.user.id

        # Kiểm tra xem người dùng có phải là quản trị viên không
        is_admin = request.user.is_staff

        titleArtice = request.POST['title']
        contentArtice = request.POST['content']
        ImageArtice = request.FILES.get('ImageArtice')

        # Lấy ID vùng trồng từ request.POST
        selected_region_id = request.POST['selected_region']

        # Sử dụng ID để lấy thể hiện của GrowingRegion
        if selected_region_id:
            selected_region = GrowingRegion.objects.get(GrowingRegionID=selected_region_id)

        # region_name = request.POST['RegionName']
        # region_description = request.POST['RegionDescription']
        # region_area = request.POST['RegionArea']
        # region_main_product = request.POST['RegionMainProduct']

        latitude = request.POST['Latitude']
        longitude = request.POST['Longitude']
        location_name = request.POST['LocationName']
        fruitType = request.POST['FruitType']

        fruit_name = request.POST['FruitName']
        fruit_description = request.POST['FruitDescription']
        fruit_planting_time = request.POST['PlantingTime']
        fruit_harvest_time = request.POST['HarvestTime']
        quantity = request.POST['quantity']

        # new_images = request.FILES.getlist('image')
        # imageName = request.POST['ImageName']
        # description = request.POST['ImageDescription']

        new_videos = request.FILES.getlist('video')
        tile_video = request.POST['Title_video']
        print('222')

        # Xử lý dữ liệu định dạng ngày/tháng/năm
        try:
            fruit_planting_time = datetime.strptime(fruit_planting_time, '%Y-%m-%d').date()
            fruit_harvest_time = datetime.strptime(fruit_harvest_time, '%Y-%m-%d').date()
        except ValueError:
            error_message = "Ngày không hợp lệ. Sử dụng định dạng YYYY-MM-DD."

        if not error_message:
            try:
                print('333')
                # Tạo bản ghi cho GrowingRegion
                # region = GrowingRegion(RegionName=region_name, Description=region_description, Area=region_area, MainProduct=region_main_product)
                # region.save()

                # Tạo bản ghi cho Location
                location = Location(Latitude=latitude, Longitude=longitude, Name=location_name, FruitType=fruitType,
                                    GrowingRegion=selected_region)
                location.save()
                print('444')
                # Tạo bản ghi cho Fruit
                fruit = Fruit(FruitName=fruit_name, Description=fruit_description, PlantingTime=fruit_planting_time,
                              HarvestTime=fruit_harvest_time, Quantity=quantity, Location=location)
                fruit.save()
                print('555')

                # Tạo bản ghi nội dung trái cây
                # Lấy số lượng trường mẫu
                num_forms = int(request.POST.get('num_forms', 0))

                # Lưu dữ liệu từ các trường mẫu vào model FruitContent
                for i in range(1, num_forms + 1):
                    print('666')
                    title = request.POST.get(f'FruitTile{i}')
                    content = request.POST.get(f'FruitConten{i}')
                    image = request.FILES.get(f'FruitName{i}')
                    if title or content or image:
                        FruitContent.objects.create(fruit=fruit, title=title, content=content, image=image)

                if new_videos:
                    if len(new_videos) <= 3:
                        for video in new_videos:
                            video_obj = Video(Title=tile_video, VideoFile=video, FruitID=fruit)
                            video_obj.save()
                    else:
                        messages.error(request, "Chọn tối đa 3 video.")
                        return render(request, 'quantri/create_article.html', {'message': 'Mã OTP đã hết hạn.'})
                print('777')
                # Tạo bài viết
                article = Article(Title=titleArtice, Image=ImageArtice, Content=contentArtice, FruitID=fruit,
                                  User_id=user_id)
                print('article', article)
                if is_admin:
                    print('start')
                    article.IsApproved = True
                article.save()
                print('888')
                # Chuyển hướng đến trang danh sách bài viết sau khi đăng
                return redirect('post:home')

            except ValidationError as e:
                error_message = "Có lỗi xảy ra: " + str(e)
    print('999print''')
    return render(request, 'quantri/create_article.html',
                  {'error_message': error_message, 'growing_regions': growing_regions})


def get_user_articles(request, user_id_param):
    try:
        # Sử dụng truy vấn để lấy danh sách các bài viết của một người dùng
        user = User.objects.get(pk=user_id_param)
        user_articles = Article.objects.filter(User_id=user_id_param).order_by('-ArticleID')

        try:
            user_avatar = UserAvatar.objects.get(user=user)
        except UserAvatar.DoesNotExist:
            user_avatar = None

        # gọi hàm để hiển thị thông báo
        display_notification = display_notifications(request)

        # gọi hàm để hiển thị số lượng thông báo
        count = count_unread_notifications(request.user)

        # vùng
        growing_regions = get_growing_regions()
        # Trả về danh sách các bài viết
        return render(request, 'quantri/user_articles.html', {'user_articles': user_articles,
                                                              'user': user,
                                                              'user_avatar': user_avatar,
                                                              'display_notification': display_notification,
                                                              'count': count,
                                                              'growing_regions': growing_regions

                                                              })
    except User.DoesNotExist:
        # Xử lý trường hợp người dùng không tồn tại
        return HttpResponse("Người dùng không tồn tại", status=404)


def delete_article(request, article_id):
    # Tìm bài viết cần xóa hoặc trả về 404 nếu không tìm thấy
    article = get_object_or_404(Article, ArticleID=article_id)
    user_articles = article.User.id
    fruit = article.FruitID
    fruitConten = FruitContent.objects.filter(fruit=fruit)

    videos = Video.objects.filter(FruitID=article.FruitID_id)
    Location = fruit.Location

    Location.delete()
    videos.delete()
    fruitConten.delete()
    fruit.delete()
    article.delete()

    return redirect('post:get_user_articles', user_id_param=user_articles)


# def delete_img(request, img_id):
#     try:
#         img = Image.objects.get(ImageID=img_id)
#         img.delete()
#         return HttpResponse('xóa ảnh thành công')
#     except:
#         return HttpResponse('xóa ảnh không  thành công')

# def delete_video(request, video_id):
#     try:
#         video = Video.objects.get(id=video_id)
#         video.delete()
#         return HttpResponse('xóa video thành công')
#     except:
#         return HttpResponse('xóa video không  thành công')

# def editfruitConten(request, id):

#     if request.method == 'GET':
#         fruit_conte = get_object_or_404(FruitContent, id=id)
#         title = request.GET.get('titlefruitConten')
#         content = request.GET.get('contentfruitConten')

#         fruit_conte.title = title
#         fruit_conte.content = content
#         fruit_conte.save()

#         return HttpResponse({'status': 'success'})
#     else:

#         return HttpResponse('lỗiiii')


def edit_article(request, article_id):
    # Lấy bài viết cần sửa hoặc trả về 404 nếu không tìm thấy
    article = get_object_or_404(Article, ArticleID=article_id)
    fruit = article.FruitID
    fruitConten = FruitContent.objects.filter(fruit=fruit)
    videos = Video.objects.filter(FruitID=article.FruitID_id)
    Location = fruit.Location
    growing_region = Location.GrowingRegion
    is_admin = request.user.is_staff  # Kiểm tra xem người dùng có phải là quản trị viên không

    if request.method == 'POST':
        # Kiểm tra xem người dùng có quyền sửa bài viết không
        if request.user.id == article.User_id or request.user.is_staff:
            # Cập nhật các trường vùng
            growing_region.RegionName = request.POST.get('RegionName', growing_region.RegionName)
            growing_region.Description = request.POST.get('RegionDescription', growing_region.Description)
            growing_region.Area = request.POST.get('RegionArea', growing_region.Area)
            growing_region.MainProduct = request.POST.get('RegionMainProduct', growing_region.MainProduct)
            growing_region.save()

            # Cập nhật các trường địa điểm trồng
            Location.Latitude = request.POST.get('Latitude', Location.Latitude)
            Location.Longitude = request.POST.get('Longitude', Location.Longitude)
            Location.Name = request.POST.get('LocationName', Location.Name)
            Location.save()

            # Cập nhật các trường về trái cây
            fruit.FruitName = request.POST.get('FruitName', fruit.FruitName)
            fruit.Description = request.POST.get('FruitDescription', fruit.Description)
            fruit.PlantingTime = request.POST.get('PlantingTime', fruit.PlantingTime)
            fruit.HarvestTime = request.POST.get('HarvestTime', fruit.HarvestTime)
            fruit.Quantity = request.POST.get('quantity', fruit.Quantity)
            fruit.save()

            # new_images = request.FILES.getlist('image')
            # imageName = request.POST['ImageName']
            # description = request.POST['ImageDescription']
            #  # Tạo bản ghi cho Image
            # for image in new_images:
            #     image_obj = Image(ImageName=imageName, Description=description, ImageURL=image, FruitID=fruit)
            #     image_obj.save()

            # # Cập nhật các hình ảnh
            # for image in images:
            #     image_id = image.ImageID
            #     image_name = request.POST.get('ImageName_' + str(image_id), image.ImageName)
            #     image_description = request.POST.get('ImageDescription_' + str(image_id), image.Description)
            #     image.ImageName = image_name
            #     image.Description = image_description
            #     image.save()

            # Cập nhật các video
            new_videos = request.FILES.getlist('video')
            tile_video = request.POST['Title_video']
            # Tạo bản ghi cho VIDEO
            for video in new_videos:
                video_obj = Video(Title=tile_video, VideoFile=video, FruitID=fruit)
                video_obj.save()
            # for video in videos:
            #     video_id = video.id
            #     video_name = request.POST.get('Title_video_' + str(video_id),  video.Title)
            #     video.Title = video_name
            #     video.save()

            article.Title = request.POST.get('title', article.Title)
            article.Content = request.POST.get('content', article.Content)
            article.Image = request.FILES.get('img', article.Image)

            if is_admin:
                article.IsApproved = True
            else:
                article.IsApproved = False
            article.save()  # Lưu thay đổi vào cơ sở dữ liệu

            num_forms = int(request.POST.get('num_forms', 0))
            # Lưu dữ liệu từ các trường mẫu vào model FruitContent
            for i in range(1, num_forms + 1):
                fruitid = request.POST.get(f'id{i}')
                title = request.POST.get(f'titlefruitConten{i}')
                content = request.POST.get(f'contentfruitConten{i}')
                image = request.FILES.get(f'imgfruitConten{i}')
                print('imgggg', image)

                fruit_conte = FruitContent.objects.get(id=fruitid)
                fruit_conte.title = title
                fruit_conte.content = content

                if image:
                    fruit_conte.image = image

                fruit_conte.save()

            return redirect('post:get_user_articles', user_id_param=request.user.id)
            # return redirect('post:home')

    return render(request, 'quantri/edit_article.html', {
        'article': article,
        'fruit': fruit,
        'fruitConten': fruitConten,
        'videos': videos,
        'Location': Location,
        'growing_region': growing_region,
    })


# Xem thông báo (Chi Tiết Bài Viết)
def article_notifications(request, article_id, feedback_id):
    try:
        article = get_object_or_404(Article, ArticleID=article_id)
        fruits = article.FruitID
        fruit_conte = FruitContent.objects.filter(fruit=fruits)

        # images = Image.objects.filter(FruitID=article.FruitID_id)
        user_article = User.objects.get(id=article.User.id)
        try:
            user_avt = UserAvatar.objects.get(user=user_article)
        except UserAvatar.DoesNotExist:
            user_avt = None

        videos = Video.objects.filter(FruitID=article.FruitID_id)
        Location = fruits.Location
        growing_region = Location.GrowingRegion

        # Lấy tất cả các đối tượng Location của GrowingRegion
        all_locations = growing_region.location_set.all()
        all_locations_info = []
        for location in all_locations:
            # Sử dụng all() để lấy tất cả các đối tượng Fruit liên quan
            fruits_info = location.fruits.all()
            for fruit in fruits_info:
                fruit_info = {
                    'fruit_name': fruit.FruitName,
                    'location_name': location.Name,
                    'latitude': float(location.Latitude),
                    'longitude': float(location.Longitude),
                    'FruitType': location.FruitType,
                }
                all_locations_info.append(fruit_info)

        location_names = [info['location_name'] for info in all_locations_info]

        feedbacks = Feedback.objects.filter(Article=article)

        feedback_form = FeedbackForm()
        reply_form = FeedbackForm()

        user_avatars = {}

        for feedback in feedbacks:
            # Lấy thông tin người dùng từ trường User của Feedback
            user = feedback.User

            try:

                user_avatar = UserAvatar.objects.get(user=user)
                if user_avatar.avatar:
                    user_avatars[user.id] = user_avatar.avatar.url
                else:
                    user_avatars[user.id] = None
            except UserAvatar.DoesNotExist:
                user_avatars[user.id] = None

        growing_regions = get_growing_regions()

        # Chuyển đổi giá trị Decimal thành kiểu float hoặc str trước khi đưa vào JSON
        latitude_value = float(Location.Latitude)
        longitude_value = float(Location.Longitude)

        # Tạo một từ điển chứa thông tin về Location
        location_info = {
            'name': Location.Name,
            'latitude': latitude_value,
            'longitude': longitude_value,
            'fruit_name': fruit.FruitName,
            'FruitType': Location.FruitType,

        }

        # Chuyển từ điển thành chuỗi JSON
        location_json = json.dumps(location_info)
        user = request.user  # Lấy thông tin người dùng hiện tại

        # gọi hàm để hiển thị số lượng thông báo
        if request.user.is_authenticated:
            unread_count = count_unread_notifications(request.user)
        else:
            unread_count = 0
        # gọi hàm để hiển thị thông báo
        display_notification = display_notifications(request)

        # đổi trạng thái là đã đọc thông báo
        notifications = Feedback.objects.filter(FeedbackID=feedback_id)
        for feedback in notifications:
            feedback.is_read = True
            feedback.save()  # Lưu lại trạng thái đã thay đổi

        # bài viết liên quan
        print(',,,,', fruit.FruitID)
        related_articles = Article.objects.filter(FruitID=fruits.FruitID).exclude(ArticleID=article_id)[:5]


    except Article.DoesNotExist:
        return render(request, 'quantri/custom_404.html')

    return render(request, 'quantri/article_list.html', {
        'article': article,
        # 'images': images,
        'growing_region': growing_region,
        'feedbacks': feedbacks,
        'feedback_form': feedback_form,
        'reply_form': reply_form,
        'growing_regions': growing_regions,
        'user_avatars': user_avatars,
        'fruit': fruits,  # Truyền user_avatars vào context để truyền đến template
        'Location': Location,
        'location_json': location_json,
        'user': user,
        'videos': videos,
        'count': unread_count,
        'display_notification': display_notification,
        'related_articles': related_articles,
        'fruit_conte': fruit_conte,
        'user_article': user_article,
        'user_avt': user_avt,
        'all_locations': all_locations,
        'all_locations_info': json.dumps(all_locations_info),
        'location_names': location_names,

    })


def update_account(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_avatar = request.FILES.get('avatar')
        new_password = request.POST.get('password')
        story = request.POST.get('story')
        fb = request.POST.get('fb')
        zalo = request.POST.get('zalo')
        phone = request.POST.get('phone')

        user = request.user
        user.username = new_username
        user.email = new_email
        if new_password:
            user.password = make_password(new_password)
        user.save()

        user_avatar1, created = UserAvatar.objects.get_or_create(user=user)
        user_avatar1.story = story
        user_avatar1.fb = fb
        user_avatar1.zalo = zalo
        user_avatar1.phone = phone
        user_avatar1.save()

        if new_avatar:
            user_avatar, created = UserAvatar.objects.get_or_create(user=user)
            user_avatar.avatar = new_avatar
            user_avatar.save()

        # Đăng nhập lại người dùng với thông tin đã được cập nhật
        updated_user = authenticate(username=new_username, password=new_password)
        if updated_user:
            login(request, updated_user)

        return redirect('post:get_user_articles', user_id_param=user.id)

    return render(request, 'quantri/update_account.html')


def create_growing_region(request):
    if request.method == 'POST':
        RegionName = request.POST.get('RegionName')
        Description = request.POST.get('Description')
        Area = request.POST.get('Area')
        MainProduct = request.POST.get('MainProduct')

        # Kiểm tra xem vùng trồng có tên tương tự đã tồn tại hay không (không phân biệt chữ hoa chữ thường)
        if GrowingRegion.objects.filter(RegionName__iexact=RegionName).exists():
            # Hiển thị thông báo nếu vùng trồng có tên tương tự đã tồn tại
            message = "Vùng trồng với tên đã tồn tại !!!."
            return render(request, 'quantri/create_growing_region.html', {'message': message})

        # Nếu vùng trồng chưa tồn tại, tạo mới
        growing_region = GrowingRegion(RegionName=RegionName, Description=Description, Area=Area,
                                       MainProduct=MainProduct)
        growing_region.save()

        return redirect('post:create_article')

    return render(request, 'quantri/create_growing_region.html')


# mùa vụ
def detail_seasonPlans(request, id):
    season_plan = get_object_or_404(SeasonPlan, SeasonPlanID=id)

    # Tìm kế hoạch gieo trồng với mùa vụ
    planting_plans = PlantingPlan.objects.filter(season=season_plan)

    # Lấy danh sách các plan_id từ planting_plans
    plan_ids = [plan.plan_id for plan in planting_plans]

    # Lịch trình chăm sóc liên quan đến các plan_id
    care_schedule = CareSchedule.objects.filter(plan__in=plan_ids)

    season_plans = SeasonPlan.objects.all()
    context = {
        'season_plans': season_plans,
        'season_plan': season_plan,
        'planting_plans': planting_plans,
        'careSchedule': care_schedule,
    }

    return render(request, 'quantri/detail_seasonPlans.html', context)


# ==============BÁO, SẢN VẬT ĐỊA PHƯƠNG===============
def item(request, id):
    item = Items.objects.get(Items_id=id)
    display_notification = display_notifications(request)
    items = Items.objects.all().exclude(Items_id=id)[:5]

    # gọi hàm để hiển thị số lượng thông báo
    if request.user.is_authenticated:
        unread_count = count_unread_notifications(request.user)
    else:
        unread_count = 0
    # Vùng
    growing_regions = get_growing_regions()

    return render(request, 'quantri/items.html', {
        'item': item,
        'display_notification': display_notification,
        'count': unread_count,
        'growing_regions': growing_regions,
        'items': items
    })


def item_list(request):
    items = Items.objects.all()

    # gọi hàm để hiển thị thông báo
    display_notification = display_notifications(request)

    # gọi hàm để hiển thị số lượng thông báo
    if request.user.is_authenticated:
        unread_count = count_unread_notifications(request.user)
    else:
        unread_count = 0

    # Vùng
    growing_regions = get_growing_regions()
    return render(request, 'quantri/items_list.html', {
        'items': items,
        'display_notification': display_notification,
        'count': unread_count,
        'growing_regions': growing_regions,
    })


def newspaper(request, id):
    newspaper = Newspaper.objects.get(Newspaper_id=id)
    newspapers = Newspaper.objects.all().exclude(Newspaper_id=id)[:5]
    # Gọi hàm để hiển thị thông báo
    display_notification = display_notifications(request)

    # Gọi hàm để hiển thị số lượng thông báo
    if request.user.is_authenticated:
        unread_count = count_unread_notifications(request.user)
    else:
        unread_count = 0

    # Vùng
    growing_regions = get_growing_regions()

    return render(request, 'quantri/newspaper.html', {
        'newspaper': newspaper,
        'newspapers': newspapers,
        'display_notification': display_notification,
        'count': unread_count,
        'growing_regions': growing_regions,

    })


def newspaper_list(request):
    newspapers = Newspaper.objects.all()
    display_notification = display_notifications(request)

    # Gọi hàm để hiển thị số lượng thông báo
    if request.user.is_authenticated:
        unread_count = count_unread_notifications(request.user)
    else:
        unread_count = 0

    # Vùng
    growing_regions = get_growing_regions()
    return render(request, 'quantri/newspaper_list.html', {
        'newspapers': newspapers,
        'display_notification': display_notification,
        'count': unread_count,
        'growing_regions': growing_regions,
    })


def videos(request, id):
    video = Videos.objects.get(Video_id=id)
    display_notification = display_notifications(request)

    # gọi hàm để hiển thị số lượng thông báo
    videos = Videos.objects.all().exclude(Video_id=id)[:5]
    if request.user.is_authenticated:
        unread_count = count_unread_notifications(request.user)
    else:
        unread_count = 0

    # Vùng
    growing_regions = get_growing_regions()
    return render(request, 'quantri/videos.html', {
        'video': video,
        'display_notification': display_notification,
        'count': unread_count,
        'growing_regions': growing_regions,
        'videos': videos
    })


def videos_list(request):
    videos = Videos.objects.all()
    display_notification = display_notifications(request)

    # gọi hàm để hiển thị số lượng thông báo
    if request.user.is_authenticated:
        unread_count = count_unread_notifications(request.user)
    else:
        unread_count = 0

    # Vùng
    growing_regions = get_growing_regions()
    return render(request, 'quantri/videos_list.html', {
        'videos': videos,
        'display_notification': display_notification,
        'count': unread_count,
        'growing_regions': growing_regions,
    })


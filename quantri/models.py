from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


# # Create your models here.
class GrowingRegion(models.Model):
    class Meta:
        verbose_name_plural = "Vùng "

    GrowingRegionID = models.AutoField(primary_key=True)
    RegionName = models.CharField('Tên vùng', max_length=255)
    Description = models.TextField('Mô tả')
    Area = models.DecimalField('Diện tích', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    MainProduct = models.CharField('Trồng trái cây chính', max_length=255)

    def __str__(self):
        return self.RegionName


class Location(models.Model):
    class Meta:
        verbose_name_plural = "Địa Điểm "

    LocationID = models.AutoField(primary_key=True)
    Latitude = models.DecimalField('Kinh tuyến', max_digits=20, decimal_places=15)
    Longitude = models.DecimalField('Vĩ tuyến', max_digits=20, decimal_places=15)
    Name = models.CharField('Tên địa điểm ', max_length=255)
    GrowingRegion = models.ForeignKey(GrowingRegion, on_delete=models.CASCADE,
                                      verbose_name='Vùng trồng')  # Liên kết với vùng trồng
    FruitType = [
        ('ngan-ngay', 'ngan-ngay'),
        ('trung-ngay', 'trung-ngay'),
        ('dai-ngay', 'dai-ngay'),

    ]
    FruitType = models.CharField('loại cây trồng', max_length=20, choices=FruitType)

    def __str__(self):
        return self.Name


class Fruit(models.Model):
    class Meta:
        verbose_name_plural = "Trái Cây"

    FruitID = models.AutoField(primary_key=True)
    FruitName = models.CharField('Tên ', max_length=255)
    Description = models.TextField('Mô tả')
    PlantingTime = models.DateField('Thời gian trồng')
    HarvestTime = models.DateField('Thời gian thu hoạch')
    Quantity = models.IntegerField('diện tích (m2)')  # Thêm trường số lượng
    Location = models.ForeignKey(Location, related_name='fruits', on_delete=models.CASCADE,
                                 verbose_name='Địa điểm trồng')  # Trường ngoại khóa đến Location

    def clean(self):
        if self.PlantingTime >= self.HarvestTime:
            raise ValidationError("Thời gian trồng phải trước thời gian thu hoạch !!!")
        if self.Quantity <= 0:
            raise ValidationError(" Bạn vui lòng nhập số lượng lớn hơn 0 !!!")

    def __str__(self):
        return self.FruitName


class FruitContent(models.Model):
    class Meta:
        verbose_name_plural = "Nội dung trái cây"

    fruit = models.ForeignKey('Fruit', on_delete=models.CASCADE, related_name='contents', verbose_name='Trái cây')
    title = models.CharField('Tiêu đề', max_length=255)
    content = models.TextField('Nội dung')
    image = models.ImageField('Hình ảnh', upload_to='fruit_images/', null=True)

    def __str__(self):
        return f"{self.fruit.FruitName} - {self.title}"


# class Image(models.Model):
#     class Meta:
#         verbose_name_plural = "Hình Ảnh"
#     ImageID = models.AutoField(primary_key=True)
#     ImageName = models.TextField('Tên',max_length=20)
#     Description = models.TextField('Mô tả')
#     ImageURL = models.FileField(upload_to='images/')
#     FruitID = models.ForeignKey(Fruit, on_delete=models.CASCADE,verbose_name='Thuộc trái cây')

#     def __str__(self):
#         return self.ImageName

class Video(models.Model):
    class Meta:
        verbose_name_plural = "Video trái cây"

    Title = models.CharField('Tiêu đề', max_length=200)
    Date = models.DateField(auto_now_add=True)
    VideoFile = models.FileField(upload_to='videos/')
    FruitID = models.ForeignKey(Fruit, on_delete=models.CASCADE, verbose_name='Thuộc trái cây')

    def __str__(self):
        return self.Title


class Article(models.Model):
    class Meta:
        verbose_name_plural = "Bài Viết"

    ArticleID = models.AutoField(primary_key=True)
    Title = models.CharField('Tiêu đề', max_length=255)
    Content = models.TextField('Nội dung')
    PostingDate = models.DateField('ngày đăng', auto_now_add=True)
    FruitID = models.ForeignKey(Fruit, related_name='article', on_delete=models.CASCADE, verbose_name='Thuộc trái cây')
    IsApproved = models.BooleanField('Duyệt', default=False)
    User = models.ForeignKey(User, on_delete=models.CASCADE)  # Liên kết với người dùng
    Image = models.ImageField(upload_to='article_images/', blank=True, null=True, verbose_name='Hình ảnh')

    def __str__(self):
        return self.Title


class Feedback(models.Model):
    class Meta:
        verbose_name_plural = "Bình Luận"

    FeedbackID = models.AutoField(primary_key=True)
    Content = models.TextField('nội dung')
    ResponseDate = models.DateTimeField('Ngày đăng', auto_now_add=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='feedbacks', verbose_name='Bài viết')
    ParentFeedback = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='responses', verbose_name='Bình luận cha')

    # is_notification = models.BooleanField(default=False)
    notification_message = models.TextField(blank=True, null=True, verbose_name='Nội dung thông báo')
    is_read = models.BooleanField(default=False,
                                  verbose_name='Trạng thái thông báo')  # Trường mới để theo dõi trạng thái đã đọc hay chưa

    def __str__(self):
        return self.Content


class UserAvatar(models.Model):
    class Meta:
        verbose_name_plural = "Thông tin chi tiết User"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True)
    story = models.TextField('tiểu sử', null=True)
    fb = models.TextField(null=True, blank=True)
    zalo = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    class Meta:
        verbose_name_plural = "Thông Báo"

    NotificationID = models.AutoField(primary_key=True)
    Title = models.CharField('Tiêu đề', max_length=255)
    Content1 = models.TextField('Nội dung 1', blank=True, null=True)
    Content2 = models.TextField('Nội dung 2', blank=True, null=True)
    Content3 = models.TextField('Nội dung 3', blank=True, null=True)
    Content4 = models.TextField('Nội dung 4', blank=True, null=True)
    Content5 = models.TextField('Nội dung 5', blank=True, null=True)
    Image1 = models.ImageField(upload_to='notification_images/', blank=True, null=True, verbose_name='Hình ảnh 1')
    Image2 = models.ImageField(upload_to='notification_images/', blank=True, null=True, verbose_name='Hình ảnh 2')
    Image3 = models.ImageField(upload_to='notification_images/', blank=True, null=True, verbose_name='Hình ảnh 3')
    Image4 = models.ImageField(upload_to='notification_images/', blank=True, null=True, verbose_name='Hình ảnh 4')
    Image5 = models.ImageField(upload_to='notification_images/', blank=True, null=True, verbose_name='Hình ảnh 5')
    PostingDate = models.DateField('Ngày đăng', auto_now_add=True)

    def __str__(self):
        return self.Title


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField('Nội dung chat')
    response = models.TextField('Nội dung phản hồi')
    created_at = models.DateTimeField('Thời gian', auto_now_add=True)

    def __str__(self):
        return self.message


# ================ KẾ HOẠCH MÙA VỤ ================

class SeasonPlan(models.Model):
    class Meta:
        verbose_name_plural = "Mùa Vụ"

    SeasonPlanID = models.AutoField(primary_key=True)
    PlanName = models.CharField('Tên', max_length=255)
    Description = models.TextField('Mô tả')
    StartDate = models.DateField('Thời gian bắt đầu')
    EndDate = models.DateField('Thời gian kết thúc')

    def clean(self):
        if self.StartDate >= self.EndDate:
            raise ValidationError("Thời gian bắt đầu phải trước thời gian kết thúc !!!")

    def __str__(self):
        return self.PlanName


class CropType(models.Model):
    class Meta:
        verbose_name_plural = "Loại Cây Trồng"

    crop_type_id = models.AutoField(primary_key=True)
    crop_type_name = models.CharField('Tên', max_length=255)

    def __str__(self):
        return self.crop_type_name


class PlantingPlan(models.Model):
    class Meta:
        verbose_name_plural = "Kế Hoạch Gieo Trồng"

    plan_id = models.AutoField(primary_key=True)
    season = models.ForeignKey(SeasonPlan, on_delete=models.CASCADE, verbose_name="Mùa vụ")
    crop_type = models.ForeignKey(CropType, on_delete=models.CASCADE, verbose_name="Cây trồng")

    # start_date = models.DateField(verbose_name="Ngày bắt đầu")
    # end_date = models.DateField(verbose_name="Ngày kết thúc")

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Thời gian bắt đầu phải trước thời gian kết thúc !!!")

    def __str__(self):
        return f"{self.season.PlanName} - {self.crop_type.crop_type_name}"


class CareSchedule(models.Model):
    class Meta:
        verbose_name_plural = "Lịch Trình Chăm Sóc"

    schedule_id = models.AutoField(primary_key=True)
    plan = models.ForeignKey(PlantingPlan, on_delete=models.CASCADE, verbose_name="Tên kế hoạch")
    care_date = models.TextField(verbose_name="Thời gian")
    fertilizing = models.CharField(max_length=255, verbose_name="Phân bón")
    disease_control = models.CharField(max_length=255, verbose_name="Kiểm soát bệnh")
    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    def __str__(self):
        return f"{self.plan} - {self.care_date}"


# ==================GIÁ NÔNG SẢN======================
class ProductPrice(models.Model):
    class Meta:
        verbose_name_plural = "Giá nông sản"

    ProductPrice_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    tphcm_price = models.TextField()
    hanoi_price = models.TextField()
    danang_price = models.TextField()


    def __str__(self):
        return self.name


# =================BÁO, SẢN VẬY ĐỊA PHƯƠNG=====================
class Items(models.Model):
    class Meta:
        verbose_name_plural = "Sản Vật"

    Items_id = models.AutoField(primary_key=True)
    Title = models.CharField('Tiêu đề', blank=True, null=True, max_length=255)
    Title1 = models.CharField('Tiêu đề 1', blank=True, null=True, max_length=255)
    Content1 = models.TextField('Nội dung 1', blank=True, null=True)
    Content2 = models.TextField('Nội dung 2', blank=True, null=True)
    Content3 = models.TextField('Nội dung 3', blank=True, null=True)
    Content4 = models.TextField('Nội dung 4', blank=True, null=True)
    Content5 = models.TextField('Nội dung 5', blank=True, null=True)
    Content6 = models.TextField('Nội dung 6', blank=True, null=True)
    Image1 = models.ImageField(upload_to='items_images/', blank=True, null=True, verbose_name='Hình ảnh 1')
    Image2 = models.ImageField(upload_to='items_images/', blank=True, null=True, verbose_name='Hình ảnh 2')
    Image3 = models.ImageField(upload_to='items_images/', blank=True, null=True, verbose_name='Hình ảnh 3')
    Image4 = models.ImageField(upload_to='items_images/', blank=True, null=True, verbose_name='Hình ảnh 4')
    Image5 = models.ImageField(upload_to='items_images/', blank=True, null=True, verbose_name='Hình ảnh 5')
    Image6 = models.ImageField(upload_to='items_images/', blank=True, null=True, verbose_name='Hình ảnh 6')
    PostingDate = models.DateField('Ngày đăng', auto_now_add=True)

    def __str__(self):
        return self.Title


class Newspaper(models.Model):
    class Meta:
        verbose_name_plural = "Báo Điện Tử"

    Newspaper_id = models.AutoField(primary_key=True)
    Title = models.CharField('Tiêu đề', blank=True, null=True, max_length=255)
    Title1 = models.CharField('Tiêu đề 1', blank=True, null=True, max_length=255)
    Content1 = models.TextField('Nội dung 1', blank=True, null=True)
    Content2 = models.TextField('Nội dung 2', blank=True, null=True)
    Content3 = models.TextField('Nội dung 3', blank=True, null=True)
    Content4 = models.TextField('Nội dung 4', blank=True, null=True)
    Content5 = models.TextField('Nội dung 5', blank=True, null=True)
    Image1 = models.ImageField(upload_to='newspapers_images/', blank=True, null=True, verbose_name='Hình ảnh 1')
    Image2 = models.ImageField(upload_to='newspapers_images/', blank=True, null=True, verbose_name='Hình ảnh 2')
    Image3 = models.ImageField(upload_to='newspapers_images/', blank=True, null=True, verbose_name='Hình ảnh 3')
    Image4 = models.ImageField(upload_to='newspapers_images/', blank=True, null=True, verbose_name='Hình ảnh 4')
    Image5 = models.ImageField(upload_to='newspapers_images/', blank=True, null=True, verbose_name='Hình ảnh 5')
    PostingDate = models.DateField('Ngày đăng', auto_now_add=True)

    def __str__(self):
        return self.Title


class Videos(models.Model):
    class Meta:
        verbose_name_plural = "video bài viết"

    Video_id = models.AutoField(primary_key=True)
    Title = models.CharField('Tiêu đề', blank=True, null=True, max_length=255)
    Title_phu = models.TextField('Nội dung', blank=True, null=True, max_length=255)
    VideoFile = models.FileField(upload_to='videos/')
    PostingDate = models.DateField('Ngày đăng', auto_now_add=True)
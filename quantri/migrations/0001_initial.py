import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CropType',
            fields=[
                ('crop_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('crop_type_name', models.CharField(max_length=255, verbose_name='Tên')),
            ],
            options={
                'verbose_name_plural': 'Loại Cây Trồng',
            },
        ),
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('FruitID', models.AutoField(primary_key=True, serialize=False)),
                ('FruitName', models.CharField(max_length=255, verbose_name='Tên ')),
                ('Description', models.TextField(verbose_name='Mô tả')),
                ('PlantingTime', models.DateField(verbose_name='Thời gian trồng')),
                ('HarvestTime', models.DateField(verbose_name='Thời gian thu hoạch')),
                ('Quantity', models.IntegerField(verbose_name='diện tích (m2)')),
            ],
            options={
                'verbose_name_plural': 'Trái Cây',
            },
        ),
        migrations.CreateModel(
            name='GrowingRegion',
            fields=[
                ('GrowingRegionID', models.AutoField(primary_key=True, serialize=False)),
                ('RegionName', models.CharField(max_length=255, verbose_name='Tên vùng')),
                ('Description', models.TextField(verbose_name='Mô tả')),
                ('Area', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Diện tích')),
                ('MainProduct', models.CharField(max_length=255, verbose_name='Trồng trái cây chính')),
            ],
            options={
                'verbose_name_plural': 'Vùng ',
            },
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('Items_id', models.AutoField(primary_key=True, serialize=False)),
                ('Title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tiêu đề')),
                ('Title1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tiêu đề 1')),
                ('Content1', models.TextField(blank=True, null=True, verbose_name='Nội dung 1')),
                ('Content2', models.TextField(blank=True, null=True, verbose_name='Nội dung 2')),
                ('Content3', models.TextField(blank=True, null=True, verbose_name='Nội dung 3')),
                ('Content4', models.TextField(blank=True, null=True, verbose_name='Nội dung 4')),
                ('Content5', models.TextField(blank=True, null=True, verbose_name='Nội dung 5')),
                ('Content6', models.TextField(blank=True, null=True, verbose_name='Nội dung 6')),
                ('Image1', models.ImageField(blank=True, null=True, upload_to='items_images/', verbose_name='Hình ảnh 1')),
                ('Image2', models.ImageField(blank=True, null=True, upload_to='items_images/', verbose_name='Hình ảnh 2')),
                ('Image3', models.ImageField(blank=True, null=True, upload_to='items_images/', verbose_name='Hình ảnh 3')),
                ('Image4', models.ImageField(blank=True, null=True, upload_to='items_images/', verbose_name='Hình ảnh 4')),
                ('Image5', models.ImageField(blank=True, null=True, upload_to='items_images/', verbose_name='Hình ảnh 5')),
                ('Image6', models.ImageField(blank=True, null=True, upload_to='items_images/', verbose_name='Hình ảnh 6')),
                ('PostingDate', models.DateField(auto_now_add=True, verbose_name='Ngày đăng')),
            ],
            options={
                'verbose_name_plural': 'Sản Vật',
            },
        ),
        migrations.CreateModel(
            name='Newspaper',
            fields=[
                ('Newspaper_id', models.AutoField(primary_key=True, serialize=False)),
                ('Title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tiêu đề')),
                ('Title1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tiêu đề 1')),
                ('Content1', models.TextField(blank=True, null=True, verbose_name='Nội dung 1')),
                ('Content2', models.TextField(blank=True, null=True, verbose_name='Nội dung 2')),
                ('Content3', models.TextField(blank=True, null=True, verbose_name='Nội dung 3')),
                ('Content4', models.TextField(blank=True, null=True, verbose_name='Nội dung 4')),
                ('Content5', models.TextField(blank=True, null=True, verbose_name='Nội dung 5')),
                ('Image1', models.ImageField(blank=True, null=True, upload_to='newspapers_images/', verbose_name='Hình ảnh 1')),
                ('Image2', models.ImageField(blank=True, null=True, upload_to='newspapers_images/', verbose_name='Hình ảnh 2')),
                ('Image3', models.ImageField(blank=True, null=True, upload_to='newspapers_images/', verbose_name='Hình ảnh 3')),
                ('Image4', models.ImageField(blank=True, null=True, upload_to='newspapers_images/', verbose_name='Hình ảnh 4')),
                ('Image5', models.ImageField(blank=True, null=True, upload_to='newspapers_images/', verbose_name='Hình ảnh 5')),
                ('PostingDate', models.DateField(auto_now_add=True, verbose_name='Ngày đăng')),
            ],
            options={
                'verbose_name_plural': 'Báo Điện Tử',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('NotificationID', models.AutoField(primary_key=True, serialize=False)),
                ('Title', models.CharField(max_length=255, verbose_name='Tiêu đề')),
                ('Content1', models.TextField(blank=True, null=True, verbose_name='Nội dung 1')),
                ('Content2', models.TextField(blank=True, null=True, verbose_name='Nội dung 2')),
                ('Content3', models.TextField(blank=True, null=True, verbose_name='Nội dung 3')),
                ('Content4', models.TextField(blank=True, null=True, verbose_name='Nội dung 4')),
                ('Content5', models.TextField(blank=True, null=True, verbose_name='Nội dung 5')),
                ('Image1', models.ImageField(blank=True, null=True, upload_to='notification_images/', verbose_name='Hình ảnh 1')),
                ('Image2', models.ImageField(blank=True, null=True, upload_to='notification_images/', verbose_name='Hình ảnh 2')),
                ('Image3', models.ImageField(blank=True, null=True, upload_to='notification_images/', verbose_name='Hình ảnh 3')),
                ('Image4', models.ImageField(blank=True, null=True, upload_to='notification_images/', verbose_name='Hình ảnh 4')),
                ('Image5', models.ImageField(blank=True, null=True, upload_to='notification_images/', verbose_name='Hình ảnh 5')),
                ('PostingDate', models.DateField(auto_now_add=True, verbose_name='Ngày đăng')),
            ],
            options={
                'verbose_name_plural': 'Thông Báo',
            },
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('ProductPrice_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('tphcm_price', models.TextField()),
                ('hanoi_price', models.TextField()),
                ('danang_price', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Giá nông sản',
            },
        ),
        migrations.CreateModel(
            name='SeasonPlan',
            fields=[
                ('SeasonPlanID', models.AutoField(primary_key=True, serialize=False)),
                ('PlanName', models.CharField(max_length=255, verbose_name='Tên')),
                ('Description', models.TextField(verbose_name='Mô tả')),
                ('StartDate', models.DateField(verbose_name='Thời gian bắt đầu')),
                ('EndDate', models.DateField(verbose_name='Thời gian kết thúc')),
            ],
            options={
                'verbose_name_plural': 'Mùa Vụ',
            },
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('Video_id', models.AutoField(primary_key=True, serialize=False)),
                ('Title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tiêu đề')),
                ('Title_phu', models.TextField(blank=True, max_length=255, null=True, verbose_name='Nội dung')),
                ('VideoFile', models.FileField(upload_to='videos/')),
                ('PostingDate', models.DateField(auto_now_add=True, verbose_name='Ngày đăng')),
            ],
            options={
                'verbose_name_plural': 'video bài viết',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('ArticleID', models.AutoField(primary_key=True, serialize=False)),
                ('Title', models.CharField(max_length=255, verbose_name='Tiêu đề')),
                ('Content', models.TextField(verbose_name='Nội dung')),
                ('PostingDate', models.DateField(auto_now_add=True, verbose_name='ngày đăng')),
                ('IsApproved', models.BooleanField(default=False, verbose_name='Duyệt')),
                ('Image', models.ImageField(blank=True, null=True, upload_to='article_images/', verbose_name='Hình ảnh')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('FruitID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='quantri.fruit', verbose_name='Thuộc trái cây')),
            ],
            options={
                'verbose_name_plural': 'Bài Viết',
            },
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Nội dung chat')),
                ('response', models.TextField(verbose_name='Nội dung phản hồi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Thời gian')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('FeedbackID', models.AutoField(primary_key=True, serialize=False)),
                ('Content', models.TextField(verbose_name='nội dung')),
                ('ResponseDate', models.DateTimeField(auto_now_add=True, verbose_name='Ngày đăng')),
                ('notification_message', models.TextField(blank=True, null=True, verbose_name='Nội dung thông báo')),
                ('is_read', models.BooleanField(default=False, verbose_name='Trạng thái thông báo')),
                ('Article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='quantri.article', verbose_name='Bài viết')),
                ('ParentFeedback', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='quantri.feedback', verbose_name='Bình luận cha')),
                ('User', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Bình Luận',
            },
        ),
        migrations.CreateModel(
            name='FruitContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Tiêu đề')),
                ('content', models.TextField(verbose_name='Nội dung')),
                ('image', models.ImageField(null=True, upload_to='fruit_images/', verbose_name='Hình ảnh')),
                ('fruit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='quantri.fruit', verbose_name='Trái cây')),
            ],
            options={
                'verbose_name_plural': 'Nội dung trái cây',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('LocationID', models.AutoField(primary_key=True, serialize=False)),
                ('Latitude', models.DecimalField(decimal_places=15, max_digits=20, verbose_name='Kinh tuyến')),
                ('Longitude', models.DecimalField(decimal_places=15, max_digits=20, verbose_name='Vĩ tuyến')),
                ('Name', models.CharField(max_length=255, verbose_name='Tên địa điểm ')),
                ('FruitType', models.CharField(choices=[('ngan-ngay', 'ngan-ngay'), ('trung-ngay', 'trung-ngay'), ('dai-ngay', 'dai-ngay')], max_length=20, verbose_name='loại cây trồng')),
                ('GrowingRegion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quantri.growingregion', verbose_name='Vùng trồng')),
            ],
            options={
                'verbose_name_plural': 'Địa Điểm ',
            },
        ),
        migrations.AddField(
            model_name='fruit',
            name='Location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fruits', to='quantri.location', verbose_name='Địa điểm trồng'),
        ),
        migrations.CreateModel(
            name='PlantingPlan',
            fields=[
                ('plan_id', models.AutoField(primary_key=True, serialize=False)),
                ('crop_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quantri.croptype', verbose_name='Cây trồng')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quantri.seasonplan', verbose_name='Mùa vụ')),
            ],
            options={
                'verbose_name_plural': 'Kế Hoạch Gieo Trồng',
            },
        ),
        migrations.CreateModel(
            name='CareSchedule',
            fields=[
                ('schedule_id', models.AutoField(primary_key=True, serialize=False)),
                ('care_date', models.TextField(verbose_name='Thời gian')),
                ('fertilizing', models.CharField(max_length=255, verbose_name='Phân bón')),
                ('disease_control', models.CharField(max_length=255, verbose_name='Kiểm soát bệnh')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Ghi chú')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quantri.plantingplan', verbose_name='Tên kế hoạch')),
            ],
            options={
                'verbose_name_plural': 'Lịch Trình Chăm Sóc',
            },
        ),
        migrations.CreateModel(
            name='UserAvatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(null=True, upload_to='avatars/')),
                ('story', models.TextField(null=True, verbose_name='tiểu sử')),
                ('fb', models.TextField(blank=True, null=True)),
                ('zalo', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Thông tin chi tiết User',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=200, verbose_name='Tiêu đề')),
                ('Date', models.DateField(auto_now_add=True)),
                ('VideoFile', models.FileField(upload_to='videos/')),
                ('FruitID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quantri.fruit', verbose_name='Thuộc trái cây')),
            ],
            options={
                'verbose_name_plural': 'Video trái cây',
            },
        ),
    ]

from django.contrib import admin
from .models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('ArticleID', 'Title', 'IsApproved', 'PostingDate')
    list_filter = ('IsApproved', 'FruitID', 'User',)
    search_fields = ('Title',)


admin.site.register(Article, ArticleAdmin)


class Chat_Admin(admin.ModelAdmin):
    list_display = ('user', 'message', 'response')


admin.site.register(Chat, Chat_Admin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('Article', 'User', 'Content', 'ResponseDate', 'is_read')
    list_filter = ('is_read',)
    # Tìm kiếm theo tên người dùng và nội dung
    search_fields = ('User__username', 'Content')


admin.site.register(Feedback, FeedbackAdmin)


class FruitAdmin(admin.ModelAdmin):
    list_display = ('FruitID', 'FruitName', 'PlantingTime', 'HarvestTime', 'Quantity', 'Location')
    list_filter = ('Location',)
    # Tìm kiếm theo tên loại trái cây và tên địa điểm
    search_fields = ('FruitName', 'Location__LocationName')


admin.site.register(Fruit, FruitAdmin)


class FruitContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'fruit', 'title')
    list_filter = ('fruit',)
    search_fields = ('title',)


admin.site.register(FruitContent, FruitContentAdmin)


# Register your models here.
# admin.site.register(Article, ArticleAdmiNo)
# admin.site.register(Article, ArticleAdmin)
class GrowingRegionAdmin(admin.ModelAdmin):
    list_display = ('GrowingRegionID', 'RegionName', 'Area', 'MainProduct')
    list_filter = ('RegionName',)
    search_fields = ('MainProduct',)


admin.site.register(GrowingRegion, GrowingRegionAdmin)


# class ImageAdmin(admin.ModelAdmin):
#     list_display = ('ImageID', 'ImageName', 'Description', 'FruitID', 'ImageURL')
#     list_filter = ('FruitID',)
#     search_fields = ('ImageName', 'Description', 'FruitID__FruitName')  # Tìm kiếm theo tên hình ảnh, mô tả và tên loại trái cây

# admin.site.register(Image, ImageAdmin)
# admin.site.register(Article)
# admin.site.register(User)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('LocationID', 'Name', 'Latitude', 'Longitude', 'GrowingRegion', 'FruitType')
    list_filter = ('GrowingRegion', 'FruitType')
    search_fields = ('Name', 'GrowingRegion__RegionName', 'FruitType')


admin.site.register(Location, LocationAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('NotificationID', 'Title', 'PostingDate',)
    list_filter = ('PostingDate',)
    search_fields = ('Title', 'Content')


admin.site.register(Notification, NotificationAdmin)


class SeasonPlanAdmin(admin.ModelAdmin):
    list_display = ('SeasonPlanID', 'PlanName', 'StartDate', 'EndDate')


admin.site.register(SeasonPlan, SeasonPlanAdmin)


class VideoAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Date', 'FruitID')
    list_filter = ('FruitID',)


admin.site.register(Video, VideoAdmin)


class UserAvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    list_filter = ('user',)
    search_fields = ('user__username',)


admin.site.register(UserAvatar, UserAvatarAdmin)


class CropTypeAdmin(admin.ModelAdmin):
    list_display = ('crop_type_id', 'crop_type_name')
    search_fields = ('crop_type_name',)


admin.site.register(CropType, CropTypeAdmin)


class PlantingPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_id', 'season', 'crop_type')
    list_filter = ('crop_type', 'season',)


admin.site.register(PlantingPlan, PlantingPlanAdmin)


class CareScheduleAdmin(admin.ModelAdmin):
    list_display = ('schedule_id', 'plan', 'care_date', 'fertilizing', 'disease_control', 'note')
    list_filter = ('plan',)


admin.site.register(CareSchedule, CareScheduleAdmin)


class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ('name', 'tphcm_price', 'hanoi_price', 'danang_price')
    search_fields = ('name',)


admin.site.register(ProductPrice, ProductPriceAdmin)


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('Items_id', 'Title')
    search_fields = ('Title',)


admin.site.register(Items, ItemsAdmin)


class NewspaperAdmin(admin.ModelAdmin):
    list_display = ('Newspaper_id', 'Title')
    search_fields = ('Title',)


admin.site.register(Newspaper, NewspaperAdmin)


class VideoAdmin(admin.ModelAdmin):
    list_display = ('Video_id', 'Title', 'PostingDate')
    search_fields = ('Title', 'PostingDate')


admin.site.register(Videos, VideoAdmin)
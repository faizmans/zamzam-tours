from django.db import models

class Category(models.Model):
    # Categories: 'Hajj', 'Umrah', 'National', 'International'
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class TourPackage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='packages')
    title = models.CharField(max_length=200)
    duration_days = models.IntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    cover_image = models.ImageField(upload_to='package_images/')
    video = models.FileField(upload_to='package_videos/', blank=True, null=True, help_text="Upload an optional MP4 promo video")
    
    # Specific fields for Hajj/Umrah
    hotel_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class PackageImage(models.Model):
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='package_gallery/')
    
    def __str__(self):
        return f"Gallery Image for {self.package.title}"

class CustomerInquiry(models.Model):
    package = models.ForeignKey(TourPackage, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[('New', 'New'), ('Contacted', 'Contacted'), ('Closed', 'Closed')],
        default='New'
    )

    def __str__(self):
        return f"Inquiry from {self.customer_name} - {self.status}"
    
    class Meta:
        verbose_name_plural = "Customer Inquiries"
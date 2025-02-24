from django.shortcuts import render
from django.views.generic import TemplateView, View, UpdateView
from accounts.models import Customer
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class SendOTPView(View):
    def post(self, request):
        phone = request.POST.get('phone')
        user, created = Customer.objects.get_or_create(phone=phone)
        if created:
            user.username = phone
            user.save()
        user.generate_otp()
        return JsonResponse({'status': 'success', 'message': 'OTP sent successfully', 'OTP': user.otp})


class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')
        user = Customer.objects.get(phone=phone)
        if user.is_otp_valid(otp):
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful'})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid OTP'})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get(self, request):
        user = Customer.objects.get(phone=request.user)
        return render(request, self.template_name, {'user': user})
    
    def post(self, request):
        user = Customer.objects.get(phone=request.user)
        user.first_name = request.POST.get('first_name') or user.first_name
        user.last_name = request.POST.get('last_name') or user.last_name
        user.email = request.POST.get('email') or user.email
        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES.get('profile_pic')
        user.phone = request.POST.get('phone') or user.phone
        user.save()
        return render(request, self.template_name, {'user': user, 'message': 'Profile updated successfully'})    
    

class WishlistView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/wishlist.html'

    def get(self, request):
        user = Customer.objects.get(phone=request.user)
        return render(request, self.template_name, {'user': user})
    
    def post(self, request):
        user = Customer.objects.get(phone=request.user)
        product_id = request.POST.get('product_id')
        user.wishlist.add(product_id)
        return render(request, self.template_name, {'user': user, 'message': 'Product added to wishlist'})

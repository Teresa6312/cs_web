from .models import (
	Address, Service, CollectionPoint,
	User, Warehouse, FavoriteWebsite, Location
	)
from .forms import (
	NewUserCreationForm, NewUserChangeForm, AddressForm, WebFormSet,
	ColCreationForm, EmailForm, ColChangeForm
	)
# from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.urls import reverse
# used to reverse the url name as a url path

from django.http import QueryDict
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
import os
import json
# from django.core import serializers
from django.utils.translation import gettext as _



class HomeView(TemplateView):
	template_name = 'main/home.html'

	def get(self, request):
		return render(request, self.template_name)


class RegisterView(TemplateView):
	template_name = 'main/register.html'

	def get(self, request):
		form = NewUserCreationForm()
		webformset = WebFormSet()
		return render(request, self.template_name, {'form': form, 'webformset':webformset})

	def post(self, request):
		form = NewUserCreationForm(request.POST)
		webformset = WebFormSet(request.POST)

		if form.is_valid() and webformset.is_valid():
			user = form.save()
			for webform in webformset:
				web = webform.save(commit = False)
				web.country = user.country
				web.web_name = web.web_name.title()

				if webform.is_valid():
					existed_web = FavoriteWebsite.objects.filter(
						web_name = web.web_name,
						web_type = web.web_type,
						country = user.country)

					if existed_web.count() == 1:
						existed_web = existed_web.first()
						existed_web.rate = existed_web.rate +1
						existed_web.save()
					else:
						web.save()

			mail_subject = _('Activate your Qycs Website account.')
			message = render_to_string('email/acc_active_email.html', {
				'user': user,
				'domain': get_current_site(request).domain,
				'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token':account_activation_token.make_token(user),
			})
			email = EmailMessage(mail_subject, message, to=[user.email])
			email.send()

			username = request.POST['username']
			password = request.POST['password1']
			login_user = authenticate(
				username = username,
				password = password
			)
			login(request, login_user)

			if "colregister" in request.POST:
				return redirect(reverse('colregister'))
			else:
				return redirect(reverse('account'))
		else:
			return render(request, self.template_name, {'form': form, 'webformset':webformset})

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return redirect('account')
	else:
		return HttpResponse('Activation link is invalid!')


class SendEmailView(TemplateView):
	template_name = 'main/contact_us_email_template.html'

	def post(self, request):
		email = EmailForm(request.POST)
		next = request.POST.get('next','')
		if email.is_valid():
			subject = _('Contact us - ') + email.subject
			message = _('From ') + user_email + '\n' + email.message
			to_email = ['myqycs.001@gmail.com',]
			if email.cc:
				to_email += user_email

			send_mail(
				subject,
				message,
				to_email,
				fail_silently=False,
			)
			email.send()
		if next and next!='':
			return redirect(next)
		else:
			return redirect(reverse('home'))


class ColRegisterView(TemplateView):
	template_name = 'main/colregister.html'

	def get(self, request):
		userform = NewUserChangeForm(instance=request.user)
		userform.fields['password'].required = False
		userform.fields['phone'].required = True
		colform = ColCreationForm()
		return render(request, self.template_name, {'colform': colform,
													'userform': userform
													})

	def post(self, request):
		userform  = NewUserChangeForm(request.POST, instance=request.user)
		userform.fields['password'].required = False
		colform = ColCreationForm(request.POST, request.FILES)
		if colform.is_valid() and userform.is_valid():
			user = userform.save(request.user)
			collector = colform.save(commit=False)
			collector.collector = user
			collector.save()
			user.default_col = collector
			user.save()
			return redirect(reverse('account'))
		else:
			return render(request, self.template_name, {
					 'colform': colform,
					 'userform': userform,
					 })

class CollectorUpdateView(TemplateView):
	template_name = 'main/collector_update.html'

	def get(self, request):
		if request.user.collectionpoint:
			# col = CollectionPoint.objects.
			form = ColChangeForm(instance = request.user.collectionpoint)
			return render(request, self.template_name, {'form': form})
		else:
			return redirect(reverse('colregister'))

	def post(self, request):
		try:
			col = CollectionPoint.objects.get(collector = request.user)
			form = ColChangeForm(request.POST, request.FILES, instance=col)
			if form.is_valid():
				form.save()
				return redirect(reverse('account'))
		except:
# to the prev page create next for each views
			pass
		else:
			return render(request, self.template_name, {'form': form,
														})

class AccountView(TemplateView):
	template_name = 'main/account.html'

	def get(self, request):
		return render(request, self.template_name)

# -----------------------------------------------------------
'''
Update User Profile
'''
# -----------------------------------------------------------
class UpdateProfileView(TemplateView):
	template_name = 'main/updateprofile.html'
	col_list = CollectionPoint.objects.filter(status=True)

	def get(self, request):
		form = NewUserChangeForm(instance=request.user)
		form.fields['password'].required = False
		return render(request, self.template_name, { 'form': form,
													'col_list': self.col_list,
													})

	def post(self, request):
		form = NewUserChangeForm(request.POST, instance=request.user)
		form.fields['password'].required = False
		if form.is_valid():
			user = form.save()
			return redirect(reverse('account'), user = user)
		else:
			return render(request, self.template_name, {
									'col_list': self.col_list,
									'form': form
									})

class ChangePasswordView(TemplateView):
	template_name = 'main/changepassword.html'

	def get(self, request):
		form = PasswordChangeForm(user = request.user)
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = PasswordChangeForm(data = request.POST, user = request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect(reverse('account'))
		else:
			return render(request, self.template_name, {'form': form})


def locationView(request):
	if request.POST:
		field=request.POST.get('field','')
		value=request.POST.get('value','')
		if field=="id_country":
			locations=[i['country'] for i in Location.objects.filter(country__startswith=value).values('country').distinct()]
			locationsA=[i['state'] for i in Location.objects.filter(country__startswith=value).values('state').distinct()]
			locationsB=[i['city'] for i in Location.objects.filter(country__startswith=value).values('city').distinct()]
			context = json.dumps({
			'data': locations,
			'state': locationsA,
			'city': locationsB})
			return HttpResponse(context, content_type='application/json')
		elif field=="id_state":
			locations=[i['state'] for i in Location.objects.filter(state__startswith=value).values('state').distinct()]
			locationsA=[i['country'] for i in Location.objects.filter(state__startswith=value).values('country').distinct()]
			locationsB=[i['city'] for i in Location.objects.filter(state__startswith=value).values('city').distinct()]
			context = json.dumps({
			'data': locations,
			'country': locationsA,
			'city': locationsB})
			return HttpResponse(context, content_type='application/json')
		elif field=="id_city":
			locations=[i['city'] for i in Location.objects.filter(city__startswith=value).values('city').distinct()]
			locationsA=[i['country'] for i in Location.objects.filter(city__startswith=value).values('country').distinct()]
			locationsB=[i['state'] for i in Location.objects.filter(city__startswith=value).values('state').distinct()]
			context = json.dumps({
			'data': locations,
			'country': locationsA,
			'state': locationsB})
			return HttpResponse(context, content_type='application/json')

class AddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request):
		addform = AddressForm()
		return render(request, self.template_name, {'addform': addform,
		})

	def post(self, request):
		is_popup=request.POST.get('is_popup','')

		if "addform" in request.POST:
			addform = AddressForm(QueryDict(request.POST.get('addform')))
		else:
			addform = AddressForm(request.POST)

		if addform.is_valid():
			newaddress = addform.save(commit = False)
			newaddress.user = request.user
			newaddress.save()
			if is_popup == "True":
				if Address.objects.count()==1:
					user = User.objects.get(user=request.user)
					user.default_address = newaddress
					user.save()
				return render(request, 'main/updateprofile.html', {'newaddress': newaddress})
			else:
				return redirect(reverse('useraddress'))

		else:
			if is_popup == "True":
				return render(request, 'main/updateprofile.html', {'addform': addform})
			else:
				return render(request, self.template_name, {'addform': addform})


# Use updateView?

class EditAddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request, add_id):
		add = Address.objects.get(pk=add_id)
		addform = AddressForm(instance = add)
		return render(request, self.template_name, {'addform': addform})

	def post(self, request, add_id):

		add = Address.objects.get(pk=add_id)

# never update an address that has been shipped with package(s)
		if Service.objects.filter(ship_to_add=add).count()<1:
			# just update the addresss
			addform = AddressForm(request.POST, instance = add)
		else:
			# create a new addresss
			addform = AddressForm(request.POST)

		if addform.is_valid():
			updateaddress = addform.save(commit = False)
			updateaddress.user = request.user

# when create a new address for update, neet to reset the old one's user to be null
			if addform.instance == None:
				add.user = None
				add.save()

			updateaddress.save()
			return redirect(reverse('useraddress'))
		else:
			return render(request, self.template_name, {'addform': addform})


class DeleteAddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request, add_id):
		add = Address.objects.get(pk=add_id)
		add.user = None
		add.save()

		if add == request.user.default_address:
			user = User.objects.get(user = request.user)
			user.default_address = None
			user.save()
		return redirect(reverse('useraddress'))

class SetDefaultAddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request, add_id):
		add = Address.objects.get(pk=add_id)
		user = User.objects.get(user = request.user)
		user.default_address = add
		user.save()
		return redirect(reverse('useraddress'))



class CollectionPointView(TemplateView):
	template_name = 'main/collectionpoints.html'
	col_list = CollectionPoint.objects.filter(status=True)

	def get(self, request):
		return render(request, self.template_name, {'col_list': self.col_list,})


class ShippingView(TemplateView):
	template_name = 'main/select_way_to_ship.html'

	col_list = CollectionPoint.objects.filter(status=True)

	def get(self, request):
		return render(request, self.template_name, {'col_list': self.col_list,})

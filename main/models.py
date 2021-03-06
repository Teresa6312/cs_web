from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import *
# for ordering
from django.db.models import F

from django.utils.translation import ugettext_lazy as _

from django.urls import reverse

from django.db.models.signals import post_save

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from cloudinary.models import CloudinaryField

from datetime import date

phone_regex = RegexValidator(regex=r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$', \
	message=_("Invalid phone number format. Enter as 1-123-456-7890."))

zip_regex = RegexValidator(regex=r'^[0-9]{2,6}(?:-[0-9]{4})?$|^$', message=_("Plese Enter a valid zip code."))

SHIPPING_CARRIER_CHOICE = (
('DHL', _('DHL - Regular items')),
('EMS', _('EMS - All kind of items')),
('SF EXPRESS', _('SF EXPRESS - Regular items')),
('Cheapest', _('The cheapest one')),
('Fastest', _('The fastest one')),
)

CARRIER_CHOICE = (
 ('SF', _('ShunFeng／顺丰速运')),
 ('ChinaPost', _('YouZheng／中国邮政')),
 ('ZTO', _('ZhongTong／中通速递')),
 ('YTO', _('YuanTong／圆通速递')),
 ('STO', _('ShenTong／申通速递')),
 ('ZJS', _('ZhaiJiSong／宅急送')),
 ('YD', _('YunDa／韵达快递')),
 ('JD', _('JingDong／京东物流')),
 ('BS', _('BaiShi／百世快递')),
 ('TTK', _('Tiantian／天天快递')),
 ('EYB', _('EyouBao／E邮宝')),
 ('AAE', _('AAE／AAE快递')),
 ('ADA', _('AnDa／安达速递')),
 ('DP', _('DeBang／德邦快递')),
 ('DD', _('DangDang／当当网')),
 ('UCE', _('YouSu／优速快递')),
 ('QF', _('QuanFeng／全峰快递')),
 ('QY', _('QuanYi／全一快递')),
 ('DHL', _('DHL')),
 ('EMS', _('EMS')),
 ('FEDEX', _('FedEx／联邦快递')),
 ('SF EXPRESS', _('SF EXPRESS／顺丰速运')),
 ('UPS', _('UPS/联合国际快递')),
 ('OTHERS', _('Others／其他')),
)
INSURANCE_CHOICE = (
	(0, _('NO insurance')),
	(3, _('$3 insurance')),
	(5, _('$5 insurance')),
	(10, _('$10 insurance')),
	(15, _('$15 insurance')),
)
CURRENCY_CHOICE = (
	('CNY', _('China Yuan')),
	('USD', _('US Dollar')),
)
WEB_CATEGORY = (
 ('Clothing', _('Clothing')),
 ('Bag', _('Bag')),
 ('Jewelry', _('Jewelry')),
 ('Sport', _('Sport')),
 ('Beauty', _('Beauty')),
 ('Baby', _('Baby')),
 ('Other', _('Other')),
)

PACKAGE_CATEGORY = (
 ('B-F', _('Food/Grocery')),
 ('A-R', _('Regular Goods')),
 ('C-B', _('Beauty')),
 ('D-L', _('Luxury')),
 ('E-M', _('Mix')),
)

INFORMATION_SOURCES = (
	('WC', _('WeChat')),
	('DM', _('Dealmoon')),
)

LANGUAGE_CATEGORY = (
	('EN', _('English')),
	('CN', _('Chinese')),
)

COUNTRY_CHOICE = (
	('cn', _('China')),
	('us', _('United States'))
)

PRICERATE_CATEGORY = (
	('ship', _('Shipping Price')),
	('currency', _('Currency Rate')),
)
PRICE_CARRIER_CHOICE = (
('DHL', _('DHL')),
('EMS', _('EMS')),
('FEDEX', _('FEDEX')),
('SF EXPRESS', _('SF EXPRESS')),
('UPS', _('UPS')),
('DHL+', _('DHL 21kg+')),
('EMS+', _('EMS 21kg+')),
('FEDEX+', _('FEDEX 21kg+')),
('SF EXPRESS+', _('SF EXPRESS 21kg+')),
('UPS+', _('UPS 21kg+')),
)
class User(AbstractUser):
	email = models.EmailField(blank=False, default='', unique=True, verbose_name = _("Email"))
	email_confirmed = models.BooleanField(default =False, verbose_name= _('Email Confirmed'))
	email_confirmed.boolean = True

	phone = models.CharField(validators=[phone_regex], max_length=16, blank=True, default='',verbose_name= _('Phone Number'))
	default_address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True,  related_name='default_address', verbose_name= _('Default Shipping Address'))
	default_col = models.ForeignKey('CollectionPoint', on_delete=models.SET_NULL, blank=True, null=True, verbose_name= _('Default Collection Point'))

	reward = models.PositiveIntegerField(default = 0, verbose_name= _('Reward Points'))
	birthday = models.DateField(blank=True, null=True,verbose_name= _('Birthday'))
	updated_date = models.DateTimeField(auto_now = True, blank=True, null=True, verbose_name=_('Profile Updated Date'))
	country = models.CharField(max_length=100, blank=True, default='',verbose_name= _('Country'))
	language = models.CharField(max_length=100, choices=LANGUAGE_CATEGORY,  blank=True, default='',verbose_name= _('Preferred Language'))
	privacy_policy_agree = models.BooleanField(default =False, verbose_name= _('Privacy Policy Agreement'))
	memo = models.TextField(blank = True, default='', verbose_name= _('Memo'))


	def __str__(self):
		if self.first_name and self.last_name:
			return '%s %s: %s'%(self.first_name, self.last_name, self.email)
		else:
			return '%s : %s'%(self.username, self.email)


	class Meta(AbstractUser.Meta):
		verbose_name_plural = _("Users")
		ordering = ['-id']



class Employee(models.Model):
	employee = models.OneToOneField(User, on_delete=models.PROTECT, primary_key = True, verbose_name=_('Employee'))
	position = models.CharField(max_length=200, blank = True, default = '', verbose_name=_('Employee Position'))
	date_joined = models.DateField(blank=True, null=True, verbose_name= _('Recruitment Date'))
	date_left = models.DateField(blank=True, null=True, verbose_name= _('Resignation Date'))
	created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True, verbose_name= _('Creation Date'))
	updated_date = models.DateTimeField(auto_now = True, blank=True, null=True, verbose_name= _('Employee Profile Updated Date'))
	is_active = models.BooleanField(default =False)
	is_active.boolean = True

	def __str__(self):
		return '%s %s: %s'%(self.employee.first_name, self.employee.last_name, self.position)

	class Meta:
		verbose_name_plural = _("Employees")
		ordering = ['-pk']

def create_emp_profile(sender, **kwargs):
	if kwargs['created']:
		user = kwargs['instance']
		if user.is_staff or user.is_superuser:
			user_profile = Employee.objects.create(employee = kwargs['instance'])

post_save.connect(create_emp_profile, sender = User)

class Address_Common_Info(models.Model):
	created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True, verbose_name= _('Creation Date'))

	address = models.CharField(max_length=500, default='',verbose_name=_('address'))
	apt = models.CharField(blank=True, max_length=200, default='',verbose_name=_('Address2/Apartment'))
	city = models.CharField(max_length=100, default='',verbose_name= _('City'))
	state = models.CharField(max_length=100, default='',verbose_name= _('State/Province'))
	country = models.CharField(max_length=100, default='',verbose_name=_( 'Country'))
	zipcode = models.CharField(max_length=12, validators=[zip_regex], default='', verbose_name= _('Zip Code'))
	memo = models.TextField(blank = True, default='', verbose_name= _('Memo'))

	class Meta:
		abstract = True

class Address(Address_Common_Info):
	updated_date = models.DateTimeField(auto_now = True, blank=True, null=True, verbose_name= _('Address Updated Date'))
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name= _('User'))
	first_name = models.CharField(max_length=100, default='',verbose_name= _('First Name'))
	last_name = models.CharField(max_length=100, default='',verbose_name= _('Last Name'))
	phone = models.CharField(validators=[phone_regex], max_length=16, default='',verbose_name= _('Phone Number'))
	def __str__(self):
		return '%s %s\n %s %s, %s %s'%(self.first_name, self.last_name, self.address, self.city, self.state, self.zipcode)

	def get_absolute_url(self):
		return dict(edit=reverse('editaddress', args=[str(self.id)]),
					delete=reverse('deleteaddress', args=[str(self.id)]),
					set_default=reverse('set_dedault_address', args=[str(self.id)])
					)

	class Meta:
		verbose_name_plural = _("Addresses")
		unique_together=('user'
		,'first_name'
		,'last_name'
		,'phone'
		,'address'
		,'apt'
		,'city'
		,'state'
		,'zipcode'
		)

class CollectionPoint(Address_Common_Info):
	updated_date = models.DateTimeField(auto_now = True, blank=True, null=True, verbose_name= _('Collection Point Updated Date'))
	collector = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True,verbose_name= _('Collector'))
	license_type = models.CharField(max_length = 100, blank=True, default='', verbose_name= _('License type'))


	collector_icon = CloudinaryField( _('Collector Icon'), blank=True, null=True)
	license_image = CloudinaryField( _('Collector License'), blank=True, null=True)
	id_image = CloudinaryField( _('Collector ID'))
	wechat_qrcode = CloudinaryField( _('Collector WeChat'), blank=True, null=True)

	store_name = models.CharField(max_length = 100, blank=True, default='', verbose_name= _('Store Name'))
	store = models.BooleanField(default = True, verbose_name= _('Store'))
	store.boolean = True

	name = models.CharField(max_length = 16, unique = True, blank=False, default='', verbose_name= _('Collection Point Name'))
	paypal = models.EmailField(blank=True, default='', verbose_name = _("Paypal account"))
	wechat = models.CharField(max_length = 100, blank=True, default='', verbose_name= _('WeChat ID'))
	referrer = models.CharField(max_length = 100, blank=True, default='', verbose_name= _('Referrer'))
	apply_reason = models.TextField(blank=True, default='', verbose_name= _('Apply reason'))
	info_source = models.CharField(max_length = 100, choices=INFORMATION_SOURCES, blank=True, default='', verbose_name= _('Information source'))
	agreement = models.BooleanField(default=False, verbose_name= _('Agreement'))


# package category
	food = models.BooleanField(default = False, verbose_name= _('Food'))
	food.boolean = True
	regular = models.BooleanField(default = False, verbose_name= _('Regular'))
	regular.boolean = True
	beauty = models.BooleanField(default = False, verbose_name= _('Beauty'))
	beauty.boolean = True


# the following field can be updated by collector
	status = models.BooleanField(default = False, verbose_name= _('Available'))
	status.boolean = True
	description = models.TextField(blank = True, default='', verbose_name= _('Instruction'))
	show_contact = models.BooleanField(default = False, verbose_name= _('Show Contact Information'))
	show_contact.boolean = True

	# collection_point schedule
	mon_start = models.TimeField(blank=True, null=True, verbose_name= _('Monday'))
	mon_end = models.TimeField(blank=True, null=True, verbose_name= _('Monday End'))
	tue_start = models.TimeField(blank=True, null=True, verbose_name= _('Tuesday'))
	tue_end = models.TimeField(blank=True, null=True, verbose_name= _('Tuesday End'))
	wed_start = models.TimeField(blank=True, null=True, verbose_name= _('Wednesday'))
	wed_end = models.TimeField(blank=True, null=True, verbose_name= _('Wednesday End'))
	thu_start = models.TimeField(blank=True, null=True, verbose_name= _('Thursday'))
	thu_end = models.TimeField(blank=True, null=True, verbose_name= _('Thursday End'))
	fri_start = models.TimeField(blank=True, null=True, verbose_name= _('Friday'))
	fri_end = models.TimeField(blank=True, null=True, verbose_name= _('Friday End'))
	sat_start = models.TimeField(blank=True, null=True, verbose_name= _('Saturday'))
	sat_end = models.TimeField(blank=True, null=True, verbose_name= _('Saturday End'))
	sun_start = models.TimeField(blank=True, null=True, verbose_name= _('Sunday'))
	sun_end = models.TimeField(blank=True, null=True, verbose_name= _('Sunday End'))
	absent_start = models.DateField(blank=True, null=True, verbose_name= _('Absent'))
	absent_end = models.DateField(blank=True, null=True, verbose_name= _('Absent End'))




	def __str__(self):
		return '%s %s %s'%(self.name, self.collector.first_name, self.collector.last_name)

	def get_absolute_url(self):
		return reverse('collection_point_view', args=[str(self.pk)])

	@property
	def absent_started(self):
	    return date.today() > self.absent_start

	@property
	def absent_ended(self):
	    return date.today() > self.absent_end

	def status_all(self):
		if self.absent_start and self.absent_end:
			if date.today()>=self.absent_start and date.today()<=self.absent_end:
				return False
			else:
				return self.status
		else:
			return self.status


	class Meta:
		verbose_name_plural = _("Collection Point")
		ordering = ['-pk']

class CoReceiver(models.Model):
	first_name = models.CharField(max_length = 100, blank=True, default='', verbose_name= _('First Name'))
	last_name = models.CharField(max_length = 100, blank=True, default='', verbose_name= _('Last Name'))
	phone = models.CharField(validators=[phone_regex], max_length=16, blank=True, default='',verbose_name= _('Phone Number'))

	def __str__(self):
		return '%s %s (%s)'%(self.first_name, self.last_name, self.phone)

	class Meta:
		verbose_name_plural = _("Co-receiver")
		unique_together=('first_name','last_name','phone')


class Warehouse(Address_Common_Info):
	updated_date = models.DateTimeField(auto_now = True, blank=True, null=True, verbose_name= _('Warehouse Updated Date'))
	name = models.CharField(max_length=100, unique=True, default='',verbose_name= _('Warehouse Name'))
	status = models.BooleanField(default = False,verbose_name= _('Available'))
	status.boolean = True
	memo = models.TextField(blank=True, default='',verbose_name= _('Memo'))


	def __str__(self):
		return '%s - %s'%(self.country, self.name)

	class Meta:
		verbose_name_plural = _("Warehouse")
		ordering = ['-pk']

class Coupon(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT, blank = True, null=True, verbose_name= _('User'))

	created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True, verbose_name= _('Creation Date'))
	updated_date = models.DateTimeField(auto_now = True, blank=True, null=True, verbose_name= _('Coupon Updated Date'))

	code = models.CharField(max_length = 20, unique = True, default='', verbose_name= _('Coupon Code'))
	discount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], default = 5, verbose_name = _('Discount'))
	amount_limit = models.PositiveIntegerField(blank = True, null = True, verbose_name = _('Amount Limit'))

	start_date = models.DateTimeField(blank = True, null = True, verbose_name= _('Start Date'))
	end_date = models.DateTimeField(blank = True, null = True, verbose_name= _('End Date'))

	package = models.BooleanField(default = False, verbose_name= _('Good For Package'))
	package.boolean = True

	order = models.BooleanField(default = False,verbose_name= _('Good For Order'))
	order.boolean = True

	one_time_only = models.BooleanField(default = True, verbose_name= _('One Time Use Only'))
	one_time_only.boolean = True
	used_times = models.PositiveIntegerField(default=0,verbose_name= _('Coupon Used Times'))
	memo = models.TextField(blank=True, default='',verbose_name= _('Memo'))

	def __str__(self):
		return '%s %d %s'%(self.code,self.discount,"% OFF")

	def check_coupon(self, user):
		if self.user and user != coupon.user:
			return False
		if self.start_date and date.today() < self.start_date:
			return False
		if self.end_date and date.today() > self.end_date:
			return False
		if self.one_time_only and self.used_times!=0:
			return False
		return True


	class Meta:
		verbose_name_plural = _("Coupon")
		ordering = [F('start_date').asc(nulls_last=True)]



class OrderSet(models.Model):
	created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True, verbose_name= _('Creation Date'))
	coupon = models.ForeignKey(Coupon, on_delete=models.DO_NOTHING, blank= True, null=True, verbose_name= _('Coupon'))
	total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0, verbose_name= _('Total Amount'))
	currency = models.CharField(max_length = 100, blank=True, choices=CURRENCY_CHOICE, default='USD', verbose_name= _('Currency'))
	insurance = models.PositiveIntegerField(choices=INSURANCE_CHOICE, blank=False, default=0, verbose_name= _('Insurance Plan'))
	payment_confirmed = models.BooleanField(default=False, verbose_name=_("Payment Confirmed"))
	payment_confirmed.boolean = True
	tx =  models.CharField(max_length = 30, blank=True, verbose_name= _('tx From PayPal'))

	def get_should_pay_amount(self):
		total_amount = 0
		for package in self.service_set.all:
			total_amount = total_amount + package.get_total()

		return total_amount

	def get_total(self):
		amount_package = 0
		amount_order = 0
		for package in self.service_set.all():
			if package.order:
				amount_order = package.get_total() + amount_order
			else:
				amount_package = package.get_total() + amount_package

		for package in self.parentpackage_set.all():
			if package.service_set.first().order:
				amount_order = float (package.package_amount) + amount_order
			else:
				amount_package = float (package.package_amount) + amount_package
		if self.coupon:
			if self.coupon.order and self.coupon.package:
				discounted = (amount_order + amount_package)*self.coupon.discount/100
			elif self.coupon.order:
				discounted = amount_order*self.coupon.discount/100
			elif self.coupon.package:
				discounted = amount_package*self.coupon.discount/100

			if self.coupon.amount_limit and discounted > self.coupon.amount_limit:
				discounted = self.coupon.amount_limit
		else:
			discounted = 0.00


		return [amount_order+amount_package,float('%.2f' % discounted)]

	class Meta:
		verbose_name_plural = _("Order Set")

class ParentPackage(models.Model):
	created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True, verbose_name= _('Creation Date'))
	emp_pack = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank = True, null=True, related_name='package_pack_by_employee',verbose_name= _('Packed by Employee'))
	packed_date = models.DateField(blank=True, null=True,verbose_name= _('Packed Date'))
	memo = models.TextField(blank=True, default='',verbose_name= _('Memo'))

	weight = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=1, verbose_name= _('Weight(kg)'))
	volume_weight = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=1, verbose_name= _('Volume Weight(kg)'))
	package_type = models.CharField(max_length = 16, choices = PACKAGE_CATEGORY, blank=True, default='',verbose_name = _('Package Type'))

	tracking_num = models.CharField(max_length=50, blank=True, default='',verbose_name= _('Tracking Number'))
	carrier = models.CharField(max_length=100, choices=PRICE_CARRIER_CHOICE, blank=True, default='',verbose_name= _('Carrier'))
	shipped_date = models.DateField(blank=True, null=True,verbose_name= _('Shipped Date'))

	package_amount = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= _('Direct Shipping Package Amount'))
	currency = models.CharField(max_length = 100, blank=True, choices=CURRENCY_CHOICE, default='', verbose_name= _('Currency'))

	order_set = models.ForeignKey(OrderSet, on_delete=models.SET_NULL, blank=True, null=True, verbose_name= _('Order Set'))
	paid_amount = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= _('Paid Amount'))
	received_date = models.DateField(blank=True, null=True,verbose_name= _('Received Date'))


# for order only
	emp_split = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank = True, null=True, related_name='emplloyee_splited_package',verbose_name= _('Splitted by Employee'))

	issue = models.TextField(blank=True, default='',verbose_name= _('Package Issue'))



	def ship_to(self):
		if self.service_set.count() > 0:
			if self.service_set.first().ship_to_add:
				return self.service_set.first().ship_to_add
			elif self.service_set.first().ship_to_col:
				return self.service_set.first().ship_to_col
			elif self.service_set.first().ship_to_wh:
				return self.service_set.first().ship_to_wh
			else:
				return ''
		else:
			return ''

	def __str__(self):
		if self.tracking_num=='':
			return "%s - %s"%(self.id, self.ship_to())
		else:
			return "%s - %s: %s"%(self.tracking_num, self.carrier, self.ship_to())

	def get_total(self):
		amount_package = 0
		for package in self.service_set.all():
			amount_package = package.get_total() + amount_package
		return amount_package

	class Meta:
		verbose_name_plural = _("Parent Package")
		ordering = ['-created_date']

class Service(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='client_user',verbose_name= _('User'))
	order_set = models.ForeignKey(OrderSet, on_delete=models.SET_NULL, blank=True, null=True, verbose_name= _('Order Set'))

	order = models.BooleanField(default=False,verbose_name= _('Order'))
	order.boolean = True
	storage = models.BooleanField(default=False,verbose_name= _('Storage'))
	storage.boolean = True
	co_shipping = models.NullBooleanField(verbose_name= _('Co-Shipping'))
	co_shipping.boolean = True
	parent_package = models.ForeignKey(ParentPackage, on_delete=models.SET_NULL, blank = True, null=True,verbose_name= _('Parent Package'))

	created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True, verbose_name= _('Creation Date'))
	package_type = models.CharField(max_length = 16, choices = PACKAGE_CATEGORY, blank=True, default='',verbose_name = _('Package Type'))

# for order only
	emp_created = models.ForeignKey(Employee, on_delete=models.PROTECT, blank = True, null=True, related_name='order_created_by_emplloyee',verbose_name= _('Created by Employee'))

	request_ship_date = models.DateField(blank=True, null=True, verbose_name= _('Date Requested to Ship'))
	memo = models.TextField(blank=True, default='',verbose_name= _('Memo'))
	cust_tracking_num = models.CharField(max_length = 50, blank=True, default='',verbose_name= _("Original Package's Tracking Number"))
	cust_carrier = models.CharField(max_length = 100, choices=CARRIER_CHOICE, blank=True, default='',verbose_name= _("Original Package Carrier"))
	low_volume_request = models.BooleanField(default = True,verbose_name= _('Low Volume Request'))
	low_volume_request.boolean = True

# for direct shipping only
	no_rush_request = models.BooleanField(default = False,verbose_name= _('No Rush Request'))
	no_rush_request.boolean = True

	wh_received = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='received_at_warehouse',verbose_name= _('Inter-warehouse'))
	wh_received_date = models.DateField(blank=True, null=True,verbose_name= _('Warehouse Received Date'))
	ready_date = models.DateField(blank=True, null=True, verbose_name= _('Package Ready Date'))
	emp_pack = models.ForeignKey(Employee, on_delete=models.PROTECT,  blank = True, null=True, related_name='package_repacked_by_employee', verbose_name= _('Packed by Employee'))
	weight = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=1, verbose_name= _('Weight(kg)'))
	volume_weight = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=1, verbose_name= _('Volume Weight(kg)'))
	ship_carrier = models.CharField(max_length = 100, choices=SHIPPING_CARRIER_CHOICE, blank=True, default='',verbose_name= _("Select a Carrier"))



	deposit = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2 , verbose_name= _('Deposit Amount'))

	storage_fee = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= _('Storage Fee'))
	shipping_fee = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= _('Shipping Fee'))
# for order only
	order_amount = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= _('Order Amount'))
	paid_amount = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= _('Paid Amount'))
	currency = models.CharField(max_length = 100, blank=True, choices=CURRENCY_CHOICE, default='', verbose_name= _('Currency'))

# NULL FOR SHIPPING TO COLLECTION POINT
	ship_to_add = models.ForeignKey(Address, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='ship_to_personal_location', verbose_name= _("Shipping Address"))

# NULL FOR SHIP TO USER'S ADDRESS
	ship_to_col = models.ForeignKey(CollectionPoint, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='ship_to_collection_point', verbose_name= _('Shipping Collection Point location'))
	receiver = models.ForeignKey(CoReceiver, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name= _('Receiver'))

# for order only
	ship_to_wh = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='ship_to_warehouse', verbose_name= _('Ship to Warehouse'))

# for picked up in Warehouse or collection point
	picked_up = models.BooleanField(default=False, verbose_name= _('Receiver Picked Up'))
	picked_up.boolean = True

	picked_up_date = models.DateField(blank=True, null=True, verbose_name= _('Picked Up Date'))

	last_shipped_date = models.DateField(blank=True, null=True, verbose_name= _('Final Shipping Date'))
	tracking_num = models.CharField(max_length = 50, blank=True, default='', verbose_name= _('Final Shipping Tracking Number'))
	last_carrier = models.CharField(max_length = 100, choices=CARRIER_CHOICE, blank=True, default='', verbose_name= _('Final Shipping Carrier'))

	issue = models.TextField(blank=True, default='', verbose_name= _('Package Issue'))
	refund_amount = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= _('Refund Amount'))

	def get_total(self):
		total = 0.0
		if self.storage_fee:
			total = total +  float (self.storage_fee)
		if self.shipping_fee:
			total = total + float (self.shipping_fee)
		if self.order_amount:
			total = total + float (self.order_amount)
		return total

	def ship_to(self):
		if self.co_shipping:
			return self.ship_to_col
		elif self.ship_to_add:
			return self.ship_to_add
		elif self.ship_to_wh:
			return self.ship_to_wh
		else:
			return ''

	def __str__(self):
		if self.ship_to():
			if self.order:
				return "%s's Order created on %s \n ship to %s"%(self.user, self.created_date, self.ship_to())
			elif self.co_shipping:
				return "%s's package created on %s \n ship to %s"%(self.user, self.created_date, self.ship_to())
			else:
				return "%s's package created on %s \n"%(self.user, self.created_date)
		else:
			return "%s's package created on %s \n"%(self.user, self.created_date)

	def get_absolute_url(self):
		return reverse('package_detail', args=[str(self.id)])

	def status_all(self):
		if self.picked_up:
			return _('The receiver has picked up the package.')
		elif self.parent_package:
			if self.parent_package.issue != '' and self.parent_package.issue != None:
				return _('Package is being holded on the way to your selected location.\nPlease view the detail for more information.')
			elif self.parent_package.shipped_date:
				return _('Package have been shipped out from Warehouse.')
			else:
				return _('Package is ready to ship out from Warehouse.')
		elif self.issue != '' and self.issue != None:
			return _('There is some problem with your package.\nPlease view the detail for more information.')
		elif self.paid_key:
			return _('Package has been paid, and it is being prepared to ship out from Warehouse')
		elif self.ready_date:
			return _('Package is ready to pay.')
		elif self.wh_received_date:
			return _('Package arrived the Warehouse.')
		else:
			return _('N/A')

	class Meta:
		verbose_name_plural = _("Package/Order")
		ordering = ['-created_date']


class Item(models.Model):
	service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name = _('Package/Order'))
	item_name = models.CharField(max_length = 200, blank=False, default='', verbose_name = _('Item Name'))
	item_detail = models.CharField(max_length = 100, blank=True, default='', verbose_name = _('Item Details'))
	item_quantity = models.PositiveIntegerField(blank=False, default=1, verbose_name = _('quantity'))
	item_value = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name = _('Item Value'))
	currency = models.CharField(max_length = 100, choices=CURRENCY_CHOICE, blank=True, default='', verbose_name = _('Currency'))
	item_url  = models.CharField(max_length = 1000, blank=True, default='', verbose_name = _('Item URL'))
	memo = models.TextField(blank=True, default='', verbose_name = _('Memo'))
	low_volume_request = models.BooleanField(default = True,verbose_name= _('Low Volume Request'))
	low_volume_request.boolean = True

	# for order only
	tax_included = models.BooleanField(default=True, verbose_name = _('Included Tax'))
	tax_included.boolean = True

	order_by = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, blank = True, null=True, verbose_name = _('Order by Employee'))

	def __str__(self):
		return self.item_name

	class Meta:
		verbose_name_plural = _("Item")
		ordering = ['service']


class PackageSnapshot(models.Model):
	package = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name = _('Package'))
	snapshot = CloudinaryField(_("Package Snapshot"))

	class Meta:
		verbose_name_plural = _("Package Snapshots")
		ordering = ['package']

class FavoriteWebsite(models.Model):

	country = models.CharField(max_length=100, blank=True, default='',verbose_name= _('Country'))
	web_type = models.CharField(max_length = 50, choices = WEB_CATEGORY, blank=True, default='',verbose_name = _('Category'))
	web_name = models.CharField(max_length = 100, blank=True, default='', verbose_name = _('Website Name'))
	web_url = models.URLField (max_length = 1000, blank=True, default='', verbose_name = _('Website url'))
	rate = models.PositiveIntegerField(default=1, verbose_name = _('Rating'))

	class Meta:
		verbose_name_plural = _("Favorite Website")
		ordering = ['web_name']

class Resource(models.Model):
	title = models.CharField(max_length=100, default='', unique=True, verbose_name= _('Title'))
	english_header = models.CharField(max_length=100, default='', verbose_name= _('English Header'))
	chinese_header = models.CharField(max_length=100, default='', verbose_name= _('Chinese Header'))
	english_content = models.TextField(blank=True, default='',  verbose_name= _('English Version Content'))
	chinese_content = models.TextField(blank=True, default='', verbose_name= _('Chinese Version Content'))
	english_file = models.FileField(upload_to = 'resource/english', blank=True,  verbose_name= _('English Version File'))
	chinese_file = models.FileField(upload_to = 'resource/chinese', blank=True, verbose_name= _('Chinese Version File'))

	class Meta:
		verbose_name_plural = _("Resource")

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('information', args=[str(self.title)])

class Location(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	city = models.CharField(max_length=100, blank=True, default='',verbose_name= _('City'))
	state = models.CharField(max_length=100, blank=True, default='',verbose_name= _('State/Province'))
	country = models.CharField(max_length=100, blank=False, default='',verbose_name= _('Country'))
	country_shortname = models.CharField(max_length=100, blank=False, default='',verbose_name= _('Country Shortname'))

	class Meta:
		verbose_name_plural = _("Location")

class PriceRate(models.Model):
	category = models.CharField(max_length = 50, choices = PRICERATE_CATEGORY, blank=True, default='', verbose_name = _('Category'))
	from_country = models.CharField(max_length=50, choices = COUNTRY_CHOICE, blank=True, default='', verbose_name= _('From Country'))
	to_country = models.CharField(max_length=50, choices = COUNTRY_CHOICE, blank=True, default='', verbose_name= _('To_Country'))
	package_type = models.CharField(max_length = 16, choices = PACKAGE_CATEGORY, blank=True, default='',verbose_name = _('Package Type'))
	carrier = models.CharField(max_length = 100, choices=PRICE_CARRIER_CHOICE, blank=True, default='', verbose_name= _('Shipping Carrier'))
	period = models.CharField(max_length = 100, default='',  blank=True, verbose_name= _('Shipping Period'))
	shipping_currency = models.CharField(max_length = 100, blank=True, choices=CURRENCY_CHOICE, default='USD', verbose_name= _('Currency for Shipping Price'))
	first_weight_price = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= _('First Weight Price'))
	next_weight_price = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= _('Next Weight Price'))
	avg_weight_price = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= _('Average Weight Price'))

	rate = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= _('Currency Rate'))

	class Meta:
		verbose_name_plural = _("Price Rate")
		unique_together=(
			'category',
			'from_country',
			'to_country',
			'package_type',
			'carrier',
		)

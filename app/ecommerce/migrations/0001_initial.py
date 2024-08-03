# Generated by Django 4.2.14 on 2024-08-03 17:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_guest', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('unit_number', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(choices=[('Afghanistan', 'Afghanistan'), ('Aland Islands', 'Aland Islands'), ('Albania', 'Albania'), ('Algeria', 'Algeria'), ('American Samoa', 'American Samoa'), ('Andorra', 'Andorra'), ('Angola', 'Angola'), ('Anguilla', 'Anguilla'), ('Antarctica', 'Antarctica'), ('Antigua and Barbuda', 'Antigua and Barbuda'), ('Argentina', 'Argentina'), ('Armenia', 'Armenia'), ('Aruba', 'Aruba'), ('Australia', 'Australia'), ('Austria', 'Austria'), ('Azerbaijan', 'Azerbaijan'), ('Bahamas', 'Bahamas'), ('Bahrain', 'Bahrain'), ('Bangladesh', 'Bangladesh'), ('Barbados', 'Barbados'), ('Belgium', 'Belgium'), ('Belize', 'Belize'), ('Benin', 'Benin'), ('Bermuda', 'Bermuda'), ('Bhutan', 'Bhutan'), ('Bolivia, Plurinational State of', 'Bolivia, Plurinational State of'), ('Bonaire, Sint Eustatius and Saba', 'Bonaire, Sint Eustatius and Saba'), ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'), ('Botswana', 'Botswana'), ('Bouvet Island', 'Bouvet Island'), ('Brazil', 'Brazil'), ('British Indian Ocean Territory', 'British Indian Ocean Territory'), ('Brunei Darussalam', 'Brunei Darussalam'), ('Bulgaria', 'Bulgaria'), ('Burkina Faso', 'Burkina Faso'), ('Burundi', 'Burundi'), ('Cambodia', 'Cambodia'), ('Cameroon', 'Cameroon'), ('Canada', 'Canada'), ('Cape Verde', 'Cape Verde'), ('Cayman Islands', 'Cayman Islands'), ('Central African Republic', 'Central African Republic'), ('Chad', 'Chad'), ('Chile', 'Chile'), ('China', 'China'), ('Christmas Island', 'Christmas Island'), ('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'), ('Colombia', 'Colombia'), ('Comoros', 'Comoros'), ('Congo', 'Congo'), ('Congo, The Democratic Republic of the', 'Congo, The Democratic Republic of the'), ('Cook Islands', 'Cook Islands'), ('Costa Rica', 'Costa Rica'), ("Côte d'Ivoire", "Côte d'Ivoire"), ('Croatia', 'Croatia'), ('Cuba', 'Cuba'), ('Curaçao', 'Curaçao'), ('Cyprus', 'Cyprus'), ('Czech Republic', 'Czech Republic'), ('Denmark', 'Denmark'), ('Djibouti', 'Djibouti'), ('Dominica', 'Dominica'), ('Dominican Republic', 'Dominican Republic'), ('Ecuador', 'Ecuador'), ('Egypt', 'Egypt'), ('El Salvador', 'El Salvador'), ('Equatorial Guinea', 'Equatorial Guinea'), ('Eritrea', 'Eritrea'), ('Estonia', 'Estonia'), ('Ethiopia', 'Ethiopia'), ('Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas)'), ('Faroe Islands', 'Faroe Islands'), ('Fiji', 'Fiji'), ('Finland', 'Finland'), ('France', 'France'), ('French Guiana', 'French Guiana'), ('French Polynesia', 'French Polynesia'), ('French Southern Territories', 'French Southern Territories'), ('Gabon', 'Gabon'), ('Gambia', 'Gambia'), ('Georgia', 'Georgia'), ('Germany', 'Germany'), ('Ghana', 'Ghana'), ('Gibraltar', 'Gibraltar'), ('Greece', 'Greece'), ('Greenland', 'Greenland'), ('Grenada', 'Grenada'), ('Guadeloupe', 'Guadeloupe'), ('Guam', 'Guam'), ('Guatemala', 'Guatemala'), ('Guernsey', 'Guernsey'), ('Guinea', 'Guinea'), ('Guinea-Bissau', 'Guinea-Bissau'), ('Guyana', 'Guyana'), ('Haiti', 'Haiti'), ('Heard Island and McDonald Islands', 'Heard Island and McDonald Islands'), ('Holy See (Vatican City State)', 'Holy See (Vatican City State)'), ('Honduras', 'Honduras'), ('Hong Kong', 'Hong Kong'), ('Hungary', 'Hungary'), ('Iceland', 'Iceland'), ('India', 'India'), ('Indonesia', 'Indonesia'), ('Iran, Islamic Republic of', 'Iran, Islamic Republic of'), ('Iraq', 'Iraq'), ('Ireland', 'Ireland'), ('Isle of Man', 'Isle of Man'), ('Israel', 'Israel'), ('Italy', 'Italy'), ('Jamaica', 'Jamaica'), ('Japan', 'Japan'), ('Jersey', 'Jersey'), ('Jordan', 'Jordan'), ('Kazakhstan', 'Kazakhstan'), ('Kenya', 'Kenya'), ('Kiribati', 'Kiribati'), ("Korea, Democratic People's Republic of", "Korea, Democratic People's Republic of"), ('Korea, Republic of', 'Korea, Republic of'), ('Kuwait', 'Kuwait'), ('Kyrgyzstan', 'Kyrgyzstan'), ("Lao People's Democratic Republic", "Lao People's Democratic Republic"), ('Latvia', 'Latvia'), ('Lebanon', 'Lebanon'), ('Lesotho', 'Lesotho'), ('Liberia', 'Liberia'), ('Libya', 'Libya'), ('Liechtenstein', 'Liechtenstein'), ('Lithuania', 'Lithuania'), ('Luxembourg', 'Luxembourg'), ('Macao', 'Macao'), ('Macedonia, Republic of', 'Macedonia, Republic of'), ('Madagascar', 'Madagascar'), ('Malawi', 'Malawi'), ('Malaysia', 'Malaysia'), ('Maldives', 'Maldives'), ('Mali', 'Mali'), ('Malta', 'Malta'), ('Marshall Islands', 'Marshall Islands'), ('Martinique', 'Martinique'), ('Mauritania', 'Mauritania'), ('Mauritius', 'Mauritius'), ('Mayotte', 'Mayotte'), ('Mexico', 'Mexico'), ('Micronesia, Federated States of', 'Micronesia, Federated States of'), ('Moldova, Republic of', 'Moldova, Republic of'), ('Monaco', 'Monaco'), ('Mongolia', 'Mongolia'), ('Montenegro', 'Montenegro'), ('Montserrat', 'Montserrat'), ('Morocco', 'Morocco'), ('Mozambique', 'Mozambique'), ('Myanmar', 'Myanmar'), ('Namibia', 'Namibia'), ('Nauru', 'Nauru'), ('Nepal', 'Nepal'), ('Netherlands', 'Netherlands'), ('New Caledonia', 'New Caledonia'), ('New Zealand', 'New Zealand'), ('Nicaragua', 'Nicaragua'), ('Niger', 'Niger'), ('Nigeria', 'Nigeria'), ('Niue', 'Niue'), ('Norfolk Island', 'Norfolk Island'), ('Northern Mariana Islands', 'Northern Mariana Islands'), ('Norway', 'Norway'), ('Oman', 'Oman'), ('Pakistan', 'Pakistan'), ('Palau', 'Palau'), ('Palestinian Territory, Occupied', 'Palestinian Territory, Occupied'), ('Panama', 'Panama'), ('Papua New Guinea', 'Papua New Guinea'), ('Paraguay', 'Paraguay'), ('Peru', 'Peru'), ('Philippines', 'Philippines'), ('Pitcairn', 'Pitcairn'), ('Poland', 'Poland'), ('Portugal', 'Portugal'), ('Puerto Rico', 'Puerto Rico'), ('Qatar', 'Qatar'), ('Réunion', 'Réunion'), ('Romania', 'Romania'), ('Rwanda', 'Rwanda'), ('Saint Barthélemy', 'Saint Barthélemy'), ('Saint Helena, Ascension and Tristan da Cunha', 'Saint Helena, Ascension and Tristan da Cunha'), ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'), ('Saint Lucia', 'Saint Lucia'), ('Saint Martin (French part)', 'Saint Martin (French part)'), ('Saint Pierre and Miquelon', 'Saint Pierre and Miquelon'), ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'), ('Samoa', 'Samoa'), ('San Marino', 'San Marino'), ('Sao Tome and Principe', 'Sao Tome and Principe'), ('Saudi Arabia', 'Saudi Arabia'), ('Senegal', 'Senegal'), ('Serbia', 'Serbia'), ('Seychelles', 'Seychelles'), ('Sierra Leone', 'Sierra Leone'), ('Singapore', 'Singapore'), ('Sint Maarten (Dutch part)', 'Sint Maarten (Dutch part)'), ('Slovakia', 'Slovakia'), ('Slovenia', 'Slovenia'), ('Solomon Islands', 'Solomon Islands'), ('Somalia', 'Somalia'), ('South Africa', 'South Africa'), ('South Georgia and the South Sandwich Islands', 'South Georgia and the South Sandwich Islands'), ('Spain', 'Spain'), ('Sri Lanka', 'Sri Lanka'), ('Sudan', 'Sudan'), ('Suriname', 'Suriname'), ('South Sudan', 'South Sudan'), ('Svalbard and Jan Mayen', 'Svalbard and Jan Mayen'), ('Swaziland', 'Swaziland'), ('Sweden', 'Sweden'), ('Switzerland', 'Switzerland'), ('Syrian Arab Republic', 'Syrian Arab Republic'), ('Taiwan, Province of China', 'Taiwan, Province of China'), ('Tajikistan', 'Tajikistan'), ('Tanzania, United Republic of', 'Tanzania, United Republic of'), ('Thailand', 'Thailand'), ('Timor-Leste', 'Timor-Leste'), ('Togo', 'Togo'), ('Tokelau', 'Tokelau'), ('Tonga', 'Tonga'), ('Trinidad and Tobago', 'Trinidad and Tobago'), ('Tunisia', 'Tunisia'), ('Turkey', 'Turkey'), ('Turkmenistan', 'Turkmenistan'), ('Turks and Caicos Islands', 'Turks and Caicos Islands'), ('Tuvalu', 'Tuvalu'), ('Uganda', 'Uganda'), ('Ukraine', 'Ukraine'), ('United Arab Emirates', 'United Arab Emirates'), ('United Kingdom', 'United Kingdom'), ('United States', 'United States'), ('United States Minor Outlying Islands', 'United States Minor Outlying Islands'), ('Uruguay', 'Uruguay'), ('Uzbekistan', 'Uzbekistan'), ('Vanuatu', 'Vanuatu'), ('Venezuela, Bolivarian Republic of', 'Venezuela, Bolivarian Republic of'), ('Viet Nam', 'Viet Nam'), ('Virgin Islands, British', 'Virgin Islands, British'), ('Virgin Islands, U.S.', 'Virgin Islands, U.S.'), ('Wallis and Futuna', 'Wallis and Futuna'), ('Yemen', 'Yemen'), ('Zambia', 'Zambia'), ('Zimbabwe', 'Zimbabwe')], max_length=50)),
                ('region', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('post_code', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AttributeOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('discount_rate', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.PositiveSmallIntegerField(choices=[(1, 'CARD'), (2, 'CASH_ON_DELIVERY'), (3, 'BANK_TRANSFER')], default=1)),
                ('shipping_method', models.PositiveSmallIntegerField(choices=[(1, 'UPS'), (2, 'DHL')], default=1)),
                ('order_price', models.PositiveIntegerField()),
                ('order_status', models.PositiveSmallIntegerField(choices=[(1, 'NEW'), (2, 'IN_PROGRESS'), (3, 'SHIPPED'), (4, 'DONE')], default=1)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecommerce.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('M', 'Man'), ('W', 'Woman')], max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('attribute_option', models.ManyToManyField(to='ecommerce.attributeoption')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.brand')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('product_code', models.CharField(max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.color')),
                ('discount', models.ManyToManyField(related_name='discount', to='ecommerce.discount')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_item', to='ecommerce.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('1 L', '1 l'), ('2 L', '2 l'), ('3 L', '3 l'), ('4 L', '4 l'), ('5 L', '5 l'), ('6 L', '6 l'), ('7 L', '7 l'), ('8 L', '8 l'), ('9 L', '9 l'), ('10 L', '10 l'), ('11 L', '11 l'), ('12 L', '12 l'), ('13 L', '13 l'), ('14 L', '14 l'), ('15 L', '15 l'), ('16 L', '16 l'), ('17 L', '17 l'), ('18 L', '18 l'), ('19 L', '19 l'), ('20 L', '20 l'), ('21 L', '21 l'), ('22 L', '22 l'), ('23 L', '23 l'), ('24 L', '24 l'), ('25 L', '25 l'), ('26 L', '26 l'), ('27 L', '27 l'), ('28 L', '28 l'), ('29 L', '29 l'), ('30 L', '30 l'), ('31 L', '31 l')], max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty_in_stock', models.PositiveIntegerField()),
                ('product_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_variation', to='ecommerce.productitem')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.productsize')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SizeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('SHOES', 'shoes'), ('CLOTHES', 'clothes'), ('BAGS', 'bags')], max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_default', models.BooleanField(default=False)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='ecommerce.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart_item', to='ecommerce.shoppingcart')),
                ('product_variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart_item', to='ecommerce.productvariation')),
            ],
        ),
        migrations.AddField(
            model_name='productsize',
            name='size_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.sizecategory'),
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('image', models.URLField(blank=True, null=True)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.productcategory')),
                ('size_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.sizecategory')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.productcategory'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('price', models.PositiveIntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='ecommerce.order')),
                ('product_variation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_item', to='ecommerce.productvariation')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255)),
                ('product_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='ecommerce.productitem')),
            ],
        ),
        migrations.AddField(
            model_name='attributeoption',
            name='attribute_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.attributetype'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.ManyToManyField(related_name='address_to_user', through='ecommerce.UserAddress', to='ecommerce.address'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]

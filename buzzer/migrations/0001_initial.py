import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Buzz',
            fields=[
                ('id_buzz', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(max_length=140)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('file', models.FileField(blank=True, upload_to='buzzfile', verbose_name='Buzz File')),
                ('file_type', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id_chat', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('members', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('rejected', models.DateTimeField(blank=True, null=True)),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_follows', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_is_followed', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('text', models.TextField(max_length=140, primary_key=True, serialize=False)),
                ('buzzs', models.ManyToManyField(to='buzzer.Buzz')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id_message', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('content', models.CharField(max_length=140)),
                ('notified', models.BooleanField(default=False)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buzzer.Chat')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id_notification', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=140)),
                ('description', models.TextField(max_length=140)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('showed', models.BooleanField(default=False)),
                ('type_notification', models.PositiveIntegerField(default=0)),
                ('buzz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='buzzer.Buzz')),
                ('follower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('message', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='buzzer.Message')),
                ('user_notify', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='who_is_notified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screen_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=150)),
                ('url', models.CharField(max_length=150)),
                ('bio', models.CharField(max_length=150)),
                ('birthday', models.DateField(null=True)),
                ('image', models.ImageField(default='media/buzzer_logo.png', upload_to='media', verbose_name='Image')),
                ('count_follower', models.PositiveIntegerField(default=0)),
                ('count_followed', models.PositiveIntegerField(default=0)),
                ('count_notification', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

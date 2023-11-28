# Generated by Django 4.2.5 on 2023-10-29 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_uploadedpdf'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc', models.FileField(upload_to='docs/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='UploadedPDF',
        ),
    ]
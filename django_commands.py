# Update models in "models.py".

# Create migrations for those changes.
python manage.py makemigrations

# Take all the migrations that haven’t been applied and run them against the database.
# Essentially, synchronize the changes made to the models with the schema in the database.
python manage.py migrate

# Create a user who can login to the admin site.
python manage.py createsuperuser

# python manage.py makemigrations feat

# Run the application
python manage.py runserver
#python manage.py runserver ec2-35-153-202-107.compute-1.amazonaws.com:8000